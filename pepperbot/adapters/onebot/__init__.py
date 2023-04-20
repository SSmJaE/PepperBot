from typing import Dict, Optional, cast

import arrow
from pepperbot.adapters.onebot.event import OnebotV11Event
from pepperbot.core.event.base_adapter import BaseAdapter
from pepperbot.exceptions import EventHandleError
from pepperbot.extensions.log import logger
from pepperbot.store.event import ProtocolEvent, filter_event_by_type
from pepperbot.store.meta import LAST_ONEBOT_HEARTBEAT_TIME
from pepperbot.store.orm import get_metadata
from pepperbot.types import T_ConversationType
from pepperbot.utils.common import get_own_attributes


own_attributes = get_own_attributes(OnebotV11Event)

events: list[ProtocolEvent] = [getattr(OnebotV11Event, attr) for attr in own_attributes]


class OnebotV11Adapter(BaseAdapter):
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
        """onebot没有直接的事件名，而是post_type和sub_type，所以手动转发一下"""
        event: Optional[ProtocolEvent] = None

        post_type = raw_event["post_type"]

        if post_type == "meta_event":
            if raw_event["meta_event_type"] == "heartbeat":
                event = OnebotV11Event.heartbeat

            elif raw_event.get("sub_type") == "connect":
                event = OnebotV11Event.on_connect

        if post_type == "request":
            request_type = raw_event["request_type"]
            sub_type = raw_event.get("sub_type")

            if request_type == "group":
                if sub_type == "add":
                    # logger.info("加群请求")
                    event = OnebotV11Event.group_join_request

                elif sub_type == "invite":
                    # logger.info("机器人被邀请入群")
                    event = OnebotV11Event.been_group_invited

            elif request_type == "friend":
                # logger.info("机器人接收到添加好友请求")
                event = OnebotV11Event.been_friend_added

        if post_type == "notice":
            notice_type = raw_event["notice_type"]
            sub_type = raw_event.get("sub_type")

            if notice_type == "group_increase":
                # logger.info("新成员入群")
                event = OnebotV11Event.group_member_increased

            elif notice_type == "group_decrease":
                # logger.info("群成员减少")
                event = OnebotV11Event.group_member_declined

            elif notice_type == "notify":
                if sub_type == "poke":
                    # logger.info("群POKE事件")
                    event = OnebotV11Event.been_group_poked

                if sub_type == "honor":
                    # logger.info("群荣誉变更")
                    event = OnebotV11Event.group_honor_change

        if post_type == "message":
            message_type = raw_event["message_type"]
            sub_type = raw_event.get("sub_type")

            if message_type == "private":
                if sub_type == "friend":
                    # logger.info("好友私聊消息")
                    event = OnebotV11Event.friend_message

                elif sub_type == "group":
                    # todo 临时会话可能获取不到groupId
                    # logger.info("群临时会话")
                    event = OnebotV11Event.temporary_message

            elif message_type == "group":
                if sub_type == "normal":
                    event = OnebotV11Event.group_message

                elif sub_type == "anonymous":
                    event = OnebotV11Event.group_anonymous_message

                # elif sub_type == "notice":
                #     event = OnebotV11Event.group_notice

        if not event:
            raise EventHandleError(f"未能获取onebot事件名称")

        return event

    @staticmethod
    def get_conversation_type(raw_event: dict, protocol_event: ProtocolEvent):
        mode: Optional[T_ConversationType] = None

        if protocol_event in OnebotV11Adapter.group_events:
            mode = "group"
        elif protocol_event in OnebotV11Adapter.private_events:
            mode = "private"

        return mode

    @staticmethod
    def get_source_id(raw_event: Dict, mode: T_ConversationType) -> str:
        source_id: Optional[str] = None

        if mode == "group":
            source_id = raw_event["group_id"]
        elif mode == "private":
            source_id = raw_event["sender"]["user_id"]

        return str(source_id) if source_id else ""

    @staticmethod
    def get_user_id(raw_event: Dict, mode: T_ConversationType) -> str:
        user_id: Optional[str] = None

        try:
            if mode == "group":
                user_id = raw_event["sender"]["user_id"]
            elif mode == "private":
                user_id = raw_event["user_id"]

            return str(user_id) if user_id else ""
        except KeyError:
            # 比如notice之类的事件，没有user_id
            return ""

    @staticmethod
    async def health_check() -> bool:
        last_onebot_heartbeat_time = await get_metadata(
            LAST_ONEBOT_HEARTBEAT_TIME, arrow.now().timestamp()
        )
        current_timestamp = arrow.now().timestamp()

        if current_timestamp - last_onebot_heartbeat_time > 30:
            logger.error("onebot心跳超时，请检查go-cqhttp是否正常运行")
            return False

        return True
