# https://docs.go-cqhttp.org/api/#%E5%A4%84%E7%90%86%E5%8A%A0%E7%BE%A4%E8%AF%B7%E6%B1%82-%E9%82%80%E8%AF%B7
# from __future__ import annotations

from typing import TYPE_CHECKING
from pepperbot.core.bot.api_caller import ApiCaller
from pepperbot.store.meta import get_onebot_caller
from pepperbot.types import BaseBot

if TYPE_CHECKING:
    from pepperbot.core.message.chain import T_SegmentInstance


class OnebotV11Api:
    @staticmethod
    async def get_login_info():
        return (await get_onebot_caller()("get_login_info")).json()["data"]

    @staticmethod
    async def group_message(group_id: str, *segments: "T_SegmentInstance"):
        message = [segment.onebot for segment in segments]

        return await get_onebot_caller()(
            "send_group_msg",
            **{
                "group_id": group_id,
                "message": message,
            },
        )

    @staticmethod
    async def upload_group_file(
        group_id: str,
        path: str,
        display_name: str,
        folder_id: str = None,
    ):
        return (
            await get_onebot_caller()(
                "upload_group_file",
                **{
                    "group_id": group_id,
                    "folder": folder_id,
                    "file": path,
                    "name": display_name,
                },
            )
        ).json()["data"]

    @staticmethod
    async def get_all_files(group_id: str):
        return (
            await get_onebot_caller()(
                "get_group_root_files",
                **{
                    "group_id": group_id,
                },
            )
        ).json()["data"]

    @staticmethod
    async def ban(group_id: str, user_id: str, duration: int = 30):
        await get_onebot_caller()(
            "set_group_ban",
            **{
                "group_id": group_id,
                "user_id": user_id,
                "duration": duration * 60,
            },
        )

    @staticmethod
    async def kickout(group_id: str, user_id: str, permenant: bool = False):
        await get_onebot_caller()(
            "set_group_kick",
            **{
                "group_id": group_id,
                "user_id": user_id,
                "reject_add_request": permenant,
            },
        )

    @staticmethod
    async def private_message(user_id: str, *segments: "T_SegmentInstance"):
        await get_onebot_caller()(
            "send_msg",
            **{
                "message_type": "private",
                "user_id": user_id,
                "message": [segment.onebot for segment in segments],
            },
        )

    @staticmethod
    async def delete_friend(friend_id: str):
        await get_onebot_caller()(
            "delete_friend",
            **{
                "friend_id": friend_id,
            },
        )

    @staticmethod
    async def accept_group_request(flag: str):
        await get_onebot_caller()(
            "set_group_add_request",
            **{
                "flag": flag,
                "type": "add",
                "approve": True,
            },
        )

    @staticmethod
    async def reject_group_request(flag: str, reason: str = ""):
        await get_onebot_caller()(
            "set_group_add_request",
            **{
                "flag": flag,
                "type": "add",
                "approve": False,
                "reason": reason,
            },
        )

    @staticmethod
    async def accept_friend_request(flag: str):
        await get_onebot_caller()(
            "set_friend_add_request",
            **{
                "flag": flag,
                "approve": True,
            },
        )

    @staticmethod
    async def reject_friend_request(flag: str, reason: str = ""):
        await get_onebot_caller()(
            "set_friend_add_request",
            **{
                "flag": flag,
                "approve": False,
            },
        )


class OnebotV11Properties(BaseBot):
    bot_id: str
    group_id: str
    private_id: str
    api_caller: ApiCaller


class OnebotV11CommonApi(OnebotV11Properties):
    pass


class OnebotV11GroupApi(OnebotV11Properties):
    async def group_message(self, *segments: "T_SegmentInstance"):
        """
        默认向当前群发送消息

        如果想实现，在A群接收到消息后，给B群发消息，手动调api
        """
        return await OnebotV11Api.group_message(self.group_id, segments)

    def at_all(self):
        return {"type": "at", "data": {"qq": "all"}}

    async def upload_group_file(
        self,
        path: str,
        display_name: str,
        folder_id: str = None,
    ):
        return await OnebotV11Api.upload_group_file(
            self.group_id,
            path,
            display_name,
            folder_id,
        )

    async def get_all_files(self):
        return await OnebotV11Api.get_all_files(self.group_id)

    async def ban(self, user_id: str, duration: int = 30):
        return await OnebotV11Api.ban(self.group_id, user_id, duration)

    async def kickout(self, user_id: str, permenant: bool = False):
        return await OnebotV11Api.kickout(self.group_id, user_id, permenant)

    async def accept_group_request(self, flag: str):
        return await OnebotV11Api.accept_group_request(flag)

    async def reject_group_request(self, flag: str, reason: str = ""):
        return await OnebotV11Api.reject_group_request(flag, reason)


class OnebotV11PrivateApi(OnebotV11Properties):
    async def private_message(self, *segments: "T_SegmentInstance"):
        return await OnebotV11Api.private_message(self.private_id, *segments)

    async def delete_friend(self):
        return await OnebotV11Api.delete_friend(self.private_id)

    async def accept_friend_request(self, flag: str):
        return await OnebotV11Api.accept_friend_request(flag)

    async def reject_friend_request(self, flag: str, reason: str = ""):
        return await OnebotV11Api.reject_friend_request(flag, reason)


class OnebotV11GroupBot(OnebotV11CommonApi, OnebotV11GroupApi):
    __slots__ = (
        "bot_id",
        "group_id",
        "api_caller",
    )

    def __init__(self, bot_id: str, group_id: str):
        self.bot_id = bot_id
        self.group_id = group_id
        self.api_caller = get_onebot_caller()


class OnebotV11PrivateBot(OnebotV11CommonApi, OnebotV11PrivateApi):
    __slots__ = (
        "bot_id",
        "private_id",
        "api_caller",
    )

    def __init__(self, bot_id: str, private_id: str):
        self.bot_id = bot_id
        self.private_id = private_id
        self.api_caller = get_onebot_caller()
