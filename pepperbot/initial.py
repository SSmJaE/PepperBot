from typing import Any, Callable, Coroutine, Iterable, Literal, Optional, Type

from apscheduler.triggers.interval import IntervalTrigger
from devtools import debug, pformat
from sanic import Sanic

from pepperbot.adapters.telegram import register_telegram_event
from pepperbot.config import global_config
from pepperbot.core.bot.api_caller import ApiCaller
from pepperbot.core.route.utils import (
    create_bot_routes,
    create_web_routes,
    http_receiver,
    websocket_receiver,
)
from pepperbot.exceptions import InitializationError
from pepperbot.extensions.command.handle import check_command_timeout
from pepperbot.extensions.log import logger
from pepperbot.extensions.scheduler import async_scheduler
from pepperbot.store.meta import (
    ALL_AVAILABLE_BOT_PROTOCOLS,
    DEFAULT_URI,
    BotRoute,
    api_callers,
    clean_bot_instances,
    get_telegram_caller,
    output_config,
    register_routes,
    route_mapping,
)
from pepperbot.types import T_BotProtocol, T_WebProtocol

sanic_app = Sanic("PepperBot")
sanic_app.config.WEBSOCKET_PING_TIMEOUT = None  # type:ignore


async_create_telegram_handler: Optional[Callable] = None


class PepperBot:
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
        bot_protocol: Literal["onebot", "keaimao"],
        receive_protocol: T_WebProtocol,
        backend_protocol: T_WebProtocol,
        backend_port: int,
        backend_host="127.0.0.1",
        receive_uri: str = "",
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

    def register_telegram(self, *args, **kwargs):
        # sanic启动至少需要一个route，虽然这个route并不会被调用
        create_web_routes(
            sanic_app,
            receive_protocol="http",
            uri="/telegram/http",
            request_handler=lambda request: 1,
        )

        async def create_client_under_async_context():
            """
            pyrogram client require to be created under same async context
            for the reason that it interacts with sqlite

            unnecessarily to invoke `idle()` as we have sanic
            """
            from pyrogram.client import Client

            pyrogram_client = Client(*args, **kwargs)
            api_callers["telegram"] = pyrogram_client

            register_telegram_event(pyrogram_client)

            logger.success("Client created")

            await pyrogram_client.start()

        global async_create_telegram_handler
        async_create_telegram_handler = create_client_under_async_context

    def register_plugin(self):
        pass

    def apply_routes(self, routes: Iterable[BotRoute]):
        create_bot_routes([*routes, *register_routes])

    def share_state_command(self):
        pass

    @staticmethod
    async def before_server_start(*args):
        logger.success(f"successfully load .env config \n {pformat(global_config)}")

        logger.success(f"successfully create bot routes")
        output_config()

        if async_create_telegram_handler:
            async_scheduler.add_job(async_create_telegram_handler)

        async_scheduler.add_job(check_command_timeout, IntervalTrigger(seconds=10))
        # async_scheduler.add_job(clean_bot_instances)
        async_scheduler.start()

    def run(self):
        sanic_app.register_listener(
            PepperBot.before_server_start, "before_server_start"
        )

        try:
            sanic_app.run(self.host, self.port, debug=self.debug)
        except (KeyboardInterrupt, SystemExit):
            logger.info("PepperBot成功退出")
        # except:
        #     logger.exception("")
