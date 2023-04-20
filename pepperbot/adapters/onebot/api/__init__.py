# https://docs.go-cqhttp.org/api/#%E5%A4%84%E7%90%86%E5%8A%A0%E7%BE%A4%E8%AF%B7%E6%B1%82-%E9%82%80%E8%AF%B7

# from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, List, Optional, Tuple, Union

from pepperbot.adapters.onebot.models.group import InvitedRequest, JoinRequest
from pepperbot.adapters.onebot.models.user import GroupMember
from pepperbot.core.api.api_caller import ApiCaller
from pepperbot.exceptions import BackendApiError, EventHandleError
from pepperbot.store.meta import get_onebot_caller
from pepperbot.types import BaseBot

if TYPE_CHECKING:
    from pepperbot.core.message.chain import T_SegmentInstance


class OnebotV11API:
    """https://docs.go-cqhttp.org/api/#bot-%E8%B4%A6%E5%8F%B7"""

    @staticmethod
    async def get_login_info():
        """https://docs.go-cqhttp.org/api/#%E8%8E%B7%E5%8F%96%E7%99%BB%E5%BD%95%E5%8F%B7%E4%BF%A1%E6%81%AF"""

        try:
            return await get_onebot_caller()("get_login_info")
        except:
            raise BackendApiError(f"无法获取onebot机器人登录信息，请确认onebot服务是否正常运行")

    @staticmethod
    async def set_account_profile(
        nickname: Optional[str] = None,
        company: Optional[str] = None,
        email: Optional[str] = None,
        college: Optional[str] = None,
        personal_note: Optional[str] = None,
    ):
        """https://docs.go-cqhttp.org/api/#%E8%AE%BE%E7%BD%AE%E7%99%BB%E5%BD%95%E5%8F%B7%E8%B5%84%E6%96%99

        字段名	数据类型	默认值	说明
        nickname	string	-	名称
        company	string	-	公司
        email	string	-	邮箱
        college	string	-	学校
        personal_note	string	-	个人说明
        """

        buffer = {k: v for k, v in locals().items() if v is not None}

        return await get_onebot_caller()(
            "set_qq_profile",
            **buffer,
        )

    @staticmethod
    async def get_online_clients(no_cache=True):
        """https://docs.go-cqhttp.org/api/#获取当前账号在线客户端列表"""

        return await get_onebot_caller()(
            "get_online_clients",
            **{
                "no_cache": no_cache,
            },
        )

    @staticmethod
    async def get_stranger_info(
        user_id: str,
        no_cache: bool = False,
    ):
        """https://docs.go-cqhttp.org/api/#获取陌生人信息

        字段名	数据类型	默认值	说明
        user_id	int64	-	QQ 号
        no_cache	boolean	false	是否不使用缓存（使用缓存可能更新不及时, 但响应更快）
        """

        return await get_onebot_caller()(
            "get_stranger_info",
            **{
                "user_id": user_id,
                "no_cache": no_cache,
            },
        )

    @staticmethod
    async def get_friend_list():
        """https://docs.go-cqhttp.org/api/#获取好友列表"""

        return await get_onebot_caller()("get_stranger_info")

    @staticmethod
    async def get_unidirectional_friend_list():
        """https://docs.go-cqhttp.org/api/#获取单向好友列表"""

        return await get_onebot_caller()("get_unidirectional_friend_list")

    @staticmethod
    async def delete_friend(user_id: str):
        """https://docs.go-cqhttp.org/api/#删除好友"""

        return await get_onebot_caller()(
            "delete_friend",
            **{
                "user_id": user_id,
            },
        )

    @staticmethod
    async def delete_unidirectional_friend(user_id: str):
        """https://docs.go-cqhttp.org/api/#删除好友"""

        return await get_onebot_caller()(
            "delete_unidirectional_friend",
            **{
                "user_id": user_id,
            },
        )

    @staticmethod
    async def private_message(user_id: str, *segments: "T_SegmentInstance"):
        """https://docs.go-cqhttp.org/api/#发送私聊消息"""

        return await get_onebot_caller()(
            "send_msg",
            **{
                "message_type": "private",
                "user_id": user_id,
                "message": [await segment.onebot() for segment in segments],
            },
        )

    @staticmethod
    async def group_message(group_id: str, *segments: "T_SegmentInstance"):
        message = [await segment.onebot() for segment in segments]

        return await get_onebot_caller()(
            "send_group_msg",
            **{
                "group_id": group_id,
                "message": message,
            },
        )

    @staticmethod
    async def withdraw_message(message_id: str):
        """https://docs.go-cqhttp.org/api/#撤回消息

        **参数**
        | 字段名       | 数据类型 | 默认值 | 说明    |
        | ------------ | -------- | ------ | ------- |
        | `message_id` | int32    | -      | 消息 ID |

        **响应数据**
        | 字段       | 类型              | 说明     |
        | ---------- | ----------------- | -------- |
        | `messages` | forward message[] | 消息列表 |
        """

        await get_onebot_caller()(
            "delete_msg",
            **{
                "message_id": message_id,
            },
        )

    @staticmethod
    async def mark_msg_as_read(message_id: int) -> None:
        """https://docs.go-cqhttp.org/api/#标记消息已读

        Args:
            message_id (int): 消息 ID

        Returns:
            None
        """
        await get_onebot_caller()(
            "mark_msg_as_read",
            **{
                "message_id": message_id,
            },
        )

    @staticmethod
    async def get_forward_msg(message_id: str) -> list[dict[str, Any]]:
        """
        获取合并转发内容

        https://docs.go-cqhttp.org/api/#获取合并转发内容

        Args:
            message_id (str): 消息 ID

        Returns:
            List[Dict[str, Any]]: 消息列表，包含以下字段：
                - `content` (str): 消息内容
                - `sender` (Dict[str, Any]): 消息发送者信息，包含以下字段：
                    - `nickname` (str): 发送者昵称
                    - `user_id` (int): 发送者 QQ 号
                - `time` (int): 消息发送时间的时间戳
        """
        resp = await get_onebot_caller()(
            "get_forward_msg",
            **{
                "message_id": message_id,
            },
        )
        messages = resp.get("data", {}).get("messages", [])
        return messages

    @staticmethod
    async def send_group_forward_msg(group_id: int, messages: list[dict]) -> dict:
        """
        发送合并转发 ( 群聊 )

        https://docs.go-cqhttp.org/api/#发送合并转发-群聊-

        Args:
            group_id (int): 群号
            messages (List[dict]): 自定义转发消息, 具体看 https://docs.go-cqhttp.org/cqcode/#合并转发消息节点

        Returns:
            dict: 响应数据
                - `message_id` (int): 消息 ID
                - `forward_id` (str): 转发消息 ID
        """
        return await get_onebot_caller()(
            "send_group_forward_msg",
            **{
                "group_id": group_id,
                "messages": messages,
            },
        )

    @staticmethod
    async def send_private_forward_msg(user_id: int, messages: list[dict]) -> dict:
        """
        发送合并转发 ( 好友 )

        Args:
            user_id (int): 好友 QQ 号
            messages (List[dict]): 自定义转发消息, 具体看 CQcode

        Returns:
            dict: 响应数据

        参考文档：
        https://docs.go-cqhttp.org/api/#发送合并转发-好友
        """
        return await get_onebot_caller()(
            "send_private_forward_msg",
            **{
                "user_id": user_id,
                "messages": messages,
            },
        )

    @staticmethod
    async def get_group_msg_history(group_id: int, message_seq: int = 0) -> List[dict]:
        """
        获取群消息历史记录

        Args:
            group_id (int): 群号
            message_seq (int, optional): 起始消息序号, 可通过 `get_msg` 获得，默认为 0

        Returns:
            List[dict]: 从起始序号开始的前19条消息

        Raises:
            TypeError: 当消息序号非整数时抛出该异常
        """
        if not isinstance(message_seq, int):
            raise TypeError("message_seq must be integer")

        return (
            await get_onebot_caller()(
                "get_group_msg_history",
                **{
                    "group_id": group_id,
                    "message_seq": message_seq,
                },
            )
        )["messages"]

    @staticmethod
    async def get_image(file: str) -> Optional[Dict[str, Any]]:
        """
        获取图片信息

        Args:
            file (str): 图片缓存文件名

        Returns:
            Dict[str, Any] or None: 图片信息
                - size (int): 图片源文件大小
                - filename (str): 图片文件原名
                - url (str): 图片下载地址
        """
        return await get_onebot_caller()(
            "get_image",
            **{
                "file": file,
            },
        )

    @staticmethod
    async def can_send_image() -> bool:
        """
        检查是否可以发送图片

        Returns:
            bool: 是否可以发送图片
        """
        res = await get_onebot_caller()("can_send_image")
        return res.get("yes", False)

    @staticmethod
    async def can_send_record() -> bool:
        """
        https://docs.go-cqhttp.org/api/#检查是否可以发送语音

        Returns:
            bool: 是否可以发送语音
        """
        resp = await get_onebot_caller()("can_send_record")
        return resp.get("yes", False)

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
    async def get_group_info(group_id: int, no_cache: bool = False) -> Dict[str, Any]:
        """
        https://docs.go-cqhttp.org/api/#获取群信息

        Args:
            group_id (int): 群号
            no_cache (bool, optional): 是否不使用缓存（使用缓存可能更新不及时，但响应更快）. Defaults to False.

        Returns:
            Dict[str, Any]: 包含群信息的字典，具体字段说明如下：
                - group_id (int): 群号
                - group_name (str): 群名称
                - group_memo (str): 群备注
                - group_create_time (int): 群创建时间
                - group_level (int): 群等级
                - member_count (int): 成员数
                - max_member_count (int): 最大成员数（群容量）
        """
        return await get_onebot_caller()(
            "get_group_info",
            **{
                "group_id": group_id,
                "no_cache": no_cache,
            },
        )

    @staticmethod
    async def get_group_list(no_cache: bool = False):
        """
        https://docs.go-cqhttp.org/api/#获取群列表

        Args:
            no_cache (bool, optional): 是否不使用缓存（使用缓存可能更新不及时, 但响应更快）. Defaults to False.

        Returns:
            List[Dict[str, Any]]: 响应内容为 json 数组, 每个元素和上面的 `get_group_info` 接口相同.
        """
        response = await get_onebot_caller()(
            "get_group_list",
            **{
                "no_cache": no_cache,
            },
        )
        return response

    @staticmethod
    async def get_group_member_info(group_id: str, user_id: str):
        return_json = await get_onebot_caller()(
            "get_group_member_info",
            **{
                "group_id": group_id,
                "user_id": user_id,
            },
        )

        return GroupMember(**return_json)

    @staticmethod
    async def get_group_member_list(group_id: int, no_cache: Optional[bool] = False):
        """
        获取群成员列表

        Args:
            group_id (int): 群号
            no_cache (bool, optional): 是否不使用缓存（使用缓存可能更新不及时, 但响应更快）, defaults to False.

        Returns:
            List[Dict[str, Any]]: 响应内容为 json 数组, 每个元素的内容和上面的 `get_group_member_info` 接口相同, 但对于同一个群组的同一个成员,
            获取列表时和获取单独的成员信息时, 某些字段可能有所不同, 例如 `area`、`title` 等字段在获取列表时无法获得, 具体应以单独的成员信息为准。
        """
        return await get_onebot_caller()(
            "get_group_member_list",
            **{
                "group_id": group_id,
                "no_cache": no_cache,
            },
        )

    @staticmethod
    async def get_group_honor_info(
        group_id: int, hon_type: Union[str, None] = None
    ) -> Union[List[dict], dict]:
        """
        https://docs.go-cqhttp.org/api/#获取群荣誉信息

        Args:
            group_id (int): 群号
            hon_type (str, optional): 要获取的群荣誉类型，可传入 "talkative" "performer" "legend" "strong_newbie" "emotion" 以分别获取单个类型的群荣誉数据，或传入 "all" 获取所有数据。默认为 None。

        Returns:
            Union[List[dict], dict]: 如果传入的是单个类型，返回一个 dict，包含该类型的群荣誉数据；如果传入的是 "all"，返回一个 list，包含所有类型的群荣誉数据。
        """
        return await get_onebot_caller()(
            "get_group_honor_info",
            **{
                "group_id": group_id,
                "type": hon_type,
            },
        )

    @staticmethod
    async def get_group_system_msg() -> dict:
        """
        获取群系统消息

        Returns:
            Dict[str, Union[List[InvitedRequest], List[JoinRequest]]]: 群系统消息
        """
        result = await get_onebot_caller()("get_group_system_msg")
        invited_requests = result.get("invited_requests", [])
        join_requests = result.get("join_requests", [])
        return {
            "invited_requests": [
                InvitedRequest(**request) for request in invited_requests
            ],
            "join_requests": [JoinRequest(**request) for request in join_requests],
        }

    @staticmethod
    async def get_essence_msg_list(group_id: int):
        """
        https://docs.go-cqhttp.org/api/#获取精华消息列表

        Args:
            group_id (int): 群号

        Returns:
            List[dict]: 精华消息列表，每个元素包含以下字段：
                - `sender_id` (int): 发送者 QQ 号
                - `sender_nick` (str): 发送者昵称
                - `sender_time` (int): 消息发送时间
                - `operator_id` (int): 操作者 QQ 号
                - `operator_nick` (str): 操作者昵称
                - `operator_time` (int): 精华设置时间
                - `message_id` (int): 消息 ID
        """
        return await get_onebot_caller()(
            "get_essence_msg_list",
            **{
                "group_id": group_id,
            },
        )

    @staticmethod
    async def get_group_at_all_remain(group_id: int) -> Tuple[bool, int, int]:
        """
        获取群 @全体成员 剩余次数

        Args:
            group_id (int): 群号

        Returns:
            Tuple[bool, int, int]: 返回元组，包含三个元素：
                can_at_all (bool): 是否可以 @全体成员
                remain_at_all_count_for_group (int): 群内所有管理当天剩余 @全体成员 次数
                remain_at_all_count_for_uin (int): Bot 当天剩余 @全体成员 次数
        """
        resp = await get_onebot_caller()(
            "get_group_at_all_remain",
            **{
                "group_id": group_id,
            },
        )
        return (
            resp.get("can_at_all", False),
            resp.get("remain_at_all_count_for_group", 0),
            resp.get("remain_at_all_count_for_uin", 0),
        )

    @staticmethod
    async def set_group_name(group_id: int, group_name: str) -> None:
        """
        https://docs.go-cqhttp.org/api/#设置群名

        Args:
            group_id (int): 群号
            group_name (str): 新群名

        Returns:
            None
        """
        await get_onebot_caller()(
            "set_group_name",
            **{
                "group_id": group_id,
                "group_name": group_name,
            },
        )

    @staticmethod
    async def set_group_card(group_id: int, user_id: int, card: str = "") -> None:
        """
        https://docs.go-cqhttp.org/api/#设置群名片

        Args:
            group_id (int): 群号
            user_id (int): 要设置的 QQ 号
            card (str, optional): 群名片内容，不填或空字符串表示删除群名片. Defaults to "".

        Returns:
            None
        """
        await get_onebot_caller()(
            "set_group_card",
            **{
                "group_id": group_id,
                "user_id": user_id,
                "card": card,
            },
        )

    @staticmethod
    async def set_group_ban(group_id: str, user_id: str, duration: int = 30):
        """
        群单人禁言

        Args:
            group_id (int): 群号
            user_id (int): 要禁言的 QQ 号
            duration (int, optional): 禁言时长, 单位秒, 0 表示取消禁言. Defaults to 30 * 60.

        Returns:
            None
        """
        await get_onebot_caller()(
            "set_group_ban",
            **{
                "group_id": group_id,
                "user_id": user_id,
                "duration": duration * 60,
            },
        )

    @staticmethod
    async def set_group_whole_ban(group_id: int, enable: bool = True) -> None:
        """
        https://docs.go-cqhttp.org/api/#群全员禁言

        Args:
            group_id (int): 群号
            enable (bool, optional): 是否禁言. Defaults to True.

        Returns:
            None
        """
        await get_onebot_caller()(
            "set_group_whole_ban",
            **{
                "group_id": group_id,
                "enable": enable,
            },
        )

    @staticmethod
    async def send_group_notice(group_id: int, content: str, image: str = "") -> None:
        """
        https://docs.go-cqhttp.org/api/#发送群公告

        Args:
            group_id (int): 群号
            content (str): 公告内容
            image (str, optional): 图片路径（可选）

        Returns:
            None
        """
        await get_onebot_caller()(
            "_send_group_notice",
            **{
                "group_id": group_id,
                "content": content,
                "image": image,
            },
        )

    @staticmethod
    async def set_group_kick(group_id: str, user_id: str, permanent: bool = False):
        """
        群组踢人

        Args:
            group_id (int): 群号
            user_id (int): 要踢的 QQ 号
            reject_add_request (bool, optional): 拒绝此人的加群请求，默认为 False

        Returns:
            None
        """
        await get_onebot_caller()(
            "set_group_kick",
            **{
                "group_id": group_id,
                "user_id": user_id,
                "reject_add_request": permanent,
            },
        )

    @staticmethod
    async def upload_group_file(
        group_id: str,
        path: str,
        display_name: str,
        folder_id: Optional[str] = None,
    ):
        return await get_onebot_caller()(
            "upload_group_file",
            **{
                "group_id": group_id,
                "folder": folder_id,
                "file": path,
                "name": display_name,
            },
        )

    @staticmethod
    async def get_all_files(group_id: str):
        return await get_onebot_caller()(
            "get_group_root_files",
            **{
                "group_id": group_id,
            },
        )

    @staticmethod
    async def get_status() -> Dict[str, Any]:
        """
        https://docs.go-cqhttp.org/api/#获取状态

        Returns:
            Dict[str, Any]: 状态信息
        """
        result = await get_onebot_caller()("get_status")
        return result


