from typing import Dict, List

from pepperbot.store.meta import T_HandlerKwargMapping


class BaseAdapater:
    @staticmethod
    def get_event_name(raw_event: Dict) -> str:
        """根据各个协议，提取事件名称"""
        raise NotImplementedError()

    meta_events: List[str]
    common_events: List[str]
    group_events: List[str]
    private_events: List[str]
    kwargs: T_HandlerKwargMapping
