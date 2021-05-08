import sys
from os import path

BASE_DIR = path.dirname(path.dirname(path.abspath(__file__)))
sys.path.append(BASE_DIR)

import json
import traceback
from collections import defaultdict
from functools import wraps
from inspect import isclass, isfunction
from pprint import pprint
from typing import Callable, Literal, NewType, Optional, Type, TypeVar, Union

import arrow
from devtools import debug
from inflection import camelize
from pydantic import BaseModel
from sanic import Sanic
from sanic.websocket import WebSocketProtocol

from src.Bots.Bots import *
from src.Events import GroupIncrease, MetaEvent
from src.Parse import GROUP_EVENTS_T, RELATIONS, GroupEvent
from src.Parse.figure import figure_out
from src.User.Sender import Sender
from src.Action.main import *

app = Sanic("PepperBot")


# MethodHooks = TypeVar("MethodHooks", )
# MethodHook = TypeVar(
#     "MethodHook",
# )


class GroupHandler(BaseModel):
    class_: Callable
    args: List[Any] = []
    kwargs: Dict[str, Any] = {}


class GroupCache(BaseModel):
    botInstance: BotBase
    instance: Union[Callable, Any]
    # methods: Dict[GROUP_EVENTS_T, List[Any]] = defaultdict(list)
    methods: Dict[str, List[Any]] = defaultdict(list)

    class Config:
        arbitrary_types_allowed = True


class ClassHandler(BaseModel):
    group: Dict[int, List[GroupHandler]] = defaultdict(list)
    groupCache: Dict[int, List[GroupCache]] = defaultdict(list)


# function handlers
functionHandlers = defaultdict(list)
# classHandlers = {"group": defaultdict(list), "groupCache": defaultdict(list)}
classHandlers = ClassHandler()


# EventTypes = TypeVar("EventTypes")


def get_parent_level(bottomGroupEvent: Union[str, Any]):
    for key, value in RELATIONS["group"].items():
        if bottomGroupEvent in value:
            return key

    raise Exception("无效事件")


GROUP_EVENTS: List[str] = []

for _type, subTypes in RELATIONS["group"].items():
    GROUP_EVENTS.extend(subTypes)

GROUP_EVENTS_WITH_LIFECYCLE = [*GROUP_EVENTS]
for event in GROUP_EVENTS:
    GROUP_EVENTS_WITH_LIFECYCLE.append("Before" + event)
    GROUP_EVENTS_WITH_LIFECYCLE.append("After" + event)


def is_group_event(event: Union[str, Any]) -> bool:
    return event in GROUP_EVENTS


print("GroupMessage" in GROUP_EVENTS)
print(GroupEvent.GroupMessage in GROUP_EVENTS)


def is_valid_group_method(methodName: str):

    camelMethodName = camelize(methodName)
    return camelMethodName in GROUP_EVENTS_WITH_LIFECYCLE


def construct_api(ws):
    async def api(route: str, **kwargs):
        await ws.send(
            json.dumps(
                {
                    "action": route,
                    "params": {**kwargs},
                }
            )
        )

    return api


def construct_bot(ws, groupId: int) -> AddGroupBot:
    return AddGroupBot(construct_api(ws), groupId)


def construct_chain(receive: dict, ws, groupId) -> MessageChain:
    return MessageChain(event=receive, groupId=groupId, api=construct_api(ws))


def construct_sender(receive: dict, ws):
    return Sender(event=receive, api=construct_api(ws))


GroupIdInstanceMap = {}


def get_instance(groupId):
    instance = GroupIdInstanceMap.get(groupId)
    if instance:
        return instance
    else:
        pass


def dispatcher():
    pass


def register(groupId: Union[int, str, List[Union[int, str]]], *args, **kwargs):
    def decorator(handler: object):
        if isclass(handler):
            finalGroupIds: List[int] = []

            if isinstance(groupId, int):
                finalGroupIds.append(groupId)

            elif isinstance(groupId, str):
                finalGroupIds.append(int(groupId))

            elif isinstance(groupId, list):
                for id in groupId:
                    finalGroupIds.append(int(id))

            if finalGroupIds:
                for id in finalGroupIds:
                    newHandler = GroupHandler(
                        **{"class_": handler, "args": [*args], "kwargs": {**kwargs}}
                    )

                    classHandlers.group[id].append(newHandler)
            else:
                print("未能解析事件响应class")

        else:
            print("应为class")

        return handler

    return decorator


