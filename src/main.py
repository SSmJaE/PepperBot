import json
import sys
from collections import defaultdict
from inspect import isclass, isfunction
from os import path
from pprint import pprint
from typing import (Callable, Literal, NewType, Type, TypeVar, Union,
                    get_type_hints)

from inflection import camelize
from sanic import Sanic
from sanic.response import json as jsonResponse
from sanic.websocket import WebSocketProtocol

BASE_DIR = path.dirname(path.dirname(path.abspath(__file__)))
sys.path.append(BASE_DIR)

from src.utils.Bots import *
from src.utils.Sender import Sender


app = Sanic("PepperBot")


handlers = defaultdict(list)
classHandlers = {
    "group": defaultdict(list),
    "groupCache": defaultdict(list)
}


# EventTypes = TypeVar("EventTypes")

RELATIONS = {
    "group": {
        "GroupMessage": [
            "GroupMessage",
            "GroupAnonymousMessage",
        ],
        "GroupNotice": [
            "GroupNotice",
            "GroupMessageBeenWithdraw",
            "MemberIncrease",
            "MemberDecline",
            "uploadNewFIle",
            "adminChange",
            "banChange",
            "GroupPokeYou",
        ],
        "GroupRequest": [
            "AddGroup",
            "BeenInvited"
        ]
    },
    "friend": [

        {
            "FriendMessage": [
                "FriendMessage",
            ],
            "FriendRequest":[
                "addFriend"
            ],
            "FriendNotice":[
                "FriendPokeYou"
                "FriendWithdraw",

            ]
        }
    ],
    "temp": [
        "TempMessage"

    ]
}


def get_parent_level(bottomGroupEvent: str):
    for key, value in RELATIONS['group'].items():
        if bottomGroupEvent in value:
            return key

    raise Exception("无效事件")


GROUP_EVENTS: List[str] = []

for _type, subTypes in RELATIONS["group"].items():
    GROUP_EVENTS.extend(subTypes)

GROUP_EVENTS_WITH_LIFECYCLE = [
    *GROUP_EVENTS
]
for event in GROUP_EVENTS:
    GROUP_EVENTS_WITH_LIFECYCLE.append("Before" + event)
    GROUP_EVENTS_WITH_LIFECYCLE.append("After" + event)


def is_group_event(event: str) -> bool:
    return event in GROUP_EVENTS


def is_valid_group_method(methodName: str):

    camelMethodName = camelize(methodName)
    return camelMethodName in GROUP_EVENTS_WITH_LIFECYCLE


def figure_out(receive: dict):
    finalType: Union[str, None] = ""

    post_type = receive["post_type"]

    if post_type == "meta_event":
        finalType = "MetaEvent"

    if post_type == "request":
        request_type = receive['request_type']
        sub_type = receive['sub_type']

        if(request_type == "group"):
            if sub_type == "add":
                print("加群请求")
                finalType = "AddGroup"

            elif sub_type == "invite":
                print("机器人被邀请入群")
                finalType = "BeenInvited"

    if post_type == "notice":
        notice_type = receive['notice_type']
        sub_type = receive['sub_type']

        if(notice_type == "group_increase"):
            print("新成员入群")
            finalType = "MemberAdded"

    if post_type == "message":
        message_type = receive['message_type']
        sub_type = receive['sub_type']

        if(message_type == "private"):

            if sub_type == "friend":
                print("好友私聊消息")
                finalType = "FriendMessage"

            elif sub_type == "group":
                # todo 临时会话可能获取不到groupId
                print("群临时会话")
                finalType = "TempMessage"

        elif message_type == "group":

            if sub_type == "normal":
                print("群普通消息")
                finalType = "GroupMessage"

            elif sub_type == "anonymous":
                print("群匿名消息")
                finalType = "GroupAnonymousMessage"

            elif sub_type == "notice":
                print("群通知消息")
                finalType = "GroupNotice"

    return finalType


def construct_api(ws):
    async def api(route: str, **kwargs):
        await ws.send(json.dumps({
            "action": route,
            "params": {
                **kwargs
            },
        }))

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


def register(groupId: int, *args, **kwargs):
    def decorator(handler: object):
        if isclass(handler):
            classHandlers['group'][groupId].append({
                "class": handler,
                "args": [*args],
                **kwargs
            })

        else:
            print("应为class")

    return decorator


def on(eventType, *args, **kwargs):
    def decorator(handler: Union[Callable[[], None], object]):

        if isfunction(handler):
            handlers[eventType].append(handler)

    return decorator


@on("metaEvent")
async def handle(*args):
    # print(args)
    print("in meta")


def __cache(ws):
    _cache = classHandlers["groupCache"]

    for groupId, handlers in classHandlers["group"].items():
        for handler in handlers:
            buffer = {
                "botInstance": None,
                'methods': defaultdict(list)
            }

            #  不要每次都创建实例，on监听器新增时建立一次，之后都保存起来即可
            # todo 嵌套字典的类型提示，可能要用到data class
            buffer['instance'] = _instance = handler['class']()
            buffer['botInstance'] = construct_bot(ws, groupId)

            # 初始化时，遍历生成缓存，不要每次接收到消息都去遍历
            for methodName in dir(_instance):

                methodOrProperty = getattr(_instance, methodName)

                if callable(methodOrProperty):
                    if not methodName.startswith("__"):
                        if is_valid_group_method(methodName):
                            buffer['methods'][camelize(methodName)].append(methodOrProperty)

            _cache[groupId].append(buffer)


def __output_config():
    pprint(classHandlers)


hasInitial = False
{'data': {'message_id': -1046833221}, 'retcode': 0, 'status': 'ok'}


@app.websocket('/cqhttp/ws')
async def main_entry(request, ws):
    global hasInitial

    if not hasInitial:
        __cache(ws)
        __output_config()
        hasInitial = True

    while True:

        try:

            print("*" * 50)
            data = await ws.recv()
            receive = json.loads(data)

            finalEvent = None
            try:
                finalEvent = figure_out(receive)
            except KeyError:
                pprint(receive)

            if finalEvent:
                if finalEvent == "MetaEvent":
                    print(receive['time'])
                else:
                    pprint(receive)

                # hooks
                for handler in handlers[finalEvent]:
                    await handler(receive)

                # group class
                if is_group_event(finalEvent):
                    groupId = receive['group_id']

                    for handler in classHandlers["groupCache"][groupId]:

                        # instance = handler['instance']
                        botInstance = handler['botInstance']

                        parentLevel = get_parent_level(finalEvent)
                        eventName = finalEvent

                        args = [botInstance]
                        if parentLevel == "GroupMessage":
                            chain = construct_chain(receive, groupId=groupId, ws=ws)
                            sender = construct_sender(receive, ws)
                            args.extend([chain, sender])

                        elif parentLevel == "GroupRequest":
                            args = [GroupRequestBot(api=construct_api(
                                ws), flag=receive['flag']), receive]

                        # 按照生命周期调用
                        for method in handler['methods']["Before" + eventName]:
                            await method(*args)

                        for method in handler['methods'][eventName]:
                            await method(*args)

                        for method in handler['methods']["After" + eventName]:
                            await method(*args)

            else:
                print("un register event")

        except Exception as e:
            print(e)


def run(host: str = "0.0.0.0", port: int = 8080, debug: bool = False):
    app.run(host, port, protocol=WebSocketProtocol, debug=debug)
