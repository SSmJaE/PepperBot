import json
import time
import traceback
from inspect import isclass, isfunction
from typing import Callable, Union

import pretty_errors
from devtools import debug, pprint
from sanic import Sanic
from sanic.websocket import WebSocketProtocol
from pepperbot.action.chain import *
from pepperbot.command.handle import handle_command
from pepperbot.exceptions import EventHandlerDefineError
from pepperbot.globals import *
from pepperbot.parse import GROUP_EVENTS_T, GroupEvent, is_friend_event, is_group_event
from pepperbot.parse.bots import *
from pepperbot.parse.cache import cache
from pepperbot.parse.figure import figure_out
from pepperbot.parse.kwargs import DEFAULT_KWARGS, HANDLER_KWARGS_MAP, HandlerKwarg
from pepperbot.utils.common import (
    DisplayTree,
    await_or_normal,
    deepawait_or_normal,
    fit_kwargs,
    print_tree,
)

pretty_errors.configure(
    filename_display=pretty_errors.FILENAME_EXTENDED,
)


app = Sanic("PepperBot")


def register(
    groupId: Union[int, str, List[Union[int, str]]] = [],
    friendId="all",
    *args,
    **kwargs,
):
    def decorator(handler: Callable):
        if isclass(handler):
            decoratorMeta = GroupDecorator(
                **{
                    "args": [*args],
                    "kwargs": {**kwargs, "groupId": groupId, "friendId": friendId},
                }
            )

            classHandlers.groupMeta[handler].decorators["register"] = decoratorMeta
        else:
            raise EventHandlerDefineError("只允许使用register装饰器注册class")

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


def __output_config():

    debug(classHandlers)
    # debug(globalContext)

    result = []
    for groupId, groupCacheList in classHandlers.groupCache.items():
        buffer = []
        for groupCache in groupCacheList:
            buffer2 = []

            # todo 应该反过来，根据事件，列出订阅的classHandler，也要提升至group等级
            buffer2.append(
                DisplayTree(
                    name=f"事件",
                    node=[method for method in groupCache.methods.keys()],
                ),
            )

            # todo 提升至group等级，uniqueCommand
            buffer2.append(
                DisplayTree(
                    name=f"指令",
                    node=[
                        commandClass.__name__
                        for commandClass in groupCache.commandClasses
                    ]
                    or ["无"],
                ),
            )

            buffer.append(
                DisplayTree(
                    name=f"{groupCache.instance.__class__}",
                    node=[*buffer2],
                ),
            )

        groupTree = DisplayTree(name=f"群{groupId}", node=[*buffer])
        result.append(groupTree)

    print_tree(DisplayTree(name="PepperBot", node=result))


async def __check_command_timeout():
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
    pass


async def get_kwargs(eventName: GROUP_EVENTS_T, *_, **injectedKwargs):
    kwargList: List[HandlerKwarg] = HANDLER_KWARGS_MAP.get(eventName, DEFAULT_KWARGS)

    kwargs: Dict[str, Any] = {}
    for kwarg in kwargList:
        kwargs[kwarg.name] = await deepawait_or_normal(kwarg.value, **injectedKwargs)

    return kwargs


async def handle_qq_event(receive: Dict[str, Any], eventName: GROUP_EVENTS_T):

    if eventName == GroupEvent.meta_event:
        # print(
        #     arrow.get(receive["time"])
        #     .to("Asia/Shanghai")
        #     .format("YYYY-MM-DD HH:mm:ss"),
        #     "心跳",
        # )
        logger.info("心跳事件")

        __check_command_timeout

        # metaEvent = MetaEvent(**receive)
        # debug(metaEvent)
    else:
        pprint(receive)

    # function handler
    for handler in functionHandlers[eventName]:
        await handler(receive)

    # group handler
    if is_group_event(eventName):
        groupId = receive["group_id"]

        for handler in classHandlers.groupCache[groupId]:

            kwargs = await get_kwargs(eventName, event=receive, bot=handler.botInstance)

            # debug(kwargs)

            # 按照生命周期调用
            for method in handler.methods["before_" + eventName]:
                await await_or_normal(method, **fit_kwargs(method, kwargs))

            for method in handler.methods[eventName]:
                await await_or_normal(method, **fit_kwargs(method, kwargs))

            if eventName == GroupEvent.group_message:
                await handle_command(receive, kwargs, groupId, handler)

            for method in handler.methods["after_" + eventName]:
                await await_or_normal(method, **fit_kwargs(method, kwargs))

    elif is_friend_event(eventName):

        kwargs = await get_kwargs(eventName, event=receive)

        for handler in classHandlers.friendCache:
            for method in handler.methods["before_" + eventName]:
                await await_or_normal(method, **fit_kwargs(method, kwargs))

            for method in handler.methods[eventName]:
                await await_or_normal(method, **fit_kwargs(method, kwargs))

            # if eventName == GroupEvent.group_message:
            #     await handle_command(receive, kwargs, groupId, handler)

            for method in handler.methods["after_" + eventName]:
                await await_or_normal(method, **fit_kwargs(method, kwargs))

    elif eventName == GroupEvent.temp_message:

        kwargs = await get_kwargs(eventName, event=receive)

        for handler in classHandlers.tempCache:
            for method in handler.methods["before_" + eventName]:
                await await_or_normal(method, **fit_kwargs(method, kwargs))

            for method in handler.methods[eventName]:
                await await_or_normal(method, **fit_kwargs(method, kwargs))

            # if eventName == GroupEvent.group_message:
            #     await handle_command(receive, kwargs, groupId, handler)

            for method in handler.methods["after_" + eventName]:
                await await_or_normal(method, **fit_kwargs(method, kwargs))


hasInitial = False
hasSkipBuffer = False
bufferedMessageLength = 0


@app.websocket("/cqhttp/ws")
async def main_entry(request, ws):
    global hasInitial, hasSkipBuffer, bufferedMessageLength

    if not hasInitial:
        cache()
        __output_config()

        hasInitial = True

    while True:

        try:

            if hasSkipBuffer:
                print("*" * 50)
            data = await ws.recv()
            receive = json.loads(data)

            eventName: Optional[GROUP_EVENTS_T] = None
            try:
                eventName = figure_out(receive)
            except KeyError:
                logger.debug(receive)

            # debug(receive)

            if eventName:
                # 跳过缓存/过期的消息，根据心跳时间判断(比如离当前时间<5s)
                if not hasSkipBuffer:
                    if (
                        eventName == "meta_event"
                        and receive["meta_event_type"] == "lifecycle"
                    ):
                        continue

                    bufferedMessageLength += 1

                    currentTime = int(time.time())
                    eventTime: int = receive["time"]

                    if currentTime - eventTime < 10:
                        hasSkipBuffer = True
                        logger.success(f"已跳过{bufferedMessageLength}条缓存的事件")
                    else:
                        continue

                await handle_qq_event(receive, eventName)
            else:
                logger.warning("未注册的事件类型")
                logger.debug(receive)

        except Exception as e:
            print(e)
            print(traceback.format_exc())


@app.listener("before_server_start")
async def initialize_scheduler(app, loop):
    asyncScheduler.start()


def run(host: str = "0.0.0.0", port: int = 8080, debug: bool = False):
    try:
        app.run(host, port, protocol=WebSocketProtocol, debug=debug)
    except (KeyboardInterrupt, SystemExit):
        pass
