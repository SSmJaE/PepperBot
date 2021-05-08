import asyncio
from src.Models.api import get_group_member_info_return

import httpx
from src.main import *
from typing import Optional
from src.Message.MessageChain import SegmentInstance_T


class APICaller:
    def __init__(
        self,
        host: str = "localhost",
        port: int = 8080,
        proxies: Optional[httpx.Proxy] = None,
    ):
        self.host = host
        self.port = port

        self.client = httpx.AsyncClient(proxies=proxies)

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

    async def group_msg(self, groupId: int, *messageChains: SegmentInstance_T):
        await self.api(
            "send_group_msg",
            **{
                "group_id": groupId,
                "message": [segment.formatted for segment in messageChains],
            },
        )

    async def members(
        self,
        groupId: int,
    ):
        return await self.api(
            "get_group_member_list",
            **{
                "group_id": groupId,
            },
        )

    async def member(
        self,
        groupId: int,
        userId: int,
    ):
        response = await self.api(
            "get_group_member_info",
            **{
                "group_id": groupId,
                "user_id": userId,
            },
        )

        member = get_group_member_info_return(**response.json()).data
        return member


# {
#     "action": route,
#     "params": {**kwargs},
# }


# def __
