from typing import Dict, List, Optional, cast

from pepperbot.adapters.keaimao.event import KeaimaoEvent
from pepperbot.core.event.base_adapter import BaseAdapter
from pepperbot.exceptions import EventHandleError
from pepperbot.store.event import ProtocolEvent, filter_event_by_type
from pepperbot.types import T_ConversationType
from pepperbot.utils.common import get_own_attributes

own_attributes = get_own_attributes(KeaimaoEvent)

events: List[ProtocolEvent] = [getattr(KeaimaoEvent, attr) for attr in own_attributes]


class KeaimaoAdapter(BaseAdapter):
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
        event: Optional[ProtocolEvent] = None

        event_name = raw_event["event"]

        if event_name == "EventFriendMsg":
            event = KeaimaoEvent.private_message
        elif event_name == "EventGroupMsg":
            event = KeaimaoEvent.group_message

        if not event:
            raise EventHandleError(f"未能获取可爱猫事件名称")

        return event

    @staticmethod
    def get_conversation_type(raw_event: Dict, raw_event_name: str):
        mode: Optional[T_ConversationType] = None

        if raw_event_name in KeaimaoAdapter.group_events:
            mode = "group"
        elif raw_event_name in KeaimaoAdapter.private_events:
            mode = "private"

        return mode

    @staticmethod
    def get_source_id(raw_event: Dict, mode: T_ConversationType):
        source_id: Optional[str] = None

        if mode == "group":
            source_id = raw_event["from_wxid"]
            # from_wxid为群号
            # final_from_wxid为发言群员id
        elif mode == "private":
            source_id = raw_event["final_from_wxid"]

        return source_id
