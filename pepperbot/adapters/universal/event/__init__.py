""" 大多数机器人协议共有的事件 """

from typing import Dict, Union

from pydantic import root_validator

from pepperbot.adapters.universal.api import UniversalGroupBot
from pepperbot.core.message.chain import MessageChain, chain_factory
from pepperbot.store.event import EventHandlerKwarg, ProtocolEvent

group_bot = EventHandlerKwarg(
    name="bot",
    type_=UniversalGroupBot,
    value=lambda bot: bot,
)

raw_event = EventHandlerKwarg(
    name="raw_event",
    type_=Union[Dict, dict],
    value=lambda raw_event: raw_event,
)

chain = EventHandlerKwarg(
    name="chain",
    type_=MessageChain,
    value=chain_factory,
)


class UniversalProtocolEvent(ProtocolEvent):
    @root_validator
    def compute_size(cls, values) -> dict:
        if values["protocol_event_name"] is None:
            values["protocol_event_name"] = values["raw_event_name"]

        values["keyword_arguments"].append(raw_event)

        if "group" in values["event_type"]:
            values["keyword_arguments"].append(group_bot)

        # if "private" in values["event_type"]:
        #     values["keyword_arguments"].append(private_bot)

        for conversation_type in ("message",):
            if conversation_type in values["event_type"]:
                values["keyword_arguments"].append(chain)

        return values


class UniversalEvent:
    group_message = UniversalProtocolEvent(
        event_type=("group", "message"),
        raw_event_name="group_message",
        description="群消息",
    )
    group_join_request = UniversalProtocolEvent(
        event_type=(
            "group",
            "request",
        ),
        raw_event_name="group_join_request",
        description="加群请求",
    )
    been_group_invited = UniversalProtocolEvent(
        event_type=(
            "group",
            "request",
        ),
        raw_event_name="been_group_invited",
        description="被邀请入群",
    )
    group_member_increased = UniversalProtocolEvent(
        event_type=(
            "group",
            "notice",
        ),
        raw_event_name="group_member_increased",
        description="群成员增加",
    )
    group_member_declined = UniversalProtocolEvent(
        event_type=(
            "group",
            "notice",
        ),
        raw_event_name="group_member_declined",
        description="群成员减少",
    )
    friend_message = UniversalProtocolEvent(
        event_type=(
            "private",
            "message",
        ),
        raw_event_name="friend_message",
        description="好友消息",
    )
    stranger_message = UniversalProtocolEvent(
        event_type=(
            "private",
            "message",
        ),
        raw_event_name="stranger_message",
        description="陌生人消息",
    )
