from typing import Any, Callable, Coroutine, Iterable, Literal, Optional, Type, cast

from apscheduler.triggers.interval import IntervalTrigger
from devtools import debug, pformat
from sanic import Sanic

from pepperbot.adapters.telegram import register_telegram_event
from pepperbot.config import global_config
from pepperbot.core.api.api_caller import ApiCaller
from pepperbot.core.route.utils import (
    create_bot_routes,
    create_web_routes,
    http_receiver,
    websocket_receiver,
)
from pepperbot.exceptions import InitializationError
from pepperbot.extensions.command.handle import check_command_timeout
from pepperbot.extensions.log import debug_log, logger
from pepperbot.extensions.scheduler import async_scheduler
from pepperbot.store.orm import engine, metadata, set_metadata
from pepperbot.store.meta import (
    DEFAULT_URI,
    BotRoute,
    clean_bot_instances,
    output_config,
    api_callers,
    register_routes,
)
from pepperbot.types import BOT_PROTOCOLS, T_BotProtocol, T_WebProtocol

# from dotenv import load_dotenv
# import os

sanic_app = Sanic("PepperBot")

async_create_telegram_handler: Optional[Callable] = None


async def _ensure_async_scheduler_start():
    logger.success("PepperBot successfully start scheduler")


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

        sanic_app.config.INSPECTOR = debug
        sanic_app.config.WEBSOCKET_PING_TIMEOUT = None  # type:ignore

        sanic_app.register_listener(self.main_process_start, "main_process_start")
        sanic_app.register_listener(self.after_server_start, "after_server_start")

        # load_dotenv()  # take environment variables from .env.
        # debug_log(os.environ)

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

        if bot_protocol not in BOT_PROTOCOLS:
            raise InitializationError(f"尚不支持的机器人协议 {bot_protocol}")

        if receive_uri:
            uri = receive_uri
        else:
            if receive_protocol == "http":
                # TODO lambda重名问题，动态创建
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
        # sanic不允许重名的handler，lambda表达式会导致重名(都为lambda)
        async def telegram_handler(request):
            return 1

        create_web_routes(
            sanic_app,
            receive_protocol="http",
            uri="/telegram/http",
            request_handler=telegram_handler,
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

            logger.success("PepperBot successfully create pyrogram client")

            await pyrogram_client.start()

        global async_create_telegram_handler
        async_create_telegram_handler = create_client_under_async_context

    def register_plugin(self) -> None:
        pass

    def apply_routes(self, routes: Iterable[BotRoute]):
        create_bot_routes([*routes, *register_routes])

    def share_state_command(self):
        pass

    @staticmethod
    async def main_process_start(app, loop):
        """
        https://sanic.dev/en/guide/basics/listeners.html#asgi-mode

        If you are running your application with an ASGI server, main_process_start and main_process_stop will be ignored
        """

        # TODO 主动获取bot info
        await set_metadata("has_initial_bot_info", False)

        # TODO 在各adapter初始化完成之后，再获取
        # 所以需要实现一个hook，after_adapter_init

        # main process、worker process都需要读取.env
        # 主动读取一次，这样即使用户定义的BaseSetting中没有制定env_file，也能读取到
        # load_dotenv()  # take environment variables from .env.
        logger.success(
            f"PepperBot successfully load .env config \n {pformat(global_config)}"
        )

        logger.success(f"PepperBot successfully create bot routes")
        # output_config()
        # debug(per_worker)

        # 必须放到最后，等model都定义好了再执行
        # note that this has to be the same metadata that is used in ormar Models definition
        metadata.create_all(engine)
        # 保证过期(无效)的command status一定被清理，不会干扰has_running_command的判断
        await check_command_timeout()

    @staticmethod
    async def after_server_start(app, loop):
        # ensure that async_scheduler is created under same async context
        # https://github.com/sanic-org/sanic/issues/743
        # global async_scheduler
        # async_scheduler = AsyncIOScheduler({'event_loop': loop})

        # 正常情况下，主进程设置一次就行了
        # 但是如果自动重启，那么就需要在每次重启后都设置一次
        if app.config["AUTO_RELOAD"]:
            await set_metadata("has_initial_bot_info", False)

        if async_create_telegram_handler:
            async_scheduler.add_job(async_create_telegram_handler)

        async_scheduler.add_job(check_command_timeout, IntervalTrigger(seconds=10))
        # async_scheduler.add_job(clean_bot_instances)
        async_scheduler.add_job(_ensure_async_scheduler_start)

        async_scheduler.start()

    def run(self, **kwargs):
        """
        all available kwargs https://sanic.dev/en/guide/deployment/running.html#low-level-app-run

        bind event listener or other things before run sanic, and should not in same function with run

        otherwise, it will not work(because it only run on Sanic's main worker process, NOT any of its worker processes)
        """

        final_kwargs = dict(
            host=self.host,
            port=self.port,
            debug=self.debug,
            auto_reload=self.debug,
        )

        final_kwargs.update(kwargs)

        try:
            # by a separate dict, make sure that there wouldn't have two same kwargs
            sanic_app.run(**final_kwargs)
        except (KeyboardInterrupt, SystemExit):
            logger.info("PepperBot successfully shutdown")
        # except:
        #     logger.exception("")
