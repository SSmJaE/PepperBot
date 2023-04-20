from typing import Dict

from pydantic import root_validator
from pyrogram.client import Client
from pyrogram.types import CallbackQuery, InlineQuery, Message

from pepperbot.adapters.telegram.api import TelegramGroupBot, TelegramPrivateBot
from pepperbot.core.message.chain import MessageChain, chain_factory
from pepperbot.store.event import EventHandlerKwarg, ProtocolEvent
from pepperbot.store.meta import get_telegram_caller

raw_event = EventHandlerKwarg(
    name="raw_event", type_=Dict, value=lambda raw_event: raw_event
)

client = EventHandlerKwarg(
    name="client",
    type_=Client,
    value=lambda: get_telegram_caller(),
)


class TelegramProtocolEvent(ProtocolEvent):
    @root_validator
    def compute_size(cls, values) -> dict:
        if values["protocol_event_name"] is None:
            values["protocol_event_name"] = f"telegram_{values['raw_event_name']}"

        values["keyword_arguments"].append(raw_event)
        values["keyword_arguments"].append(client)

        # if "group" in values["event_type"]:
        #     values["keyword_arguments"].append(group_bot)

        # if "private" in values["event_type"]:
        #     values["keyword_arguments"].append(private_bot)

        # for conversation_type in ("message",):
        #     if conversation_type in values["event_type"]:
        #         values["keyword_arguments"].append(chain)

        return values


class TelegramEvent:
    raw_update = TelegramProtocolEvent(
        event_type=("meta",),
        raw_event_name="raw_update",
        description="",
    )

    inline_query = TelegramProtocolEvent(
        event_type=("message",),
        raw_event_name="inline_query",
        description="",
        keyword_arguments=[
            EventHandlerKwarg(
                name="inline_query",
                type_=InlineQuery,
                value=lambda raw_event: raw_event["callback_object"],
            ),
        ],
    )

    callback_query = TelegramProtocolEvent(
        event_type=("message",),
        raw_event_name="callback_query",
        description="",
        keyword_arguments=[
            EventHandlerKwarg(
                name="callback_query",
                type_=CallbackQuery,
                value=lambda raw_event: raw_event["callback_object"],
            ),
        ],
    )

    edited_message = TelegramProtocolEvent(
        event_type=("message",),
        raw_event_name="edited_message",
        description="",
        keyword_arguments=[
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
    )

    private_message = TelegramProtocolEvent(
        event_type=("message", "private"),
        raw_event_name="private_message",
        description="",
        keyword_arguments=[
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
    )

    group_message = TelegramProtocolEvent(
        event_type=("message", "group"),
        raw_event_name="group_message",
        description="",
        keyword_arguments=[
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
    )

    chosen_inline_result = TelegramProtocolEvent(
        event_type=("message", "private"),
        raw_event_name="chosen_inline_result",
        description="",
    )
