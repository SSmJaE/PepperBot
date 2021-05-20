from typing import Awaitable, Callable, Dict, Protocol, Union

from src.message.chain import *

# protocol可以提供类型检查，但是pylance报错


class ApiProptocal(Protocol):
    @property
    def api(self) -> Any:
        ...


class EventProptocal(Protocol):
    @property
    def event(self) -> Dict[str, Any]:
        ...


class ApiEventProptocal(ApiProptocal, EventProptocal):
    pass


class ApiGroupIdProptocal(ApiProptocal):
    @property
    def groupId(self) -> int:
        ...


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

    pass


class GroupMessageMixin:
    api: API_Caller_T
    groupId: int

    async def group_msg(self, *chain: SegmentInstance_T):
        await self.api(
            "send_group_msg",
            **{
                "group_id": self.groupId,
                "message": [segment.formatted for segment in chain],
            }
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
            }
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
            }
        )


class AddGroupMixin:
    api: API_Caller_T
    flag: str

    async def resolve(self):
        await self.api(
            "set_group_add_request",
            **{"flag": self.flag, "type": "add", "approve": True}
        )

    async def reject(self, reason: str = ""):
        await self.api(
            "set_group_add_request",
            **{"flag": self.flag, "type": "add", "approve": False, "reason": reason}
        )
