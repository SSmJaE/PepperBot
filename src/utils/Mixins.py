from typing import Dict, Protocol, Union

from src.utils.MessageChain import *

# protocol可以提供类型检查，但是pylance报错


class ApiProptocal(Protocol):
    @property
    def api(self) -> Any: ...


class EventProptocal(Protocol):
    @property
    def event(self) -> Dict[str, Any]: ...


class ApiEventProptocal(ApiProptocal, EventProptocal):
    pass


class ApiGroupIdProptocal(ApiProptocal):
    @property
    def groupId(self) -> int: ...


class GroupMessageMixin:
    api: Any
    groupId: int

    async def group_msg(self, *chain: TypeOfSegmentInstance):
        await self.api("send_group_msg", **{
            "group_id": self.groupId,
            "message": [segment.formatted for segment in chain]
        })

    def at_all(self):
        return {
            "type": "at",
            "data": {
                "qq": "all"
            }
        }


class GroupMemberMixin:
    api: Any
    event: Dict[str, Any]

    async def ban(self, duration: int = 30):
        await self.api("set_group_ban", **{
            "group_id": self.event["group_id"],
            "user_id": self.event["user_id"],
            "duration": duration * 60
        })

    # async def un_ban(self, duration: int = 30):
    #     await self.bot.call_api("set_group_ban", **{
    #         "group_id": self.groupId,
    #         "user_id": self.userId,
    #         "duration": duration * 60
    #     })

    async def kickout(self, permenant: bool = False):
        await self.api("set_group_kick", **{
            "group_id": self.event["group_id"],
            "user_id": self.event["user_id"],
            "reject_add_request": permenant
        })


class GroupRequestMixin:
    api: Any
    flag: Any

    async def resolve(self):
        await self.api("set_group_add_request", **{
            "flag": self.flag,
            "type": "add",
            "approve": True
        })

    async def reject(self, reason: str = ""):
        await self.api("set_group_add_request", **{
            "flag": self.flag,
            "type": "add",
            "approve": False,
            "reason": reason
        })
