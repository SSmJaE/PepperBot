from typing import Dict, Optional
from pepperbot.adapters.onebot.event import (
    OnebotV11CommonEvent,
    OnebotV11GroupEvent,
    OnebotV11MetaEvent,
    OnebotV11PrivateEvent,
)
from pepperbot.adapters.onebot.event.kwargs import ONEBOTV11_KWARGS_MAPPING
from pepperbot.core.event.base_adapter import BaseAdapater
from pepperbot.exceptions import EventHandleError
from pepperbot.extensions.log import logger
from pepperbot.types import T_RouteMode
from pepperbot.utils.common import get_own_attributes


class OnebotV11Adapter(BaseAdapater):
    event_prefix = "onebot_"
    meta_events = list(get_own_attributes(OnebotV11MetaEvent))
    common_events = list(get_own_attributes(OnebotV11CommonEvent))
    group_events = list(get_own_attributes(OnebotV11GroupEvent))
    private_events = list(get_own_attributes(OnebotV11PrivateEvent))

    all_events = [*meta_events, *common_events, *group_events, *private_events]

    kwargs = ONEBOTV11_KWARGS_MAPPING

    @staticmethod
    def get_event_name(raw_event: Dict):
        """onebot没有直接的事件名，而是post_type和sub_type，所以手动转发一下"""
        event_name: Optional[str] = None

        post_type = raw_event["post_type"]

        if post_type == "meta_event":
            event_name = OnebotV11MetaEvent.meta_event

        if post_type == "request":
            request_type = raw_event["request_type"]
            sub_type = raw_event.get("sub_type")

            if request_type == "group":
                if sub_type == "add":
                    # logger.info("加群请求")
                    event_name = OnebotV11GroupEvent.add_group

                elif sub_type == "invite":
                    # logger.info("机器人被邀请入群")
                    event_name = OnebotV11GroupEvent.been_invited

            elif request_type == "friend":
                # logger.info("机器人接收到添加好友请求")
                event_name = OnebotV11PrivateEvent.been_added

        if post_type == "notice":
            notice_type = raw_event["notice_type"]
            sub_type = raw_event.get("sub_type")

            if notice_type == "group_increase":
                # logger.info("新成员入群")
                event_name = OnebotV11GroupEvent.member_increased

            elif notice_type == "group_decrease":
                # logger.info("群成员减少")
                event_name = OnebotV11GroupEvent.member_declined

            elif notice_type == "notify":
                if sub_type == "poke":
                    # logger.info("群POKE事件")
                    event_name = OnebotV11GroupEvent.been_group_poked

                if sub_type == "honor":
                    # logger.info("群荣誉变更")
                    event_name = OnebotV11GroupEvent.group_honor_change

        if post_type == "message":
            message_type = raw_event["message_type"]
            sub_type = raw_event.get("sub_type")

            if message_type == "private":

                if sub_type == "friend":
                    # logger.info("好友私聊消息")
                    event_name = OnebotV11PrivateEvent.friend_message

                elif sub_type == "group":
                    # todo 临时会话可能获取不到groupId
                    # logger.info("群临时会话")
                    event_name = OnebotV11PrivateEvent.temp_message

            elif message_type == "group":

                if sub_type == "normal":
                    # logger.info("群普通消息")
                    event_name = OnebotV11GroupEvent.group_message

                elif sub_type == "anonymous":
                    # logger.info("群匿名消息")
                    event_name = OnebotV11GroupEvent.group_anonymous_essage

                elif sub_type == "notice":
                    # logger.info("群通知消息")
                    event_name = OnebotV11GroupEvent.group_notice

        if not event_name:
            raise EventHandleError(f"未能获取onebot事件名称")

        return event_name

    @staticmethod
    def get_route_mode(raw_event: Dict, raw_event_name: str):
        mode: Optional[T_RouteMode] = None

        if raw_event_name in OnebotV11Adapter.group_events:
            mode = "group"
        elif raw_event_name in OnebotV11Adapter.private_events:
            mode = "private"

        return mode

    @staticmethod
    def get_source_id(raw_event: Dict, mode: T_RouteMode):
        source_id: Optional[str] = None

        if mode == "group":
            source_id = raw_event["group_id"]
        elif mode == "private":
            source_id = raw_event["sender"]["user_id"]

        return source_id
