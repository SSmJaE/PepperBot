from typing import List, Optional, cast

from pepperbot.adapters.keaimao.api import KeaimaoApi, KeaimaoGroupApi, KeaimaoGroupBot
from pepperbot.adapters.onebot.api import (
    OnebotV11Api,
    OnebotV11GroupApi,
    OnebotV11GroupBot,
)
from pepperbot.adapters.telegram.api import TelegramGroupApi
from pepperbot.core.message.chain import T_SegmentInstance

# from pepperbot.core.event.utils import get_bot_instance
from pepperbot.exceptions import BackendApiError, EventHandleError
from pepperbot.types import BaseBot, T_BotProtocol


class UniversalArbitraryApi:
    onebot = OnebotV11Api
    keaimao = KeaimaoApi


class UniversalProperties(BaseBot):
    protocol: T_BotProtocol
    bot_id: str
    group_id: str
    onebot: Optional[OnebotV11GroupBot]
    keaimao: Optional[KeaimaoGroupBot]
    # telegram: Optional[TelegramGroupBot]


class UniversalCommonApi(UniversalProperties):

    pass


class UniversalGroupApi(UniversalProperties):
    async def group_message(self, *chain: T_SegmentInstance):
        if self.onebot:
            await self.onebot.group_message(*chain)

        elif self.keaimao:
            for segment in chain:
                await self.keaimao.group_message(segment)

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
        "onebot",
        "keaimao",
        "telegram",
        "arbitrary",
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

        from pepperbot.core.event.handle import get_bot_instance

        bot_instance = get_bot_instance(protocol, "group", group_id)
        self.onebot = (
            cast(OnebotV11GroupBot, bot_instance) if protocol == "onebot" else None
        )
        self.keaimao = (
            cast(KeaimaoGroupBot, bot_instance) if protocol == "keaimao" else None
        )
        self.telegram = bot_instance if protocol == "telegram" else None

        self.arbitrary = UniversalArbitraryApi


class UniversalPrivateBot(UniversalCommonApi, UniversalPrivateApi):
    pass
