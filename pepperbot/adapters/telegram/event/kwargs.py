from typing import Dict

from pepperbot.adapters.telegram.api import TelegramGroupBot, TelegramPrivateBot
from pepperbot.adapters.telegram.event import (
    TelegramCommonEvent,
    TelegramGroupEvent,
    TelegramPrivateEvent,
)
from pepperbot.core.message.chain import MessageChain, chain_factory
from pepperbot.store.meta import (
    EventHandlerKwarg,
    T_HandlerKwargMapping,
    get_telegram_caller,
)
from pyrogram.client import Client
from pyrogram.types import Message, InlineQuery, CallbackQuery

TELEGRAM_KWARGS_MAPPING: T_HandlerKwargMapping = {
    TelegramCommonEvent.inline_query: [
        EventHandlerKwarg(
            name="raw_event", type_=Dict, value=lambda raw_event: raw_event
        ),
        EventHandlerKwarg(
            name="client",
            type_=Client,
            value=lambda: get_telegram_caller(),
        ),
        EventHandlerKwarg(
            name="inline_query",
            type_=InlineQuery,
            value=lambda raw_event: raw_event["callback_object"],
        ),
    ],
    TelegramCommonEvent.callback_query: [
        EventHandlerKwarg(
            name="raw_event", type_=Dict, value=lambda raw_event: raw_event
        ),
        EventHandlerKwarg(
            name="client",
            type_=Client,
            value=lambda: get_telegram_caller(),
        ),
        EventHandlerKwarg(
            name="callback_query",
            type_=CallbackQuery,
            value=lambda raw_event: raw_event["callback_object"],
        ),
    ],
    TelegramCommonEvent.edited_message: [
        EventHandlerKwarg(
            name="raw_event", type_=Dict, value=lambda raw_event: raw_event
        ),
        EventHandlerKwarg(
            name="client",
            type_=Client,
            value=lambda: get_telegram_caller(),
        ),
        EventHandlerKwarg(
            name="message",
            type_=Message,
            value=lambda raw_event: raw_event["callback_object"],
        ),
        EventHandlerKwarg(
            name="bot",
            type_=TelegramPrivateBot,
            value=lambda bot: bot,
        ),
        EventHandlerKwarg(
            name="chain",
            type_=MessageChain,
            value=chain_factory,
        ),
    ],
    TelegramPrivateEvent.private_message: [
        EventHandlerKwarg(
            name="raw_event", type_=Dict, value=lambda raw_event: raw_event
        ),
        EventHandlerKwarg(
            name="client",
            type_=Client,
            value=lambda: get_telegram_caller(),
        ),
        EventHandlerKwarg(
            name="message",
            type_=Message,
            value=lambda raw_event: raw_event["callback_object"],
        ),
        EventHandlerKwarg(
            name="bot",
            type_=TelegramPrivateBot,
            value=lambda bot: bot,
        ),
        EventHandlerKwarg(
            name="chain",
            type_=MessageChain,
            value=chain_factory,
        ),
    ],
    TelegramGroupEvent.group_message: [
        EventHandlerKwarg(
            name="raw_event", type_=Dict, value=lambda raw_event: raw_event
        ),
        EventHandlerKwarg(
            name="client",
            type_=Client,
            value=lambda: get_telegram_caller(),
        ),
        EventHandlerKwarg(
            name="message",
            type_=Message,
            value=lambda raw_event: raw_event["callback_object"],
        ),
        EventHandlerKwarg(
            name="bot",
            type_=TelegramGroupBot,
            value=lambda bot: bot,
        ),
        EventHandlerKwarg(
            name="chain",
            type_=MessageChain,
            value=chain_factory,
        ),
    ],
}
