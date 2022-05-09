from typing import Dict, List

from pepperbot.store.meta import T_HandlerKwargMapping
from pepperbot.types import T_RouteMode


class BaseAdapater:
    @staticmethod
    def get_event_name(raw_event: Dict) -> str:
        """根据各个协议，提取事件名称"""
        raise NotImplementedError

    @staticmethod
    def get_route_mode(raw_event: Dict, raw_event_name: str) -> T_RouteMode:
        raise NotImplementedError

    @staticmethod
    def get_source_id(raw_event: Dict, mode: T_RouteMode) -> str:
        raise NotImplementedError

    meta_events: List[str]
    common_events: List[str]
    group_events: List[str]
    private_events: List[str]
    all_events: List[str]

    kwargs: T_HandlerKwargMapping
