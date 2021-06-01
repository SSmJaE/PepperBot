import asyncio
from typing import Optional

import httpx
from pepperbot.utils.mixins import *
from pepperbot.utils.action import *


class APICaller(GroupMessageMixin, ActionMixin):
    def __init__(
        self,
        host: str = "localhost",
        port: int = 8080,
        proxies: Optional[Any] = None,
    ):
        self.host = host
        self.port = port

        kwargs = {}
        if proxies:
            kwargs["proxies"] = proxies

        self.client = httpx.Client(**kwargs)
        # self.client = httpx.AsyncClient(**kwargs)

    def __del__(self):
        # 注销client

        self.client.close()

        # todo 没有找到在del中调用AsyncClient.aclose的方法
        # self.client.aclose().__await__()

    async def api(self, action: str, **kwargs):
        return self.client.post(f"http://{self.host}:{self.port}/{action}", json=kwargs)

        # todo 直接返回.data
        # 可以手动指定后端是go-cqhttp，方便与其它后端兼容
