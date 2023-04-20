from typing import Any, Callable, Dict, Optional, cast

from devtools import debug
from pepperbot.adapters.telegram.event import TelegramEvent
from pepperbot.core.event.base_adapter import BaseAdapter
from pepperbot.exceptions import EventHandleError
from pepperbot.extensions.log import debug_log, logger
from pepperbot.store.event import ProtocolEvent, filter_event_by_type
from pepperbot.types import T_ConversationType
from pepperbot.utils.common import get_own_attributes
from pyrogram import ContinuePropagation, filters
from pyrogram.client import Client
from pyrogram.enums.chat_type import ChatType
from pyrogram.handlers.callback_query_handler import CallbackQueryHandler
from pyrogram.handlers.chat_join_request_handler import ChatJoinRequestHandler
from pyrogram.handlers.chat_member_updated_handler import ChatMemberUpdatedHandler
from pyrogram.handlers.chosen_inline_result_handler import ChosenInlineResultHandler
from pyrogram.handlers.edited_message_handler import EditedMessageHandler
from pyrogram.handlers.inline_query_handler import InlineQueryHandler
from pyrogram.handlers.message_handler import MessageHandler
from pyrogram.handlers.raw_update_handler import RawUpdateHandler
from pyrogram.types import CallbackQuery, ChatEventFilter, Message


own_attributes = get_own_attributes(TelegramEvent)

events: list[ProtocolEvent] = [getattr(TelegramEvent, attr) for attr in own_attributes]


class TelegramAdapter(BaseAdapter):
    kwargs_mapping = {
        cast(str, event.protocol_event_name): event.keyword_arguments
        for event in events
    }

    all_events = events
    all_event_names = [cast(str, event.protocol_event_name) for event in events]

    meta_events = filter_event_by_type(events, ("meta",))
    meta_event_names = [cast(str, event.protocol_event_name) for event in meta_events]
    notice_events = filter_event_by_type(events, ("notice",))
    notice_event_names = [
        cast(str, event.protocol_event_name) for event in notice_events
    ]
    request_events = filter_event_by_type(events, ("request",))
    request_event_names = [
        cast(str, event.protocol_event_name) for event in request_events
    ]
    message_events = filter_event_by_type(events, ("message",))
    message_event_names = [
        cast(str, event.protocol_event_name) for event in message_events
    ]

    group_events = filter_event_by_type(events, ("group",))
    private_events = filter_event_by_type(events, ("private",))

    @staticmethod
    def get_event(raw_event: Dict):
        # debug(raw_event)
        return getattr(TelegramEvent, raw_event["event_name"])

    @staticmethod
    def get_conversation_type(raw_event: Dict, raw_event_name: str):
        callback_object = raw_event["callback_object"]

        # debug_log(callback_object)

        if isinstance(callback_object, CallbackQuery):
            chat_type: ChatType = callback_object.message.chat.type

        elif isinstance(callback_object, Message):
            chat_type: ChatType = callback_object.chat.type

        else:
            chat_type: ChatType = callback_object.chat_type

        if chat_type in [ChatType.BOT, ChatType.PRIVATE]:
            mode = "private"
        elif chat_type == ChatType.GROUP:
            mode = "group"
        else:
            raise EventHandleError(f"")

        return mode

    @staticmethod
    def get_source_id(raw_event: Dict, mode: T_ConversationType):
        source_id: Optional[str] = None

        callback_object = raw_event["callback_object"]
        if mode == "group":
            # 注意不是from_user.id，是来源id，比如群号
            source_id = callback_object.chat.id

        elif mode == "private":
            source_id = callback_object.from_user.id

        elif mode == "channel":
            source_id = callback_object.chat.id

        return source_id

    @staticmethod
    def get_user_id(raw_event: Dict, mode: T_ConversationType):
        callback_object = raw_event["callback_object"]

        # debug_log(callback_object)

        user_id: Optional[int | str] = None

        if isinstance(callback_object, CallbackQuery):
            user_id = callback_object.from_user.id

        elif isinstance(callback_object, Message):
            user_id = callback_object.from_user.id

        else:
            user_id = callback_object.user.id

        return str(user_id) if user_id else None


