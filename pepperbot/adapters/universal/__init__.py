from typing import List, cast
from pepperbot.adapters.onebot.event import OnebotV11Event
from pepperbot.adapters.universal.event import UniversalEvent
from pepperbot.core.event.base_adapter import BaseAdapter
from pepperbot.store.event import ProtocolEvent, filter_event_by_type
from pepperbot.utils.common import get_own_attributes

own_attributes = get_own_attributes(UniversalEvent)

events: List[ProtocolEvent] = [getattr(UniversalEvent, attr) for attr in own_attributes]


class UniversalAdapter(BaseAdapter):
    kwargs_mapping = {
        cast(str, event.protocol_event_name): event.keyword_arguments
        for event in events
    }

    all_events = events
    meta_events = filter_event_by_type(events, ("meta",))
    notice_events = filter_event_by_type(events, ("notice",))
    request_events = filter_event_by_type(events, ("request",))
    message_events = filter_event_by_type(events, ("message",))
    group_events = filter_event_by_type(events, ("group",))
    private_events = filter_event_by_type(events, ("private",))
