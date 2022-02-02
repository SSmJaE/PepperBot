from typing import Dict

from pepperbot.adapters.keaimao.event.event import (
    KeaimaoCommonEvent,
    KeaimaoGroupEvent,
    KeaimaoMetaEvent,
    KeaimaoPrivateEvent,
)
from pepperbot.adapters.keaimao.event.kwargs import KEAIMAO_KWARGS_MAPPING
from pepperbot.core.event.base_adapter import BaseAdapater
from pepperbot.exceptions import EventHandleError
from pepperbot.utils.common import get_own_attributes


class KeaimaoAdapter(BaseAdapater):
    @staticmethod
    def get_event_name(raw_event: Dict):
        event_name: str = ""
        event = raw_event["event"]

        if event == "EventFriendMsg":
            event_name = KeaimaoPrivateEvent.friend_message
        elif event == "EventGroupMsg":
            event_name = KeaimaoGroupEvent.group_message

        if not event_name:
            raise EventHandleError(f"未能获取可爱猫事件名称")

        return event_name

    meta_events = list(get_own_attributes(KeaimaoMetaEvent))
    common_events = list(get_own_attributes(KeaimaoCommonEvent))
    group_events = list(get_own_attributes(KeaimaoGroupEvent))
    private_events = list(get_own_attributes(KeaimaoPrivateEvent))

    kwargs = KEAIMAO_KWARGS_MAPPING