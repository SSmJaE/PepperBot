from typing import Callable, Dict

from devtools import debug
from pepperbot.adapters.telegram.event import (
    TelegramCommonEvent,
    TelegramGroupEvent,
    TelegramMetaEvent,
    TelegramPrivateEvent,
)
from pepperbot.adapters.telegram.event.kwargs import TELEGRAM_KWARGS_MAPPING
from pepperbot.core.event.base_adapter import BaseAdapater

# from pepperbot.core.event.handle import handle_event
from pepperbot.exceptions import EventHandleError
from pepperbot.utils.common import get_own_attributes
from pyrogram import ContinuePropagation, filters
from pyrogram.client import Client
from pyrogram.handlers.callback_query_handler import CallbackQueryHandler
from pyrogram.handlers.chat_join_request_handler import ChatJoinRequestHandler
from pyrogram.handlers.chat_member_updated_handler import ChatMemberUpdatedHandler
from pyrogram.handlers.chosen_inline_result_handler import ChosenInlineResultHandler
from pyrogram.handlers.inline_query_handler import InlineQueryHandler
from pyrogram.handlers.message_handler import MessageHandler
from pyrogram.types import Message


class TelegramAdapter(BaseAdapater):
    @staticmethod
    def get_event_name(raw_event: Dict):
        debug(raw_event)

        return raw_event["event_name"]

    event_prefix = "telegram_"
    meta_events = list(get_own_attributes(TelegramMetaEvent))
    common_events = list(get_own_attributes(TelegramCommonEvent))
    group_events = list(get_own_attributes(TelegramGroupEvent))
    private_events = list(get_own_attributes(TelegramPrivateEvent))

    kwargs = TELEGRAM_KWARGS_MAPPING


async def private_message_handler(client: Client, message: Message, handle_event):
    await handle_event(
        "telegram",
        dict(event_name=TelegramPrivateEvent.private_message, callback_object=message),
    )


async def group_message_handler(client: Client, message: Message, handle_event):
    await handle_event(
        "telegram",
        dict(event_name=TelegramGroupEvent.group_message, callback_object=message),
    )


async def callback_query_handler(client: Client, message: Message, handle_event):
    await handle_event(
        "telegram",
        dict(event_name=TelegramCommonEvent.callback_query, callback_object=message),
    )


# async def chat_member_updated_handler(client: Client, message: Message, handle_event):
#     await handle_event(
#         "telegram",
#         dict(event_name=TelegramGroupEvent.group_message, callback_object=message),
#     )


async def chosen_inline_result_handler(client: Client, message: Message, handle_event):
    await handle_event(
        "telegram",
        dict(
            event_name=TelegramCommonEvent.chosen_inline_result, callback_object=message
        ),
    )


async def inline_query_handler(client: Client, message: Message, handle_event):
    await handle_event(
        "telegram",
        dict(event_name=TelegramCommonEvent.inline_query, callback_object=message),
    )

    raise ContinuePropagation


def with_handle_event(handle_event: Callable, handler: Callable):
    """
    avoid circlely import caused by `handle_event`

    pass `handle_event` as parameter to avoid multiple times import
    """

    async def wrapper(client, callback_object):
        return await handler(client, callback_object, handle_event)

    return wrapper


def register_telegram_event(pyrogram_client: Client):
    from pepperbot.core.event.handle import handle_event

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
