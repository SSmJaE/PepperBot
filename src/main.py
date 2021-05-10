import sys
import time
from os import path

BASE_DIR = path.dirname(path.dirname(path.abspath(__file__)))
sys.path.append(BASE_DIR)

import json
import traceback
from collections import defaultdict
from functools import wraps
from inspect import isawaitable, isclass, iscoroutine, isfunction
from pprint import pprint
from typing import Callable, Literal, NewType, Optional, Type, TypeVar, Union

import arrow
from devtools import debug
from inflection import camelize
from pydantic import BaseModel
from sanic import Sanic
from sanic.websocket import WebSocketProtocol

from src.Action.main import *
from src.Bots.Bots import *
from src.Events import GroupIncrease, MetaEvent
from src.Exceptions import (
    CommandClassDefineException,
    CommandClassOnExit,
    CommandClassOnFinish,
    CommandClassOnTimeout,
)
from src.Parse import GROUP_EVENTS_T, RELATIONS, GroupEvent
from src.Parse.figure import figure_out
from src.User.Sender import Sender
from src.utils.common import await_or_normal, get_own_methods

app = Sanic("PepperBot")

CLASS_ID_MAP: Dict[Any, Any] = {}

ClassId_T = Any


class CommandClassBase:
    pass


class UserMessage(BaseModel):
    messageId: int
    message: List[SegmentInstance_T]
    createTime: int
    groupId: int
    userId: int

    class Config:
        arbitrary_types_allowed = True


class NormalContext(BaseModel):
    """
    默认不收录消息，除非触发了指令，减少内存占用
    """

    messageQueue: List[UserMessage] = []
    commandStatus: str = "initial"
    userContext: Dict = {}


class CommandContext(BaseModel):
    """
    如果相同的一条指令，需要为某些用户跨群，某些不跨群，应该怎么操作？
    复制一份，一个全局permission，另一个提供permission方法，实现动态用户黑名单/白名单
    """

    # todo 如果未提供，使用全局设置
    # 通过as_command的kwargs指定
    maxSize: int
    timeout: int

    """
    - normal        same user same group
    - crossUser     cross user same group 
    - crossGroup    same user cross group
    - global        cross user cross group
    """
    mode: Literal["normal", "crossUser", "crossGroup", "global"] = "normal"

    # 如果是normal指令，需要为一个用户在每个群都保存一个消息队列和指令进度
    # 第一个key为QQ号，第二个key为群号
    normalContextMap: Dict[int, Dict[int, NormalContext]] = defaultdict(dict)

    # crossGroup
    crossGroupMessageQueue: List[UserMessage] = []
    # key为qq号
    # 对于当前用户，他的指令执行到哪一步了
    crossGroupUserStatus: Dict[int, NormalContext] = defaultdict(NormalContext)

    # crossUser
    crossUserMessageQueue: List[UserMessage] = []
    # key为群号
    crossUserCommandStatus: Dict[int, NormalContext] = defaultdict(NormalContext)

    # global
    globalMessageQueue: List[UserMessage] = []
    globalCommandStatus: str = "initial"
    globalContext: Dict = {}


# todo 多个命令，一致前缀，都执行？
class Context(BaseModel):
    """
    context主要是为一个用户和各个commandClass的交互服务

    以用户或者commandClass为key都可以，不过用户的数量可能要比命令多得多

    所以以命令类为key
    """

    # todo 相同commandClass，不同permission的处理
    cache: Dict[ClassId_T, CommandContext] = {}
    # 全局默认栈深
    maxSize: int = 10
    # 全局默认消息过期时间，单位秒
    timeout: int = 2 * 60 * 60

    class Config:
        arbitrary_types_allowed = True


# todo 提供统一的api，允许用户设置各种全局变量的默认值
globalContext = Context()


class CommandCache(BaseModel):
    instance: Union[Callable, Any]
    # key为方法名，value为实例化后的方法
    methods: Dict[str, Union[Callable, Any]] = {}
    kwargs: Dict[str, Any]
    targetMethod: str = "initial"


