from typing import List, Optional, Type, cast

from pepperbot.adapters.keaimao.api import KeaimaoApi, KeaimaoGroupApi, KeaimaoGroupBot
from pepperbot.adapters.onebot.api import (
    OnebotV11Api,
    OnebotV11GroupApi,
    OnebotV11GroupBot,
)
from pepperbot.adapters.telegram.api import TelegramApi, TelegramGroupApi
from pepperbot.core.message.chain import T_SegmentInstance

# from pepperbot.core.event.utils import get_bot_instance
from pepperbot.exceptions import BackendApiError, EventHandleError
from pepperbot.types import BaseBot, T_BotProtocol


class ArbitraryApi:
    onebot = OnebotV11Api
    keaimao = KeaimaoApi
    telegram = TelegramApi


class UniversalProperties(BaseBot):
    protocol: T_BotProtocol
    bot_id: str
    group_id: str
    arbitrary: Type[ArbitraryApi]
    onebot: Optional[OnebotV11GroupBot]
    keaimao: Optional[KeaimaoGroupBot]
    # telegram: Optional[TelegramGroupBot]


class UniversalCommonApi(UniversalProperties):

    pass


class UniversalGroupApi(UniversalProperties):
    async def group_message(self, *segments: T_SegmentInstance):
        if self.onebot:
            return await self.onebot.group_message(*segments)

        elif self.keaimao:
            return await self.keaimao.group_message(*segments)

        else:
            raise BackendApiError()

    group_msg = group_message


class UniversalPrivateApi(UniversalProperties):
    pass


class UniversalGroupBot(UniversalCommonApi, UniversalGroupApi):
    """
    universal api直接绑定在bot身上，方法都是实例化的，因为最常用
    chain 也实例化，常用
    onebot, keaimao, telegram的方法，不太常用，也可以实例化，
    同一个协议，同一个消息来源，只会多创建一个api实例，可以接受
    """

    __slots__ = (
        "protocol",
        "bot_id",
        "group_id",
        "arbitrary",
        "onebot",
        "keaimao",
        "telegram",
    )

    def __init__(
        self,
        protocol: T_BotProtocol,
        bot_id: str,
        group_id: str,
    ):
        self.protocol = protocol

        self.bot_id = bot_id
        self.group_id = group_id

        self.arbitrary = ArbitraryApi

        from pepperbot.core.event.handle import get_or_create_bot

        bot_instance = get_or_create_bot(protocol, "group", group_id)

        self.onebot = (
            cast(OnebotV11GroupBot, bot_instance) if protocol == "onebot" else None
        )
        self.keaimao = (
            cast(KeaimaoGroupBot, bot_instance) if protocol == "keaimao" else None
        )
        self.telegram = bot_instance if protocol == "telegram" else None


class UniversalPrivateBot(UniversalCommonApi, UniversalPrivateApi):
    pass
