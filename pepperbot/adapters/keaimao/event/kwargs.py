from typing import Dict

from pepperbot.adapters.keaimao.api import KeaimaoGroupBot, KeaimaoPrivateBot
from pepperbot.adapters.keaimao.event import KeaimaoGroupEvent, KeaimaoPrivateEvent
from pepperbot.core.message.chain import MessageChain, chain_factory
from pepperbot.store.meta import EventHandlerKwarg, T_HandlerKwargMapping

KEAIMAO_KWARGS_MAPPING: T_HandlerKwargMapping = {
    KeaimaoGroupEvent.group_message: [
        EventHandlerKwarg(
            name="raw_event",
            type_=Dict,
            value=lambda raw_event: raw_event,
        ),
        EventHandlerKwarg(
            name="bot",
            type_=KeaimaoGroupBot,
            value=lambda bot: bot,
        ),
        EventHandlerKwarg(
            name="chain",
            type_=MessageChain,
            value=chain_factory,
        ),
    ],
    KeaimaoPrivateEvent.private_message: [
        EventHandlerKwarg(
            name="raw_event",
            type_=Dict,
            value=lambda raw_event: raw_event,
        ),
        EventHandlerKwarg(
            name="bot",
            type_=KeaimaoPrivateBot,
            value=lambda bot: bot,
        ),
        EventHandlerKwarg(
            name="chain",
            type_=MessageChain,
            value=chain_factory,
        ),
    ],
}