async def any_handler(client: Client, update: Any, handle_event, users, chats):
    await handle_event(
        "telegram",
        dict(
            event_name=TelegramEvent.raw_update.raw_event_name,
            callback_object=update,
            users=users,
            chats=chats,
        ),
    )

    raise ContinuePropagation


async def private_message_handler(client: Client, callback_object: Any, handle_event):
    await handle_event(
        "telegram",
        dict(
            event_name=TelegramEvent.private_message.raw_event_name,
            callback_object=callback_object,
        ),
    )

    raise ContinuePropagation


async def group_message_handler(client: Client, callback_object: Any, handle_event):
    await handle_event(
        "telegram",
        dict(
            event_name=TelegramEvent.group_message.raw_event_name,
            callback_object=callback_object,
        ),
    )

    raise ContinuePropagation


async def edited_message_handler(client: Client, callback_object: Any, handle_event):
    await handle_event(
        "telegram",
        dict(
            event_name=TelegramEvent.edited_message.raw_event_name,
            callback_object=callback_object,
        ),
    )

    raise ContinuePropagation


async def callback_query_handler(client: Client, callback_object: Any, handle_event):
    await handle_event(
        "telegram",
        dict(
            event_name=TelegramEvent.callback_query.raw_event_name,
            callback_object=callback_object,
        ),
    )

    raise ContinuePropagation


# async def chat_member_updated_handler(client: Client, message: Message, handle_event):
#     await handle_event(
#         "telegram",
#         dict(event_name=TelegramGroupEvent.group_message, callback_object=message),
#     )


async def chosen_inline_result_handler(
    client: Client, callback_object: Any, handle_event
):
    await handle_event(
        "telegram",
        dict(
            event_name=TelegramEvent.chosen_inline_result.raw_event_name,
            callback_object=callback_object,
        ),
    )

    raise ContinuePropagation


async def inline_query_handler(client: Client, callback_object: Any, handle_event):
    await handle_event(
        "telegram",
        dict(
            event_name=TelegramEvent.inline_query.raw_event_name,
            callback_object=callback_object,
        ),
    )

    raise ContinuePropagation


def with_handle_event(handle_event: Callable, handler: Callable):
    """
    avoid circlely import caused by `handle_event`

    pass `handle_event` as parameter to avoid multiple times import
    """

    async def wrapper(client, callback_object, *args):
        try:
            debug(*args)
            return await handler(client, callback_object, handle_event, *args)

        except ContinuePropagation:
            raise ContinuePropagation

        except Exception as e:
            logger.exception(e)

    return wrapper


def register_telegram_event(pyrogram_client: Client):
    from pepperbot.core.event.handle import handle_event

    # pyrogram_client.add_handler(
    #     RawUpdateHandler(
    #         with_handle_event(handle_event, any_handler),
    #     )
    # )
    pyrogram_client.add_handler(
        MessageHandler(
            with_handle_event(handle_event, private_message_handler),
            filters.private,
        )
    )
    pyrogram_client.add_handler(
        MessageHandler(
            with_handle_event(handle_event, group_message_handler),
            filters.group,
        )
    )
    pyrogram_client.add_handler(
        MessageHandler(
            with_handle_event(handle_event, group_message_handler),
            filters.channel,
        )
    )
    pyrogram_client.add_handler(
        EditedMessageHandler(
            with_handle_event(handle_event, edited_message_handler),
        )
    )
    pyrogram_client.add_handler(
        InlineQueryHandler(
            with_handle_event(handle_event, inline_query_handler),
        )
    )
    pyrogram_client.add_handler(
        CallbackQueryHandler(
            with_handle_event(handle_event, callback_query_handler),
        )
    )
    # pyrogram_client.add_handler(
    #     ChatMemberUpdatedHandler(
    #         with_handle_event(handle_event, chat_member_updated_handler),
    #     )
    # )
    pyrogram_client.add_handler(
        ChosenInlineResultHandler(
            with_handle_event(handle_event, chosen_inline_result_handler),
        )
    )
