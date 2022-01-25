from typing import Any, Callable, Iterable, Literal, Optional, Type

from devtools import debug
from sanic import Sanic

from pepperbot.adapters.keaimao import KeaimaoAdapter
from pepperbot.adapters.onebot import OnebotV11Adapter
from pepperbot.core.bot.api_caller import ApiCaller
from pepperbot.core.event.base import AdapaterBase
from pepperbot.core.route.utils import (
    create_bot_routes,
    create_web_routes,
    http_receiver,
    websocket_receiver,
)
from pepperbot.exceptions import InitializationError
from pepperbot.extensions.logger import logger
from pepperbot.extensions.scheduler import async_scheduler
from pepperbot.store.meta import (
    DEFAULT_URI,
    AdapterBuffer,
    BotRoute,
    api_callers,
    clean_bot_instances,
    register_routes,
    route_mapping,
)
from pepperbot.types import API_Caller_T, T_BotProtocol, T_WebProtocol

sanic_app = Sanic("PepperBot")

sanic_app.config.WEBSOCKET_PING_TIMEOUT = None  # type:ignore

T_ApiCaller = API_Caller_T


class PepperBot:
    adapters = {}

    def __init__(
        self,
        host: str = "0.0.0.0",
        port: int = 8080,
        debug: bool = False,
    ):
        self.host = host
        self.port = port
        self.debug = debug

    def register_adapter(
        self,
        bot_protocol: T_BotProtocol,
        receive_protocol: T_WebProtocol,
        backend_protocol: T_WebProtocol,
        backend_port: int,
        backend_host="127.0.0.1",
        receive_uri: str = None,
    ):
        adapter: AdapaterBase
        api_caller: ApiCaller
        uri: str
        request_handler: Optional[Callable] = None

        if bot_protocol == "onebot":
            adapter = OnebotV11Adapter()
        elif bot_protocol == "keaimao":
            adapter = KeaimaoAdapter()
        else:
            raise InitializationError(f"尚不支持的机器人协议 {bot_protocol}")

        if receive_uri:
            uri = receive_uri
        else:
            if receive_protocol == "http":
                request_handler = lambda request: http_receiver(
                    request, bot_protocol, adapter
                )
                uri = DEFAULT_URI[bot_protocol] + "/http"

            elif receive_protocol == "websocket":
                request_handler = lambda request, ws: websocket_receiver(
                    request, ws, bot_protocol, adapter
                )
                # request_handler = websocket_receiver
                uri = DEFAULT_URI[bot_protocol] + "/ws"

            else:
                raise InitializationError(f"未知通信协议 {receive_protocol}")

        if backend_protocol == "http":
            api_caller = ApiCaller(
                bot_protocol=bot_protocol,
                backend_protocol="http",
                backend_port=backend_port,
                backend_host=backend_host,
            )
        elif backend_protocol == "websocket":
            raise InitializationError(f"backend_protocol尚不支持ws")
        else:
            raise InitializationError(f"未知通信协议 {backend_protocol}")

        api_callers[bot_protocol] = api_caller

        create_web_routes(
            sanic_app,
            AdapterBuffer(
                receive_protocol=receive_protocol,
                uri=uri,
                request_handler=request_handler,
            ),
        )

    def register_plugin(self):
        pass

    def apply_routes(self, routes: Iterable[BotRoute]):
        create_bot_routes([*routes, *register_routes])

    @staticmethod
    def initialize_scheduler(*args):
        # async_scheduler.add_job(check_command_timeout)
        # async_scheduler.add_job(clean_bot_instances)
        async_scheduler.start()

    def run(self):
        sanic_app.register_listener(
            PepperBot.initialize_scheduler, "before_server_start"
        )

        debug(route_mapping)
        debug(sanic_app._future_routes)

        try:
            sanic_app.run(self.host, self.port, debug=self.debug)
        except (KeyboardInterrupt, SystemExit):
            logger.success("PepperBot成功退出")


# 一个轻量级的跨平台机器人框架，轻松地在平台间传递消息
# A lightweight cross-platform bot framework, write once, run everywhere