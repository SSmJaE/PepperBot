import asyncio
from typing import Optional

import httpx
from pepperbot.utils.mixins import *


class APICaller(GroupMessageMixin, ActionMixin):
    def __init__(
        self,
        host: str = "localhost",
        port: int = 8080,
        proxies: Optional[httpx.Proxy] = None,
    ):
        self.host = host
        self.port = port

        kwargs = {}
        if proxies:
            kwargs["proxies"] = proxies

        self.client = httpx.AsyncClient(**kwargs)

        # try:
        #     self.client = httpx.AsyncClient(proxies=proxies)
        #     yield None
        # finally:
        #     await self.client.aclose()

    def __del__(self):
        # todo 销毁时，注销client，似乎有点多此一举？
        # try:
        #     loop = asyncio.get_event_loop()
        #     loop.run_until_complete(self.client.aclose())
        # except:
        #     pass
        # asyncio.run(self.client.aclose())
        pass

    async def api(self, action: str, **kwargs):
        return await self.client.post(
            f"http://{self.host}:{self.port}/{action}", json=kwargs
        )
