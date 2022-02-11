from typing import Any, Callable, Iterable, Literal, Optional, Type

from devtools import debug, pformat
from sanic import Sanic

from pepperbot.core.bot.api_caller import ApiCaller
from pepperbot.core.route.utils import (
    create_bot_routes,
    create_web_routes,
    http_receiver,
    websocket_receiver,
)
from pepperbot.exceptions import InitializationError
from pepperbot.extensions.log import logger
from pepperbot.extensions.scheduler import async_scheduler
from pepperbot.store.meta import (
    ALL_AVAILABLE_BOT_PROTOCOLS,
    DEFAULT_URI,
    BotRoute,
    api_callers,
    clean_bot_instances,
    register_routes,
    route_mapping,
    output_config,
)
from pepperbot.types import T_BotProtocol, T_WebProtocol

sanic_app = Sanic("PepperBot")

sanic_app.config.WEBSOCKET_PING_TIMEOUT = None  # type:ignore


# async def async_initial_wrapper():
#     """ 在框架启动器只执行一次的异步任务 """
#     await initial_bot_info()


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
        uri: str
        request_handler: Optional[Callable] = None

        if bot_protocol not in ALL_AVAILABLE_BOT_PROTOCOLS:
            raise InitializationError(f"尚不支持的机器人协议 {bot_protocol}")

        if receive_uri:
            uri = receive_uri
        else:
            if receive_protocol == "http":
                request_handler = lambda request: http_receiver(request, bot_protocol)
                uri = DEFAULT_URI[bot_protocol] + "/http"

            elif receive_protocol == "websocket":
                request_handler = lambda request, ws: websocket_receiver(
                    request, ws, bot_protocol
                )
                uri = DEFAULT_URI[bot_protocol] + "/ws"

            else:
                raise InitializationError(f"未知通信协议 {receive_protocol}")

        create_web_routes(
            sanic_app,
            receive_protocol=receive_protocol,
            uri=uri,
            request_handler=request_handler,
        )

        api_caller: ApiCaller

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

    def register_plugin(self):
        pass

    def apply_routes(self, routes: Iterable[BotRoute]):
        create_bot_routes([*routes, *register_routes])

    def share_state_command(self):
        pass

    @staticmethod
    def before_server_start(*args):
        output_config()

        # async_scheduler.add_job(check_command_timeout)
        # async_scheduler.add_job(clean_bot_instances)
        async_scheduler.start()

    def run(self):
        sanic_app.register_listener(
            PepperBot.before_server_start, "before_server_start"
        )

        # logger.debug(pformat(route_mapping))
        # logger.debug(pformat(sanic_app._future_routes))

        # try:
        #     raise InitializationError(f"测试")
        # except:
        #     logger.exception("捕获")

        try:
            sanic_app.run(self.host, self.port, debug=self.debug)
        except (KeyboardInterrupt, SystemExit):
            logger.info("PepperBot成功退出")
        # except:
        #     logger.exception("")
