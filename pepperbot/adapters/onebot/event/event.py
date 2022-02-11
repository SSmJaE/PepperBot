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
    group_anonymous_essage = "group_anonymous_essage"
    group_notice = "group_notice"
    group_message_been_withdraw = "group_message_been_withdraw"
    group_honor_change = "group_honor_change"
    group_admin_change = "group_admin_change"
    group_ban_change = "group_ban_change"
    member_increased = "member_increased"
    member_declined = "member_declined"
    new_file_uploaded = "new_file_uploaded"
    add_group = "add_group"
    # 针对个人，群相关
    been_group_poked = "been_group_poked"
    been_invited = "been_invited"


class OnebotV11PrivateEvent:
    # 针对个人，个人相关
    been_added = "been_added"
    friend_message = "friend_message"
    been_friend_poked = "been_friend_poked"
    friend_message_been_withdraw = "friend_message_been_withdraw"
    temp_message = "temp_message"


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