def on(eventType, *args, **kwargs):
    def decorator(handler: Union[Callable[[], None], object]):

        if isfunction(handler):
            functionHandlers[eventType].append(handler)

    return decorator


@on("metaEvent")
async def handle(*args):
    # print(args)
    print("in meta")


def __skip_buffer():
    pass


def __cache(ws):
    _cache = classHandlers.groupCache

    for groupId, handlers in classHandlers.group.items():
        for handler in handlers:

            #  不要每次都创建实例，on监听器新增时建立一次，之后都保存起来即可
            _instance = handler.class_()
            buffer = GroupCache(
                instance=_instance, botInstance=construct_bot(ws, groupId)
            )

            # 初始化时，遍历生成缓存，不要每次接收到消息都去遍历
            for methodName in dir(_instance):

                methodOrProperty = getattr(_instance, methodName)

                if callable(methodOrProperty):
                    if not methodName.startswith("__"):
                        if is_valid_group_method(methodName):
                            # todo 作为参数时，cast类型
                            buffer.methods[camelize(methodName)].append(  # type: ignore
                                methodOrProperty
                            )

            _cache[groupId].append(buffer)


def __output_config():
    debug(classHandlers)


hasInitial = False
{"data": {"message_id": -1046833221}, "retcode": 0, "status": "ok"}


@app.websocket("/cqhttp/ws")
async def main_entry(request, ws):
    global hasInitial

    if not hasInitial:
        __cache(ws)
        __output_config()
        hasInitial = True

    # todo 跳过缓存/过期的消息，根据心跳时间判断(比如离当前时间<5s)
    __skip_buffer

    while True:

        try:

            print("*" * 50)
            data = await ws.recv()
            receive = json.loads(data)

            finalEvent: Union[str, None, GROUP_EVENTS_T] = None
            try:
                finalEvent = figure_out(receive)
            except KeyError:
                pprint(receive)

            if finalEvent:
                if finalEvent == GroupEvent.MetaEvent:
                    print(
                        arrow.get(receive["time"])
                        .to("Asia/Shanghai")
                        .format("YYYY-MM-DD HH:mm:ss")
                    )

                    metaEvent = MetaEvent(**receive)
                    debug(metaEvent)
                else:
                    pprint(receive)

                # hooks
                for handler in functionHandlers[finalEvent]:
                    await handler(receive)

                # group class
                if is_group_event(finalEvent):
                    groupId = receive["group_id"]

                    for handler in classHandlers.groupCache[groupId]:

                        # instance = handler['instance']
                        botInstance = handler.botInstance

                        parentLevel = get_parent_level(finalEvent)
                        eventName = finalEvent

                        args: Dict[str, Union[BotBase, MessageChain, Sender, Any]] = {
                            "bot": botInstance
                        }
                        if parentLevel == "GroupMessage":
                            args["chain"] = construct_chain(
                                receive, groupId=groupId, ws=ws
                            )
                            args["sender"] = construct_sender(receive, ws)

                        elif parentLevel == "GroupRequest":
                            if finalEvent == GroupEvent.AddGroup:
                                args = {
                                    "bot": GroupRequestBot(
                                        api=construct_api(ws), flag=receive.get("flag")
                                    ),
                                    "event": receive,
                                }

                        elif parentLevel == "GroupNotice":
                            if finalEvent == GroupEvent.MemberIncreased:
                                event = GroupIncrease.GroupIncreaseEvent(**receive)
                                member = await api.member(
                                    groupId=event.group_id, userId=event.user_id
                                )

                                debug(member)

                                args = {
                                    "bot": GroupNoticeBot(
                                        api=construct_api(ws),
                                        groupId=groupId,
                                    ),
                                    "event": receive,
                                    "member": member,
                                }

                            else:
                                args = {
                                    "bot": GroupNoticeBot(
                                        api=construct_api(ws),
                                        groupId=groupId,
                                    ),
                                    "event": receive,
                                }

                        # 按照生命周期调用
                        for method in handler.methods["Before" + eventName]:
                            await method(**args)

                        for method in handler.methods[eventName]:
                            await method(**args)

                        for method in handler.methods["After" + eventName]:
                            await method(**args)

            else:
                print("un register event")

        except Exception as e:
            print(e)
            print(traceback.format_exc())


def run(host: str = "0.0.0.0", port: int = 8080, debug: bool = False):
    app.run(host, port, protocol=WebSocketProtocol, debug=debug)
