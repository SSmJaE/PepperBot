from functools import partial

from pepperbot.adapters.keaimao.api import KeaimaoAPI
from pepperbot.adapters.onebot.api import OnebotV11API
from pepperbot.adapters.telegram.api import TelegramAPI
from pepperbot.core.message.segment import Reply, T_SegmentInstance
from pepperbot.exceptions import EventHandleError
from pepperbot.store.event import EventMetadata


class CommandSender:
    __slots__ = (
        "protocol",
        "mode",
        "source_id",
        "user_id",
        "message_sender",
        "onebot_message_id",
    )

    def __init__(self, event_meta: EventMetadata):
        self.protocol = event_meta.protocol
        self.mode = event_meta.conversation_type
        self.source_id = event_meta.source_id
        self.user_id = event_meta.user_id
        self.onebot_message_id = event_meta.raw_event.get("message_id", "")

        f = None

        if event_meta.protocol == "onebot":
            if event_meta.conversation_type == "group":
                f = partial(OnebotV11API.group_message, event_meta.source_id)

            if event_meta.conversation_type == "private":
                f = partial(OnebotV11API.private_message, event_meta.source_id)

        if event_meta.protocol == "keaimao":
            if event_meta.conversation_type == "group":
                f = partial(KeaimaoAPI.group_message, event_meta.source_id)

            if event_meta.conversation_type == "private":
                f = partial(KeaimaoAPI.private_message, event_meta.source_id)

        if event_meta.protocol == "telegram":
            if event_meta.conversation_type == "group":
                f = partial(TelegramAPI.group_message, event_meta.source_id)

            if event_meta.conversation_type == "private":
                f = partial(TelegramAPI.private_message, event_meta.source_id)

        if not f:
            raise EventHandleError(f"未知的协议类型：{event_meta.protocol}")

        self.message_sender = f

    async def send_message(self, *segments: T_SegmentInstance):
        """自动识别消息来源并发送，不需要指定协议，不需要指定是私聊还是群"""
        return await self.message_sender(*segments)

    async def reply(self, *segments: T_SegmentInstance):
        """自动识别消息来源并回复，不需要指定协议，不需要指定是私聊还是群"""
        return await self.message_sender(Reply(self.onebot_message_id), *segments)
