from typing import Dict, Optional

from pepperbot.adapters.keaimao.event import (
    KeaimaoMetaEvent,
    KeaimaoCommonEvent,
    KeaimaoGroupEvent,
    KeaimaoPrivateEvent,
)
from pepperbot.adapters.keaimao.event.kwargs import KEAIMAO_KWARGS_MAPPING
from pepperbot.core.event.base_adapter import BaseAdapter
from pepperbot.exceptions import EventHandleError
from pepperbot.types import T_RouteMode
from pepperbot.utils.common import get_own_attributes


class KeaimaoAdapter(BaseAdapter):
    event_prefix = "keaimao_"
    meta_events = list(get_own_attributes(KeaimaoMetaEvent))
    common_events = list(get_own_attributes(KeaimaoCommonEvent))
    group_events = list(get_own_attributes(KeaimaoGroupEvent))
    private_events = list(get_own_attributes(KeaimaoPrivateEvent))

    all_events = [*meta_events, *common_events, *group_events, *private_events]

    kwargs = KEAIMAO_KWARGS_MAPPING

    @staticmethod
    def get_event_name(raw_event: Dict):
        event_name: str = ""
        event = raw_event["event"]

        if event == "EventFriendMsg":
            event_name = KeaimaoPrivateEvent.private_message
        elif event == "EventGroupMsg":
            event_name = KeaimaoGroupEvent.group_message

        if not event_name:
            raise EventHandleError(f"未能获取可爱猫事件名称")

        return event_name

    @staticmethod
    def get_route_mode(raw_event: Dict, raw_event_name: str):
        mode: Optional[T_RouteMode] = None

        if raw_event_name in KeaimaoAdapter.group_events:
            mode = "group"
        elif raw_event_name in KeaimaoAdapter.private_events:
            mode = "private"

        return mode

    @staticmethod
    def get_source_id(raw_event: Dict, mode: T_RouteMode):
        source_id: Optional[str] = None

        if mode == "group":
            source_id = raw_event["from_wxid"]
            # from_wxid为群号
            # final_from_wxid为发言群员id
        elif mode == "private":
            source_id = raw_event["final_from_wxid"]

        return source_id
