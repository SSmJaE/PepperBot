from typing import Awaitable, Callable, Dict, Protocol, Union

from pepperbot.message.chain import *
from pepperbot.models.api import *


# protocol可以提供类型检查，但是pylance报错
# class ApiProptocal(Protocol):
#     @property
#     def api(self) -> Any:
#         ...


# class EventProptocal(Protocol):
#     @property
#     def event(self) -> Dict[str, Any]:
#         ...


# class ApiEventProptocal(ApiProptocal, EventProptocal):
#     pass


# class ApiGroupIdProptocal(ApiProptocal):
#     @property
#     def groupId(self) -> int:
#         ...


class GetGroupIdMixin:
    def __get_group_id(self):
        # try
        # kwargs.get("groupId")
        # try
        # self.event["group_id"]
        # self.groupId
        pass


class GetUserIdMixin:
    def __get_user_id(self):
        # self.groupId
        # self.event["group_id"]
        # kwargs.get("groupId")
        pass


class GroupMetaMixin:
    """发公告，修改群名等等"""

    pass


class GroupInfoMixin:
    """群文件，群相册等"""

    pass


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


class GroupMessageMixin:
    api: API_Caller_T
    groupId: Optional[int]

    async def group_msg(
        self, targetGroupId: Union[int, SegmentInstance_T], *chain: SegmentInstance_T
    ):
        if isinstance(targetGroupId, int):
            groupId = targetGroupId
            message = [segment.formatted for segment in chain]
        else:
            groupId = self.groupId
            message = [
                targetGroupId.formatted,
                *[segment.formatted for segment in chain],
            ]

        await self.api(
            "send_group_msg",
            **{
                "group_id": groupId,
                "message": message,
            },
        )

    def at_all(self):
        return {"type": "at", "data": {"qq": "all"}}


class GroupMemberMixin:
    api: API_Caller_T
    event: Dict[str, Any]

    async def ban(self, duration: int = 30):
        await self.api(
            "set_group_ban",
            **{
                "group_id": self.event["group_id"],
                "user_id": self.event["user_id"],
                "duration": duration * 60,
            },
        )

    # async def un_ban(self, duration: int = 30):
    #     await self.bot.call_api("set_group_ban", **{
    #         "group_id": self.groupId,
    #         "user_id": self.userId,
    #         "duration": duration * 60
    #     })

    async def kickout(self, permenant: bool = False):
        await self.api(
            "set_group_kick",
            **{
                "group_id": self.event["group_id"],
                "user_id": self.event["user_id"],
                "reject_add_request": permenant,
            },
        )


class AddGroupMixin:
    api: API_Caller_T
    flag: str

    async def resolve(self):
        await self.api(
            "set_group_add_request",
            **{"flag": self.flag, "type": "add", "approve": True},
        )

    async def reject(self, reason: str = ""):
        await self.api(
            "set_group_add_request",
            **{"flag": self.flag, "type": "add", "approve": False, "reason": reason},
        )
