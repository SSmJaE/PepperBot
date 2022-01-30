from pepperbot.adapters.keaimao.api import KeaimaoGroupBot
from pepperbot.adapters.keaimao.event.event import KeaimaoGroupEvent
from pepperbot.core.message.chain import MessageChain
from pepperbot.store.meta import EventHandlerKwarg, T_HandlerKwargMapping

KEAIMAO_KWARGS_MAPPING: T_HandlerKwargMapping = {
    KeaimaoGroupEvent.group_message: [
        EventHandlerKwarg(
            name="bot",
            type_=KeaimaoGroupBot,
            value=lambda bot: bot,
        ),
        EventHandlerKwarg(
            name="chain",
            type_=MessageChain,
            value=lambda protocol, mode, raw_event, source_id: MessageChain(
                protocol, mode, raw_event, source_id
            ),
        ),
    ]
}
