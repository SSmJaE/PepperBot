from typing import Dict
from pepperbot.core.bot.universal import UniversalGroupBot
from pepperbot.core.event.universal import UniversalGroupEvent
from pepperbot.core.message.chain import MessageChain, chain_factory
from pepperbot.store.meta import EventHandlerKwarg, T_HandlerKwargMapping


UNIVERSAL_KWARGS_MAPPING: T_HandlerKwargMapping = {
    UniversalGroupEvent.group_message: [
        EventHandlerKwarg(name="bot", type_=UniversalGroupBot, value=lambda bot: bot),
        EventHandlerKwarg(
            name="raw_event", type_=Dict, value=lambda raw_event: raw_event
        ),
        EventHandlerKwarg(
            name="chain",
            type_=MessageChain,
            value=chain_factory,
        ),
    ]
}
