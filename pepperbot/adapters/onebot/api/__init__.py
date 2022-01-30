# https://docs.go-cqhttp.org/api/#%E5%A4%84%E7%90%86%E5%8A%A0%E7%BE%A4%E8%AF%B7%E6%B1%82-%E9%82%80%E8%AF%B7

from typing import Tuple
from pepperbot.core.bot.api_caller import ApiCaller
from pepperbot.core.message.chain import T_SegmentInstance
from pepperbot.store.meta import get_onebot_caller
from pepperbot.types import BaseBot


class OnebotV11Api:
    @staticmethod
    async def group_message(group_id: str, chain: Tuple[T_SegmentInstance, ...]):
        message = [segment.onebot for segment in chain]

        await get_onebot_caller()(
            "send_group_msg",
            **{
                "group_id": group_id,
                "message": message,
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
    async def group_message(self, *segments: T_SegmentInstance):
        """
        默认向当前群发送消息

        如果想实现，在A群接收到消息后，给B群发消息，手动调api
        """
        return await OnebotV11Api.group_message(self.group_id, segments)


class OnebotV11PrivateApi(OnebotV11Properties):
    pass


class OnebotV11GroupBot(OnebotV11CommonApi, OnebotV11GroupApi):
    # __slots__=()

    def __init__(self, bot_id: str, group_id: str):
        self.bot_id = bot_id
        self.group_id = group_id
        self.api_caller = get_onebot_caller()


class OnebotV11PrivateBot(OnebotV11CommonApi, OnebotV11PrivateApi):
    # __slots__=()

    def __init__(self, bot_id: str, private_id: str):
        self.bot_id = bot_id
        self.private_id = private_id
        self.api_caller = get_onebot_caller()


# class AddGroupBot(BaseBot, AddGroupMixin):
#     def __init__(self, event: Dict[str, Any], api: API_Caller_T) -> None:
#         self.api: API_Caller_T = api
#         self.flag = event["flag"]
