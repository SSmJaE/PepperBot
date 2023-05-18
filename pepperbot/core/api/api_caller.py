from typing import Any, Dict
import httpx
from pepperbot.config import global_config
from pepperbot.exceptions import BackendApiError, InitializationError
from pepperbot.extensions.log import debug_log, logger
from pepperbot.types import T_BotProtocol, T_WebProtocol
from devtools import debug


class ApiCaller:
    """访问后端"""

    def __init__(
        self,
        bot_protocol: T_BotProtocol,
        backend_protocol: T_WebProtocol,
        backend_port: int,
        backend_host: str = "127.0.0.1",
    ):
        if bot_protocol == "onebot":
            self.caller = self.to_onebot

        elif bot_protocol == "keaimao":
            self.caller = self.to_keaimao

        else:
            raise InitializationError()

        self.protocol = backend_protocol
        self.host = backend_host
        self.port = backend_port

        # todo proxy
        # global_config.Debug.proxy

        self.client = httpx.Client()
        # self.client = httpx.Client(**kwargs)
        # self.client = httpx.AsyncClient(**kwargs)

    def __del__(self):
        # 注销client

        self.client.close()

        # todo 没有找到在del中调用AsyncClient.aclose的方法
        # self.client.aclose().__await__()

    def to_onebot(
        self, action: str, kwargs: dict = {}, *, direct=True
    ) -> Dict[str, Any]:
        """direct时，直接返回["data"]"""

        # debug_log(kwargs)
        httpx_result = self.client.post(
            f"http://{self.host}:{self.port}/{action}",
            json=kwargs,
        )

        try:
            httpx_result_json = httpx_result.json()

            if httpx_result_json["status"] == "failed":
                BackendApiError(
                    f"{httpx_result_json['msg']} {httpx_result_json['wording']}"
                )

            debug_log(httpx_result_json)

            if direct:
                return httpx_result_json["data"]
            else:
                return httpx_result_json

        except BackendApiError as exception:
            logger.exception(exception)
            raise exception

        except Exception as exception:
            logger.exception("无法序列化协议端返回的数据，请检查是否正确配置了对应的ip、端口、协议")
            raise exception

    def to_keaimao(self, action: str, kwargs={}) -> Dict[str, Any]:
        kwargs["event"] = action

        debug(kwargs)

        return self.client.post(f"http://{self.host}:{self.port}", json=kwargs).json()

    async def __call__(self, action: str, **kwargs):
        return self.caller(action, kwargs)

    call = __call__

    # def on_connect():
    # todo ws
    #     """ 支持ws协议调用 """
    #