class OnebotV11Properties(BaseBot):
    bot_id: str
    group_id: str
    private_id: str
    api_caller: ApiCaller


class OnebotV11GroupAPI(OnebotV11Properties):
    async def group_message(self, *segments: "T_SegmentInstance"):
        """
        默认向当前群发送消息

        如果想实现，在A群接收到消息后，给B群发消息，手动调api
        """
        return await OnebotV11API.group_message(self.group_id, *segments)

    def at_all(self):
        return {"type": "at", "data": {"qq": "all"}}

    async def upload_group_file(
        self,
        path: str,
        display_name: str,
        folder_id: Optional[str] = None,
    ):
        return await OnebotV11API.upload_group_file(
            self.group_id,
            path,
            display_name,
            folder_id,
        )

    async def get_all_files(self):
        return await OnebotV11API.get_all_files(self.group_id)

    async def ban(self, user_id: str, duration: int = 30):
        return await OnebotV11API.set_group_ban(self.group_id, user_id, duration)

    async def kickout(self, user_id: str, permanent: bool = False):
        return await OnebotV11API.set_group_kick(self.group_id, user_id, permanent)

    async def accept_group_request(self, flag: str):
        return await OnebotV11API.accept_group_request(flag)

    async def reject_group_request(self, flag: str, reason: str = ""):
        return await OnebotV11API.reject_group_request(flag, reason)


class OnebotV11PrivateAPI(OnebotV11Properties):
    async def private_message(self, *segments: "T_SegmentInstance"):
        return await OnebotV11API.private_message(self.private_id, *segments)

    async def delete_friend(self):
        return await OnebotV11API.delete_friend(self.private_id)

    async def accept_friend_request(self, flag: str):
        return await OnebotV11API.accept_friend_request(flag)

    async def reject_friend_request(self, flag: str, reason: str = ""):
        return await OnebotV11API.reject_friend_request(flag, reason)


class OnebotV11GroupBot(OnebotV11GroupAPI):
    __slots__ = (
        "bot_id",
        "group_id",
        "api_caller",
    )

    def __init__(self, bot_id: str, group_id: str):
        self.bot_id = bot_id
        self.group_id = group_id
        self.api_caller = get_onebot_caller()


class OnebotV11PrivateBot(OnebotV11PrivateAPI):
    __slots__ = (
        "bot_id",
        "private_id",
        "api_caller",
    )

    def __init__(self, bot_id: str, private_id: str):
        self.bot_id = bot_id
        self.private_id = private_id
        self.api_caller = get_onebot_caller()
