import json
from src.exceptions import EventHandlerDefineError
import traceback
from inspect import isclass, isfunction
from typing import Callable, Union

import pretty_errors
from devtools import debug, pprint
import time
from sanic import Sanic
from sanic.websocket import WebSocketProtocol

from src.action.main import *
from src.command.handle import handle_command
from src.globals import *
from src.parse import GROUP_EVENTS_T, GroupEvent, is_group_event
from src.parse.bots import *
from src.parse.cache import cache
from src.parse.figure import figure_out
from src.parse.kwargs import DEFAULT_KWARGS, HANDLER_KWARGS_MAP, HandlerKwarg
from src.utils.common import await_or_normal, deepawait_or_normal, fit_kwargs

pretty_errors.configure(
    filename_display=pretty_errors.FILENAME_EXTENDED,
)


app = Sanic("PepperBot")


# GroupIdInstanceMap = {}


# def get_instance(groupId):
#     instance = GroupIdInstanceMap.get(groupId)
#     if instance:
#         return instance
#     else:
#         pass


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


def __skip_buffer():
    pass


# myDebug = Debug(highlight=True)


def __output_config():
    debug(classHandlers)
    debug(globalContext)
    # pprint(classHandlers)
    # pprint(globalContext)


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

            kwargList: List[HandlerKwarg] = HANDLER_KWARGS_MAP.get(
                eventName, DEFAULT_KWARGS
            )

            kwargs: Dict[str, Any] = {}
            for kwarg in kwargList:
                kwargs[kwarg.name] = await deepawait_or_normal(
                    kwarg.value, event=receive, bot=handler.botInstance
                )

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


hasInitial = False
hasSkipBuffer = False
bufferedMessageLength = 0


@app.websocket("/cqhttp/ws")
async def main_entry(request, ws):
    global hasInitial, hasSkipBuffer, bufferedMessageLength

    if not hasInitial:
        cache()
        __output_config()

        # todo 跳过缓存/过期的消息，根据心跳时间判断(比如离当前时间<5s)
        __skip_buffer

        hasInitial = True

    while True:

        try:

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
                if not hasSkipBuffer:
                    if (
                        eventName == "meta_event"
                        and receive["meta_event_type"] == "lifecycle"
                    ):
                        continue

                    currentTime = int(time.time())
                    eventTime: int = receive["time"]

                    if currentTime - eventTime < 10:
                        hasSkipBuffer = True
                        logger.success(f"已跳过{bufferedMessageLength}条缓存的事件")

                    bufferedMessageLength += 1

                await handle_qq_event(receive, eventName)
            else:
                logger.warning("未注册的事件类型")
                logger.debug(receive)

        except Exception as e:
            print(e)
            print(traceback.format_exc())


def run(host: str = "0.0.0.0", port: int = 8080, debug: bool = False):
    app.run(host, port, protocol=WebSocketProtocol, debug=debug)