class GroupDecorator(BaseModel):
    args: List[Any] = []
    kwargs: Dict[str, Any] = {}


class GroupMeta(BaseModel):
    """
    收集通过各种装饰器注册的基于class的事件响应handler
    """

    # class_: Callable
    decorators: Dict[str, GroupDecorator] = {}


class GroupCache(BaseModel):
    """
    根据GroupMeta生成缓存，保存实例化的class之类
    """

    botInstance: BotBase
    instance: Union[Callable, Any]

    # bounded methods
    # methods: Dict[GROUP_EVENTS_T, List[Any]] = defaultdict(list)
    methods: Dict[str, List[Any]] = defaultdict(list)
    commandClasses: Dict[ClassId_T, CommandCache] = {}

    class Config:
        arbitrary_types_allowed = True


class ClassHandler(BaseModel):
    # key为class handler
    groupMeta: Dict[Callable, GroupMeta] = defaultdict(GroupMeta)
    # key为群号
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


# groupHandler可能有多个装饰器，比如register, withCommand
# 先解析为与装饰器名称相关的缓存至groupMeta，
# 解析完所有装饰器之后，再生成classHandlers.groupCache中的缓存
# 生成缓存时，确保register的存在，不然报错(withCommand也可以向group中推送meta信息)
# 这才是真正的meta，全局保存class和对应的meta，而不是绑定到class上，可能会涉及到bound和unbound的问题


def register(groupId: Union[int, str, List[Union[int, str]]], *args, **kwargs):
    def decorator(handler: Callable):
        if isclass(handler):
            decoratorMeta = GroupDecorator(
                **{"args": [*args], "kwargs": {**kwargs, "groupId": groupId}}
            )

            classHandlers.groupMeta[handler].decorators["register"] = decoratorMeta
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

    for handlerClass, classMeta in classHandlers.groupMeta.items():

        #  不要每次都创建实例，on监听器新增时建立一次，之后都保存起来即可
        _instance = handlerClass()

        decoratorNames = list(classMeta.decorators.keys())
        if "register" not in decoratorNames:
            raise Exception("基于class的事件响应处理器必须通过register装饰器注册")

        decoratorNames.remove("register")

        # 除register以外的class级装饰器
        commandClassesBuffer: Dict[ClassId_T, CommandCache] = {}

        for decoratorName in decoratorNames:
            argDict = classMeta.decorators[decoratorName]
            args = argDict.args
            kwargs = argDict.kwargs

            if decoratorName == "with_command":
                commandClasses = kwargs["commandClasses"]

                for commandClass in commandClasses:
                    commandInstance = commandClass()
                    commandKwargs: Dict = getattr(commandClass, "kwargs")

                    debug(commandKwargs)

                    commandBuffer = CommandCache(
                        instance=commandInstance, kwargs=commandKwargs
                    )

                    for method in get_own_methods(commandInstance):
                        commandBuffer.methods[method.__name__] = method

                    classId = random.random()
                    commandClassesBuffer[classId] = commandBuffer

                    mode = commandKwargs["mode"]

                    commandContext = CommandContext(
                        maxSize=globalContext.maxSize,
                        timeout=globalContext.timeout,
                        mode=mode,
                    )

                    CLASS_ID_MAP[classId] = commandClass

                    globalContext.cache[classId] = commandContext

        # 处理完所有其它装饰器后，最后处理register，建立groupId与classHandler的映射
        finalGroupIds: List[int] = []

        groupId = classMeta.decorators["register"].kwargs["groupId"]

        if isinstance(groupId, int):
            finalGroupIds.append(groupId)

        elif isinstance(groupId, str):
            finalGroupIds.append(int(groupId))

        elif isinstance(groupId, list):
            for id in groupId:
                finalGroupIds.append(int(id))

        for id in finalGroupIds:

            # todo 是否可以只实例化一次botInstance？动态注入groupId
            # 似乎每个群一个bot，效果更好一点
            groupCache = GroupCache(
                instance=_instance,
                botInstance=construct_bot(ws, id),
                commandClasses=commandClassesBuffer,
            )

            # 初始化时，遍历生成缓存，不要每次接收到消息都去遍历
            for method in get_own_methods(_instance):
                if is_valid_group_method(method.__name__):
                    groupCache.methods[camelize(method.__name__)].append(method)

                else:
                    print("无效的hook")
                    debug(method)

            _cache[id].append(groupCache)


