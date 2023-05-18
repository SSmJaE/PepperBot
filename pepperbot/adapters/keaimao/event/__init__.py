# https://www.kancloud.cn/yangtaott/dsaw/1179271

from typing import Dict, Union

from pydantic import root_validator

from pepperbot.adapters.keaimao.api import KeaimaoGroupBot, KeaimaoPrivateBot
from pepperbot.core.message.chain import MessageChain, chain_factory
from pepperbot.store.event import EventHandlerKwarg, ProtocolEvent

raw_event = EventHandlerKwarg(
    name="raw_event",
    type_=Union[Dict, dict],
    value=lambda raw_event: raw_event,
)

group_bot = EventHandlerKwarg(
    name="bot",
    type_=KeaimaoGroupBot,
    value=lambda bot: bot,
)

private_bot = EventHandlerKwarg(
    name="bot",
    type_=KeaimaoPrivateBot,
    value=lambda bot: bot,
)

chain = EventHandlerKwarg(
    name="chain",
    type_=MessageChain,
    value=chain_factory,
)


class KeaimaoProtocolEvent(ProtocolEvent):
    @root_validator
    def compute_size(cls, values) -> dict:
        if values["protocol_event_name"] is None:
            values["protocol_event_name"] = f"keaimao_{values['raw_event_name']}"

        values["keyword_arguments"].append(raw_event)

        if "group" in values["event_type"]:
            values["keyword_arguments"].append(group_bot)

        if "private" in values["event_type"]:
            values["keyword_arguments"].append(private_bot)

        for conversation_type in ("message",):
            if conversation_type in values["event_type"]:
                values["keyword_arguments"].append(chain)

        return values


class KeaimaoEvent:
    group_message = KeaimaoProtocolEvent(
        event_type=("group", "message"),
        raw_event_name="group_message",
        description="",
    )

    private_message = KeaimaoProtocolEvent(
        event_type=("private", "message"),
        raw_event_name="private_message",
        description="",
    )

    EventAcceptAccounts = KeaimaoProtocolEvent(
        event_type=("meta",),
        raw_event_name="EventAcceptAccounts",
        description="",
    )

    EventSysMsg = KeaimaoProtocolEvent(
        event_type=("meta",),
        raw_event_name="EventSysMsg",
        description="",
    )

    EventAddGroupMember = KeaimaoProtocolEvent(
        event_type=("group",),
        raw_event_name="EventAddGroupMember",
        description="",
    )

    EventDecreaseGroupMember = KeaimaoProtocolEvent(
        event_type=("group",),
        raw_event_name="EventDecreaseGroupMember",
        description="",
    )

    FriendVerify = KeaimaoProtocolEvent(
        event_type=("private",),
        raw_event_name="FriendVerify",
        description="",
    )
