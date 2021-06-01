from .mixins import PrivateMessageMixin


from pepperbot.message.chain import *
from pepperbot.models.api import *


class ActionMixin:
    """
    主动行为的聚合，方便action使用
    """

    api: API_Caller_T

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

    async def stranger(
        self,
        userId: int,
    ):
        response = await self.api(
            "get_stranger_info",
            **{"user_id": userId, "no_cache": False},
        )

        member = get_stranger_info_return(**response.json()).data
        return member

    async def self_info(
        self,
    ):
        response = await self.api("get_login_info")

        return get_login_info(**response.json()).data