def __output_config():
    debug(classHandlers)
    debug(globalContext)


async def __check_command_timeout():
    pass


def is_valid_request(chain: MessageChain, commandClassName: str, kwargs: Dict) -> bool:
    """
    通过commandClass的kwargs和messageChain的pure_text，判断是否触发命令的initial
    """
    # todo 是否需要@机器人
    # at: bool= commandCache.kwargs["at"]
    # if at:
    #     selfId=api.selfInfo
    #     if not chain.has(At(selfId)):
    #         continue

    needPrefix: bool = kwargs["needPrefix"]
    prefixes: List[str] = kwargs["prefix"]

    also: List[str] = kwargs["also"]
    includeClassName: bool = kwargs["includeClassName"]
    if includeClassName:
        if commandClassName not in also:
            also.append(commandClassName)

    debug(commandClassName)
    debug(prefixes)
    debug(also)

    isValidRequest = False
    for alias in also:
        if isValidRequest:
            break

        for prefix in prefixes if needPrefix else [""]:
            finalPrefix = prefix + alias
            if re.search(f"^{finalPrefix}", chain.pure_text):
                isValidRequest = True
                break

    debug(isValidRequest)
    return isValidRequest


def util_factory(
    commandContext: CommandContext,
    classId,
    groupId,
    userId,
):
    def update_command_status(status: str = "initial"):
        if commandContext.mode == "normal":
            globalContext.cache[classId].normalContextMap[userId][
                groupId
            ].commandStatus = status
        elif commandContext.mode == "crossGroup":
            globalContext.cache[classId].crossGroupUserStatus[
                userId
            ].commandStatus = status
        elif commandContext.mode == "crossUser":
            globalContext.cache[classId].crossUserCommandStatus[
                groupId
            ].commandStatus = status
        elif commandContext.mode == "global":
            globalContext.cache[classId].globalCommandStatus = status

    def process_messageQueue(
        messageQueue: List[UserMessage],
        receive: Dict,
        chain: MessageChain,
    ):
        if len(messageQueue) >= commandContext.maxSize:
            messageQueue.pop(0)

        newMessage = UserMessage(
            messageId=receive["message_id"],
            # todo unix
            createTime=round(time.time()),
            message=[*chain.chain],
            groupId=groupId,
            userId=userId
        )
        messageQueue.append(newMessage)

    return update_command_status, process_messageQueue


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
                        .format("YYYY-MM-DD HH:mm:ss"),
                        "心跳",
                    )

                    # metaEvent = MetaEvent(**receive)
                    # debug(metaEvent)
                else:
                    pprint(receive)

                # hooks
                for handler in functionHandlers[finalEvent]:
                    await handler(receive)

                # group class
                if is_group_event(finalEvent):
                    groupId = receive["group_id"]

                    for groupCacheIndex, handler in enumerate(
                        classHandlers.groupCache[groupId]
                    ):

                        # instance = handler['instance']
                        botInstance = handler.botInstance

                        parentLevel = get_parent_level(finalEvent)
                        eventName = finalEvent

                        kwargs: Dict[str, Union[BotBase, MessageChain, Sender, Any]] = {
                            "bot": botInstance
                        }

                        chain: Optional[MessageChain] = None
                        sender: Optional[Sender] = None
                        if parentLevel == "GroupMessage":
                            chain = construct_chain(receive, groupId=groupId, ws=ws)
                            kwargs["chain"] = chain
                            sender = construct_sender(receive, ws)
                            kwargs["sender"] = sender

                        elif parentLevel == "GroupRequest":
                            if finalEvent == GroupEvent.AddGroup:
                                kwargs = {
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

                                kwargs = {
                                    "bot": GroupNoticeBot(
                                        api=construct_api(ws),
                                        groupId=groupId,
                                    ),
                                    "event": receive,
                                    "member": member,
                                }

                            else:
                                kwargs = {
                                    "bot": GroupNoticeBot(
                                        api=construct_api(ws),
                                        groupId=groupId,
                                    ),
                                    "event": receive,
                                }

                        # 按照生命周期调用
                        for method in handler.methods["Before" + eventName]:
                            await method(**kwargs)

                        for method in handler.methods[eventName]:
                            await method(**kwargs)

                        if eventName == GroupEvent.GroupMessage:
                            # todo 命令的优先级，
                            # 命令需要优先级吗？
                            # 普通的group_message也有默认优先级，所以命令可以先于group_message执行，也可以后于

                            for classId, commandCache in handler.commandClasses.items():
                                commandContext = globalContext.cache[classId]
                                commandClass = CLASS_ID_MAP[classId]
                                commandClassName = commandClass.__name__

                                userId = cast(int, sender.user_id)
                                chain = cast(MessageChain, chain)

                                (
                                    update_command_status,
                                    process_messageQueue,
                                ) = util_factory(
                                    commandContext,
                                    classId,
                                    groupId,
                                    userId,
                                )

                                # 每一个用户一个指向，可以设置跨群还是不跨群
                                # 跨群就是使用一个指向，
                                # 不跨群，就是同一个用户，在不同群，有不同的指向
                                finalMessageQueue: List[UserMessage] = []
                                finalStatus: str = ""
                                finalContext: Optional[Dict] = None

                                if commandContext.mode == "normal":
                                    userGroupMap = commandContext.normalContextMap[
                                        userId
                                    ]

                                    normalContext = userGroupMap.get(groupId)
                                    if not normalContext:
                                        normalContext = NormalContext()
                                        userGroupMap[groupId] = normalContext

                                    finalContext = normalContext.userContext
                                    finalStatus = normalContext.commandStatus
                                    finalMessageQueue = normalContext.messageQueue

                                elif commandContext.mode == "crossGroup":
                                    status = commandContext.crossGroupUserStatus[userId]

                                    finalContext = status.userContext
                                    finalStatus = status.commandStatus
                                    finalMessageQueue = status.messageQueue

                                elif commandContext.mode == "crossUser":
                                    status = commandContext.crossUserCommandStatus[
                                        groupId
                                    ]

                                    finalContext = status.userContext
                                    finalStatus = status.commandStatus
                                    finalMessageQueue = status.messageQueue

                                elif commandContext.mode == "global":

                                    finalContext = commandContext.globalContext
                                    finalStatus = commandContext.globalCommandStatus
                                    finalMessageQueue = (
                                        commandContext.globalMessageQueue
                                    )

                                debug(finalContext)
                                debug(finalStatus)
                                debug(finalMessageQueue)
                                # debug(globalContext)

                                collectMessageFlag = False
                                if finalStatus == "initial":

                                    # 判断是否触发命令前缀
                                    isValidRequest = is_valid_request(
                                        chain, commandClassName, commandCache.kwargs
                                    )

                                    if isValidRequest:
                                        collectMessageFlag = True
                                    else:
                                        continue

                                else:
                                    collectMessageFlag = True

                                if collectMessageFlag:
                                    process_messageQueue(
                                        finalMessageQueue,
                                        receive,
                                        chain,
                                    )

                                # 当前指向的方法，或者说，当前激活的命令回调方法
                                targetMethod = commandCache.methods[finalStatus]
                                methodNames = commandCache.methods.keys()

                                # 判断是否正常退出
                                try:
                                    # todo 对所有事件的回调，都判断是否awaitable

                                    if finalStatus != "initial":
                                        # todo 超时判断应该每次心跳都判断，而不是接收到该用户消息时
                                        # 超时判断，与上一条消息的createTime判断
                                        # timeout: Optional[int] = commandCache.kwargs[
                                        #     "timeout"
                                        # ]

                                        # if timeout:

                                        #     prevChain = finalMessageQueue[-2]
                                        #     currentChain = finalMessageQueue[-1]

                                        #     debug(
                                        #         prevChain.createTime
                                        #         - currentChain.createTime
                                        #     )
                                        #     debug(timeout)

                                        #     if (
                                        #         prevChain.createTime
                                        #         - currentChain.createTime
                                        #         >= timeout
                                        #     ):
                                        #         raise CommandClassOnTimeout()

                                        # 退出判断
                                        exitPatterns: List[str] = commandCache.kwargs[
                                            "exitPattern"
                                        ]

                                        debug(exitPatterns)
                                        for pattern in exitPatterns:
                                            debug(re.search(pattern, chain.pure_text))
                                            if re.search(pattern, chain.pure_text):
                                                raise CommandClassOnExit()

                                    # 参数和group_message事件参数一致
                                    result = await await_or_normal(
                                        targetMethod,
                                        **kwargs,
                                        context=finalContext,
                                        messageQueue=finalMessageQueue,
                                    )
                                    debug(result)

                                    # 流程正常退出
                                    if result == True or result == None:
                                        raise CommandClassOnFinish()
                                    else:

                                        if not (
                                            callable(result) or isawaitable(result)
                                        ):
                                            raise CommandClassDefineException(
                                                "未提供命令类中可继续执行的下一个方法"
                                            )

                                        if not result.__name__ in methodNames:
                                            raise CommandClassDefineException(
                                                "下一步方法，需要在命令类中定义过，不能是外部函数或方法"
                                            )

                                        # 设置下一次执行时要调用的方法
                                        update_command_status(result.__name__)

                                except CommandClassDefineException as e:
                                    debug(e)

                                except CommandClassOnFinish:  # 流程正常退出时执行，return True时

                                    update_command_status()

                                    if "finish" in methodNames:
                                        finishHandler = commandCache.methods["finish"]
                                        await await_or_normal(
                                            finishHandler,
                                            **kwargs,
                                            context=finalContext,
                                            messageQueue=finalMessageQueue,
                                        )

                                except CommandClassOnExit:  # 用户主动退出时执行

                                    update_command_status()

                                    if "exit" in methodNames:
                                        exitHandler = commandCache.methods["exit"]
                                        await await_or_normal(
                                            exitHandler,
                                            **kwargs,
                                            context=finalContext,
                                            messageQueue=finalMessageQueue,
                                        )

                                except CommandClassOnTimeout:  # 用户响应超时时执行

                                    update_command_status()

                                    if "timeout" in methodNames:
                                        timeoutHandler = commandCache.methods["timeout"]
                                        await await_or_normal(
                                            timeoutHandler,
                                            **kwargs,
                                            context=finalContext,
                                            messageQueue=finalMessageQueue,
                                        )

                                except Exception as e:
                                    update_command_status()

                                    if "error" in methodNames:  # 用户定义的异常捕获方法
                                        errorHandler = commandCache.methods["error"]
                                        await await_or_normal(
                                            errorHandler,
                                            **kwargs,
                                            error=e,
                                            context=finalContext,
                                            messageQueue=finalMessageQueue,
                                        )

                                    else:
                                        raise e

                        for method in handler.methods["After" + eventName]:
                            await method(**kwargs)

            else:
                print("未注册的事件类型")

        except Exception as e:
            print(e)
            print(traceback.format_exc())


def run(host: str = "0.0.0.0", port: int = 8080, debug: bool = False):
    app.run(host, port, protocol=WebSocketProtocol, debug=debug)
