from typing import Awaitable, Callable, Dict, Protocol, Union

from pepperbot.message.chain import *

# from pepperbot.models.api import *


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


# todo 自动返回.data，适配器模式
class GroupFileMixin:
    api: API_Caller_T
    groupId: Optional[int]

    async def upload_file(self, path: str, displayName: str, folderId: str = None):
        return (
            await self.api(
                "upload_group_file",
                **{
                    "group_id": self.groupId,
                    "file": path,
                    "name": displayName,
                    "folder": folderId,
                },
            )
        ).json()["data"]

    async def get_all_files(self):
        return (
            await self.api(
                "get_group_root_files",
                **{
                    "group_id": self.groupId,
                },
            )
        ).json()["data"]


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


class PrivateMessageMixin:
    api: API_Caller_T
    event: Dict[str, Any]
    targetId: int

    async def private_msg(self, *chain: SegmentInstance_T):
        await self.api(
            "send_msg",
            **{
                "message_type": "private",
                "user_id": self.targetId,
                "message": [segment.formatted for segment in chain],
            },
        )


class TempMixin(PrivateMessageMixin):
    pass


class FriendMixin(PrivateMessageMixin):
    async def delete(self):
        await self.api(
            "delete_friend",
            **{
                "friend_id": self.targetId,
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


class BeenAddedMixin:
    api: API_Caller_T
    flag: str

    async def resolve(self):
        await self.api(
            "set_friend_add_request",
            **{"flag": self.flag, "approve": True},
        )

    async def reject(self, reason: str = ""):
        await self.api(
            "set_friend_add_request",
            **{"flag": self.flag, "approve": False},
        )
