from typing import Dict, List, Sequence
from pepperbot.store.event import EventHandlerKwarg, ProtocolEvent

from pepperbot.types import T_ConversationType


class BaseAdapter:
    kwargs_mapping: Dict[str, Sequence[EventHandlerKwarg]]

    all_events: List[ProtocolEvent]
    all_event_names: List[str]

    meta_events: List[ProtocolEvent]
    meta_event_names: List[str]
    notice_events: List[ProtocolEvent]
    notice_event_names: List[str]
    request_events: List[ProtocolEvent]
    request_event_names: List[str]
    message_events: List[ProtocolEvent]
    message_event_names: List[str]

    private_events: List[ProtocolEvent]
    group_events: List[ProtocolEvent]
    channel_events = List[ProtocolEvent]

    @staticmethod
    def get_event(raw_event: Dict) -> ProtocolEvent:
        """提取事件名称"""
        raise NotImplementedError

    @staticmethod
    def get_conversation_type(
        raw_event: dict, protocol_event: ProtocolEvent
    ) -> T_ConversationType:
        raise NotImplementedError

    @staticmethod
    def get_source_id(raw_event: Dict, mode: T_ConversationType) -> str:
        """提取事件源ID"""
        raise NotImplementedError

    @staticmethod
    def get_user_id(raw_event: Dict, mode: T_ConversationType) -> str:
        """提取用户ID"""
        raise NotImplementedError

    @staticmethod
    async def health_check() -> bool:
        """检查是否正常运行"""
        raise NotImplementedError
