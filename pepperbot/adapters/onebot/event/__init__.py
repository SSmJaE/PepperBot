# https://docs.go-cqhttp.org/event/#%E5%8A%A0%E5%A5%BD%E5%8F%8B%E8%AF%B7%E6%B1%82

from enum import Enum, unique
from typing import Any, List, Literal, Union


class OnebotV11MetaEvent:
    meta_event = "meta_event"
    on_connect = "on_connect"


# ONEBOTV11_META_EVENTS = [
#     "meta_event",
#     "on_connect",
# ]


class OnebotV11CommonEvent:
    pass


# ONEBOTV11_COMMON_EVENTS = []

# @unique
class OnebotV11GroupEvent:
    # 针对群
    group_message = "group_message"
    group_anonymous_message = "group_anonymous_message"
    group_notice = "group_notice"
    group_message_been_withdraw = "group_message_been_withdraw"
    group_honor_change = "group_honor_change"
    group_admin_change = "group_admin_change"
    group_ban_change = "group_ban_change"
    member_increased = "member_increased"
    member_declined = "member_declined"
    new_file_uploaded = "new_file_uploaded"
    group_join_request = "group_join_request"
    # 针对个人，群相关
    been_group_poked = "been_group_poked"
    been_invited = "been_invited"


class OnebotV11EventComments:
    """自动生成文档用"""

    group_message = (
        "群普通消息 [原始事件的字段定义]"
        + "(https://docs.go-cqhttp.org/event/#%E7%BE%A4%E6%B6%88%E6%81%AF)"
    )
    group_anonymous_message = (
        "群匿名消息  [原始事件的字段定义]"
        + "(https://docs.go-cqhttp.org/event/#%E7%BE%A4%E6%B6%88%E6%81%AF)"
    )
    # group_notice = "群通知消息  [原始事件的字段定义]" + "()"
    group_message_been_withdraw = "尚未实现"
    group_honor_change = (
        "群荣誉变更  [原始事件的字段定义]"
        + "(https://docs.go-cqhttp.org/event/#%E7%BE%A4%E6%88%90%E5%91%98%E8%8D%A3%E8%AA%89%E5%8F%98%E6%9B%B4%E6%8F%90%E7%A4%BA)"
    )
    group_admin_change = "尚未实现"
    group_ban_change = "尚未实现"
    member_increased = (
        "新成员入群  [原始事件的字段定义]"
        + "(https://docs.go-cqhttp.org/event/#%E7%BE%A4%E6%88%90%E5%91%98%E5%A2%9E%E5%8A%A0)"
    )
    member_declined = (
        "群成员减少  [原始事件的字段定义]"
        + "(https://docs.go-cqhttp.org/event/#%E7%BE%A4%E6%88%90%E5%91%98%E5%87%8F%E5%B0%91)"
    )
    new_file_uploaded = "尚未实现"
    group_join_request = (
        "加群请求  [原始事件的字段定义]"
        + "(https://docs.go-cqhttp.org/event/#%E5%8A%A0%E7%BE%A4%E8%AF%B7%E6%B1%82-%E9%82%80%E8%AF%B7)"
    )
    # 针对个人，群相关
    been_group_poked = (
        "群POKE事件  [原始事件的字段定义]"
        + "(https://docs.go-cqhttp.org/event/#%E7%BE%A4%E5%86%85%E6%88%B3%E4%B8%80%E6%88%B3)"
    )
    been_invited = (
        "机器人被邀请入群 [原始事件的字段定义]"
        + "(https://docs.go-cqhttp.org/event/#%E5%8A%A0%E7%BE%A4%E8%AF%B7%E6%B1%82-%E9%82%80%E8%AF%B7)"
    )

    been_added = (
        "机器人接收到添加好友请求  [原始事件的字段定义]"
        + "(https://docs.go-cqhttp.org/event/#%E5%8A%A0%E5%A5%BD%E5%8F%8B%E8%AF%B7%E6%B1%82)"
    )
    been_friend_poked = "尚未实现"
    temp_message = (
        "群临时会话  [原始事件的字段定义]"
        + "(https://docs.go-cqhttp.org/event/#%E7%A7%81%E8%81%8A%E6%B6%88%E6%81%AF)"
    )
    friend_message = (
        "好友私聊消息  [原始事件的字段定义]"
        + "(https://docs.go-cqhttp.org/event/#%E7%A7%81%E8%81%8A%E6%B6%88%E6%81%AF)"
    )
    friend_message_been_withdraw = "尚未实现"


class OnebotV11PrivateEvent:
    # 针对个人，个人相关
    been_added = "been_added"
    been_friend_poked = "been_friend_poked"
    temp_message = "temp_message"
    friend_message = "friend_message"
    friend_message_been_withdraw = "friend_message_been_withdraw"


# RELATIONS = {
#     "group": {
#         "GroupMessage": [
#             GroupEvent.group_message,
#             GroupEvent.group_anonymous_essage,
#         ],
#         "GroupNotice": [
#             GroupEvent.group_notice,
#             GroupEvent.group_message_been_withdraw,
#             GroupEvent.group_admin_change,
#             GroupEvent.group_ban_change,
#             GroupEvent.group_honor_change,
#             GroupEvent.member_increased,
#             GroupEvent.member_declined,
#             GroupEvent.new_file_uploaded,
#             GroupEvent.been_group_poked,
#         ],
#         "GroupRequest": [
#             GroupEvent.add_group,
#             GroupEvent.been_invited,
#         ],
#     },
#     "private": {
#         "FriendMessage": [
#             GroupEvent.friend_message,
#             GroupEvent.temp_message,
#         ],
#         "FriendRequest": [
#             GroupEvent.been_added,
#         ],
#         "FriendNotice": [
#             GroupEvent.been_friend_poked,
#             GroupEvent.friend_message_been_withdraw,
#         ],
#     },
# }


# def get_parent_level(bottomGroupEvent: Union[str, Any]):
#     for key, value in RELATIONS["group"].items():
#         if bottomGroupEvent in value:
#             return key

#     raise Exception("无效事件")


# GROUP_EVENTS: List[str] = []

# for _, subTypes in RELATIONS["group"].items():
#     GROUP_EVENTS.extend(subTypes)

# GROUP_EVENTS_WITH_LIFECYCLE = [*GROUP_EVENTS]
# for event in GROUP_EVENTS:
#     GROUP_EVENTS_WITH_LIFECYCLE.append("before_" + event)
#     GROUP_EVENTS_WITH_LIFECYCLE.append("after_" + event)


# def is_group_event(event: str) -> bool:
#     return event in GROUP_EVENTS


# def is_valid_group_method(methodName: str):
#     return methodName in GROUP_EVENTS_WITH_LIFECYCLE


# FRIEND_EVENTS: List[str] = []

# for _, subTypes in RELATIONS["friend"].items():
#     FRIEND_EVENTS.extend(subTypes)

# FRIEND_EVENTS_WITH_LIFECYCLE = [*FRIEND_EVENTS]
# for event in GROUP_EVENTS:
#     FRIEND_EVENTS_WITH_LIFECYCLE.append("before_" + event)
#     FRIEND_EVENTS_WITH_LIFECYCLE.append("after_" + event)


# def is_friend_event(event: str) -> bool:
#     return event in FRIEND_EVENTS


# def is_valid_friend_method(methodName: str):
#     return methodName in FRIEND_EVENTS_WITH_LIFECYCLE
