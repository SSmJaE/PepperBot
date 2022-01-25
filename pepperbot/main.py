import json
import time
import traceback
from inspect import isclass, isfunction
from typing import Callable, Union

import pretty_errors
from devtools import debug, pprint
from sanic import Sanic
# from sanic.websocket import WebSocketProtocol
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







def on(eventType, *args, **kwargs):
    def decorator(handler: Union[Callable[[], None], object]):

        if isfunction(handler):
            functionHandlers[eventType].append(handler)

    return decorator


@on("metaEvent")
async def handle(*args):
    # print(args)
    print("in meta")








async def get_kwargs(eventName: GROUP_EVENTS_T, *_, **injectedKwargs):
    kwargList: List[HandlerKwarg] = HANDLER_KWARGS_MAP.get(eventName, DEFAULT_KWARGS)

    kwargs: Dict[str, Any] = {}
    for kwarg in kwargList:
        kwargs[kwarg.name] = await deepawait_or_normal(kwarg.value, **injectedKwargs)

    return kwargs




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




    


