""" 大多数机器人协议共有的事件 """

from pepperbot.adapters.keaimao import KeaimaoAdapter
from pepperbot.adapters.keaimao.event import (
    KeaimaoGroupEvent,
    KeaimaoPrivateEvent,
)
from pepperbot.adapters.onebot import OnebotV11Adapter
from pepperbot.adapters.onebot.event import (
    OnebotV11GroupEvent,
    OnebotV11PrivateEvent,
)
from pepperbot.adapters.telegram import TelegramAdapter
from pepperbot.adapters.telegram.event import TelegramGroupEvent, TelegramPrivateEvent
from pepperbot.utils.common import get_own_attributes


class UniversalMetaEvent:
    pass


class UniversalCommonEvent:
    pass


class UniversalGroupEvent:
    """群事件"""

    group_message = "group_message"
    someone_request_join_group = "someone_request_join_group"
    been_invited_to_group = "been_invited_to_group"
    group_member_increased = "group_member_increased"
    group_member_declined = "group_member_declined"


class UniversalPrivateEvent:
    private_message = "private_message"
    been_added_by_stranger = "been_added_by_stranger"


UNIVERSAL_META_EVENTS = list(get_own_attributes(UniversalMetaEvent))
UNIVERSAL_COMMON_EVENTS = list(get_own_attributes(UniversalCommonEvent))
UNIVERSAL_GROUP_EVENTS = list(get_own_attributes(UniversalGroupEvent))
UNIVERSAL_PRIVATE_EVENTS = list(get_own_attributes(UniversalPrivateEvent))

ALL_UNIVERSAL_EVENTS = [
    *UNIVERSAL_META_EVENTS,
    *UNIVERSAL_COMMON_EVENTS,
    *UNIVERSAL_GROUP_EVENTS,
    *UNIVERSAL_PRIVATE_EVENTS,
]

ALL_ONEBOTV11_EVENTS = [
    *OnebotV11Adapter.meta_events,
    *OnebotV11Adapter.common_events,
    *OnebotV11Adapter.group_events,
    *OnebotV11Adapter.private_events,
]

ALL_KEAIMAO_EVENTS = [
    *KeaimaoAdapter.meta_events,
    *KeaimaoAdapter.common_events,
    *KeaimaoAdapter.group_events,
    *KeaimaoAdapter.private_events,
]

ALL_TELEGRAM_EVENTS = [
    *TelegramAdapter.meta_events,
    *TelegramAdapter.common_events,
    *TelegramAdapter.group_events,
    *TelegramAdapter.private_events,
]

available_adapters = [
    OnebotV11Adapter,
    KeaimaoAdapter,
    TelegramAdapter,
]

ALL_META_EVENTS = [
    *UNIVERSAL_META_EVENTS,
    *[
        adapter.event_prefix + event_name
        for adapter in available_adapters
        for event_name in adapter.meta_events
    ],
]

ALL_COMMON_EVENTS = [
    *UNIVERSAL_COMMON_EVENTS,
    *[
        adapter.event_prefix + event_name
        for adapter in available_adapters
        for event_name in adapter.common_events
    ],
]

ALL_GROUP_EVENTS = [
    *UNIVERSAL_GROUP_EVENTS,
    *[
        adapter.event_prefix + event_name
        for adapter in available_adapters
        for event_name in adapter.group_events
    ],
]

ALL_PRIVATE_EVENTS = [
    *UNIVERSAL_PRIVATE_EVENTS,
    *[
        adapter.event_prefix + event_name
        for adapter in available_adapters
        for event_name in adapter.private_events
    ],
]


UNIVERSAL_PROTOCOL_EVENT_MAPPING = {
    UniversalGroupEvent.group_message: [
        OnebotV11Adapter.event_prefix + OnebotV11GroupEvent.group_message,
        KeaimaoAdapter.event_prefix + KeaimaoGroupEvent.group_message,
    ],
    UniversalPrivateEvent.private_message: [
        OnebotV11Adapter.event_prefix + OnebotV11PrivateEvent.friend_message,
        KeaimaoAdapter.event_prefix + KeaimaoPrivateEvent.private_message,
    ],
}

GROUP_COMMAND_TRIGGER_EVENTS = [
    UniversalGroupEvent.group_message,
    OnebotV11Adapter.event_prefix + OnebotV11GroupEvent.group_message,
    KeaimaoAdapter.event_prefix + KeaimaoGroupEvent.group_message,
    TelegramAdapter.event_prefix + TelegramGroupEvent.group_message,
]

PRIVATE_COMMAND_TRIGGER_EVENTS = [
    UniversalPrivateEvent.private_message,
    OnebotV11Adapter.event_prefix + OnebotV11PrivateEvent.friend_message,
    OnebotV11Adapter.event_prefix + OnebotV11PrivateEvent.temp_message,
    KeaimaoAdapter.event_prefix + KeaimaoPrivateEvent.private_message,
    TelegramAdapter.event_prefix + TelegramPrivateEvent.private_message,
]
