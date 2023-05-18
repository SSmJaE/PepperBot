from typing import List, Type
from pepperbot.adapters.keaimao import KeaimaoAdapter
from pepperbot.adapters.keaimao.event import KeaimaoEvent
from pepperbot.adapters.onebot import OnebotV11Adapter
from pepperbot.adapters.onebot.event import OnebotV11Event
from pepperbot.adapters.telegram import TelegramAdapter
from pepperbot.adapters.telegram.event import TelegramEvent
from pepperbot.adapters.universal import UniversalAdapter
from pepperbot.adapters.universal.event import UniversalEvent
from pepperbot.core.event.base_adapter import BaseAdapter


available_adapters: List[Type[BaseAdapter]] = [
    UniversalAdapter,
    OnebotV11Adapter,
    KeaimaoAdapter,
    TelegramAdapter,
]

ALL_PROTOCOL_EVENT_NAMES = [
    event.protocol_event_name
    for adapter in available_adapters
    for event in adapter.all_events
]


UNIVERSAL_PROTOCOL_EVENT_MAPPING = {
    UniversalEvent.group_message.protocol_event_name: (
        OnebotV11Event.group_message,
        KeaimaoEvent.group_message,
    ),
    UniversalEvent.friend_message.protocol_event_name: [
        OnebotV11Event.friend_message,
        KeaimaoEvent.private_message,
    ],
}
""" 通用事件与协议事件的映射关系 """

COMMAND_TRIGGER_EVENTS = [
    UniversalEvent.group_message,
    OnebotV11Event.group_message,
    KeaimaoEvent.group_message,
    TelegramEvent.group_message,
    UniversalEvent.friend_message,
    UniversalEvent.stranger_message,
    OnebotV11Event.friend_message,
    OnebotV11Event.temporary_message,
    KeaimaoEvent.private_message,
    TelegramEvent.private_message,
]
""" 指令触发事件 """
