from typing import TYPE_CHECKING, Dict, Iterable, List, Tuple

if TYPE_CHECKING:
    from pepperbot.core.message.segment import T_SegmentInstance

from pepperbot.core.api.api_caller import ApiCaller
from pepperbot.core.message.segment import (
    Audio,
    Image,
    Music,
    T_SegmentClass,
    Text,
    Video,
)
from pepperbot.exceptions import BackendApiError, EventHandleError
from pepperbot.extensions.log import logger
from pepperbot.store.meta import get_bot_id, get_telegram_caller
from pepperbot.types import BaseBot
from pyrogram.client import Client
from pyrogram.enums.parse_mode import ParseMode

# segment, action, arg_name, property
TELEGRAM_SEGMENT_ACTION_MAPPING: Dict[T_SegmentClass, str] = {
    Audio: "send_audio",
    Image: "send_photo",
    Text: "send_message",
    Video: "send_video",
}


class TelegramAPI:
    @staticmethod
    async def send_message(chat_id: str, iterable: Iterable["T_SegmentInstance"]):
        client = get_telegram_caller()

        for segment in iterable:
            segment_type = segment.__class__

            if action := TELEGRAM_SEGMENT_ACTION_MAPPING.get(segment_type):
                async_method = getattr(client, action)

                await async_method(
                    chat_id=chat_id,
                    **(await segment.telegram()),
                )

            else:
                logger.error(f"尚未适配的消息类型 telegram {segment_type}")

    @staticmethod
    async def group_message(chat_id: str, *segments: "T_SegmentInstance"):
        await TelegramAPI.send_message(chat_id, segments)

    @staticmethod
    async def private_message(chat_id: str, *segments: "T_SegmentInstance"):
        await TelegramAPI.send_message(chat_id, segments)


class TelegramProperties(BaseBot):
    bot_id: str
    group_id: str
    private_id: str
    api_caller: Client


class TelegramGroupAPI(TelegramProperties):
    async def group_message(self, *segments: "T_SegmentInstance"):
        return await TelegramAPI.group_message(self.group_id, *segments)


class TelegramPrivateAPI(TelegramProperties):
    async def private_message(self, *segments: "T_SegmentInstance"):
        return await TelegramAPI.private_message(self.private_id, *segments)


class TelegramGroupBot(TelegramGroupAPI):
    __slots__ = (
        "bot_id",
        "group_id",
        "api_caller",
    )

    def __init__(self, bot_id: str, group_id: str):
        self.bot_id = bot_id
        self.group_id = group_id
        self.api_caller = get_telegram_caller()


class TelegramPrivateBot(TelegramPrivateAPI):
    __slots__ = (
        "bot_id",
        "private_id",
        "api_caller",
    )

    def __init__(self, bot_id: str, private_id: str):
        self.bot_id = bot_id
        self.private_id = private_id
        self.api_caller = get_telegram_caller()
