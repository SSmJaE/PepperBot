""" 大多数机器人协议共有的事件 """

from pepperbot.adapters.keaimao import KeaimaoAdapter
from pepperbot.adapters.keaimao.event.event import (
    KeaimaoGroupEvent,
    KeaimaoPrivateEvent,
)
from pepperbot.adapters.onebot import OnebotV11Adapter
from pepperbot.adapters.onebot.event.event import (
    OnebotV11GroupEvent,
    OnebotV11PrivateEvent,
)
from pepperbot.utils.common import get_own_attributes


class UniversalMetaEvent:
    pass


class UniversalCommonEvent:
    pass


class UniversalGroupEvent:
    """群事件"""

    group_message = "group_message"
    request_to_enter_the_group = "request_to_enter_the_group"
    been_invited_to_group = "been_invited_to_group"
    group_member_increased = "group_member_increased"
    group_member_declined = "group_member_declined"


class UniversalPrivateEvent:
    friend_message = "friend_message"
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

ALL_META_EVENTS = [
    *UNIVERSAL_META_EVENTS,
    *["onebot_" + event_name for event_name in OnebotV11Adapter.meta_events],
    *["keaimao_" + event_name for event_name in KeaimaoAdapter.meta_events],
]
ALL_COMMON_EVENTS = [
    *UNIVERSAL_COMMON_EVENTS,
    *["onebot_" + event_name for event_name in OnebotV11Adapter.common_events],
    *["keaimao_" + event_name for event_name in KeaimaoAdapter.common_events],
]
ALL_GROUP_EVENTS = [
    *UNIVERSAL_GROUP_EVENTS,
    *["onebot_" + event_name for event_name in OnebotV11Adapter.group_events],
    *["keaimao_" + event_name for event_name in KeaimaoAdapter.group_events],
]
ALL_PRIVATE_EVENTS = [
    *UNIVERSAL_PRIVATE_EVENTS,
    *["onebot_" + event_name for event_name in OnebotV11Adapter.private_events],
    *["keaimao_" + event_name for event_name in KeaimaoAdapter.private_events],
]

# todo
GROUP_COMMAND_TRIGGER_EVENTS = [
    "group_message",
    "onebot_group_message",
    "keaimao_group_message",
]
PRIVATE_COMMAND_TRIGGER_EVENTS = ["friend_message", "onebot_temp_message"]

UNIVERSAL_PROTOCOL_EVENT_MAPPING = {
    UniversalGroupEvent.group_message: [
        "onebot_" + OnebotV11GroupEvent.group_message,
        "keaimao_" + KeaimaoGroupEvent.group_message,
    ],
    UniversalPrivateEvent.friend_message: [
        "onebot_" + OnebotV11PrivateEvent.friend_message,
        "keaimao_" + KeaimaoPrivateEvent.friend_message,
    ],
}
