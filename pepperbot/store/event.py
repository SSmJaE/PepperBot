from typing import Any, Literal, Optional, Sequence, Set
from pydantic import BaseModel

from pepperbot.types import T_BotProtocol, T_ConversationType


class EventHandlerKwarg(BaseModel):
    name: str
    type_: Any
    value: Optional[Any] = None
    """ 
    value可以为嵌套协程，会自动await直到不可await，以获取结果 

    也可以为函数，自动call到un callable，
    
    协程嵌套同步函数再嵌套协程也没有问题
    """


T_EventType = Literal[
    "meta",
    "notice",
    "request",
    "message",
    "private",
    "group",
]


class ProtocolEvent(BaseModel):
    event_type: Sequence[T_EventType]
    raw_event_name: str
    protocol_event_name: Optional[str] = None
    description: str
    keyword_arguments: Sequence[EventHandlerKwarg] = []

    def __hash__(self):
        return hash(self.protocol_event_name)


def filter_event_by_type(
    events: Sequence[ProtocolEvent], target_event_types: Sequence[T_EventType]
) -> list[ProtocolEvent]:
    results: Set[ProtocolEvent] = set()

    for event in events:
        for event_type in event.event_type:
            if event_type in target_event_types:
                results.add(event)

    return list(results)


class EventMetadata(BaseModel):
    protocol: T_BotProtocol
    """ onebot、keaimao、telegram """
    raw_event: dict
    protocol_event: ProtocolEvent
    conversation_type: Optional[T_ConversationType]
    """ conversation_type 
    
    meta event可能获取不到
    """
    source_id: str
    """ group_id( mode == group ) or user_id( mode == private ) """
    user_id: str
    """ user_id """
