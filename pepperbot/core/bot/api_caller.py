import httpx
from pepperbot.config import global_config
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

    def to_onebot(self, action: str, kwargs):
        # todo 直接返回.data
        return self.client.post(f"http://{self.host}:{self.port}/{action}", json=kwargs)

    def to_keaimao(self, action: str, kwargs):
        kwargs["event"] = action

        debug(kwargs)

        return self.client.post(f"http://{self.host}:{self.port}", json=kwargs)

    async def __call__(self, action: str, **kwargs):
        return self.caller(action, kwargs)

    # def on_connect():
    # todo ws
    #     """ 支持ws协议调用 """
    #
