from enum import Enum, unique
from typing import Any, List, Literal, Union


# @unique
class GroupEvent:
    # 针对群
    group_message: Literal["group_message"] = "group_message"
    group_anonymous_essage: Literal["group_anonymous_essage"] = "group_anonymous_essage"
    group_notice: Literal["group_notice"] = "group_notice"
    group_message_been_withdraw: Literal[
        "group_message_been_withdraw"
    ] = "group_message_been_withdraw"
    group_honor_change: Literal["group_honor_change"] = "group_honor_change"
    group_admin_change: Literal["group_admin_change"] = "group_admin_change"
    group_ban_change: Literal["group_ban_change"] = "group_ban_change"
    member_increased: Literal["member_increased"] = "member_increased"
    member_declined: Literal["member_declined"] = "member_declined"
    new_file_uploaded: Literal["new_file_uploaded"] = "new_file_uploaded"
    add_group: Literal["add_group"] = "add_group"
    # 针对个人，群相关
    been_group_poked: Literal["been_group_poked"] = "been_group_poked"
    been_invited: Literal["been_invited"] = "been_invited"
    # 针对个人，个人相关
    been_added: Literal["been_added"] = "been_added"
    friend_message: Literal["friend_message"] = "friend_message"
    been_friend_poked: Literal["been_friend_poked"] = "been_friend_poked"
    friend_message_been_withdraw: Literal[
        "friend_message_been_withdraw"
    ] = "friend_message_been_withdraw"
    temp_message: Literal["temp_message"] = "temp_message"
    # 其它
    meta_event: Literal["meta_event"] = "meta_event"


RELATIONS = {
    "group": {
        "GroupMessage": [
            GroupEvent.group_message,
            GroupEvent.group_anonymous_essage,
        ],
        "GroupNotice": [
            GroupEvent.group_notice,
            GroupEvent.group_message_been_withdraw,
            GroupEvent.group_admin_change,
            GroupEvent.group_ban_change,
            GroupEvent.group_honor_change,
            GroupEvent.member_increased,
            GroupEvent.member_declined,
            GroupEvent.new_file_uploaded,
            GroupEvent.been_group_poked,
        ],
        "GroupRequest": [GroupEvent.add_group, GroupEvent.been_invited],
    },
    "friend": [
        {
            "FriendMessage": [
                GroupEvent.friend_message,
            ],
            "FriendRequest": [GroupEvent.been_added],
            "FriendNotice": [
                GroupEvent.been_friend_poked,
                GroupEvent.friend_message_been_withdraw,
            ],
        }
    ],
    "temp": [GroupEvent.temp_message],
}


GROUP_EVENTS_T = Literal[
    "group_message",
    "group_anonymous_essage",
    "group_notice",
    "group_message_been_withdraw",
    "group_honor_change",
    "group_admin_change",
    "group_ban_change",
    "member_increased",
    "member_declined",
    "new_file_uploaded",
    "add_group",
    "been_group_poked",
    "been_invited",
    "been_added",
    "friend_message",
    "been_friend_poked",
    "friend_message_been_withdraw",
    "temp_message",
    "meta_event",
]


def get_parent_level(bottomGroupEvent: Union[str, Any]):
    for key, value in RELATIONS["group"].items():
        if bottomGroupEvent in value:
            return key

    raise Exception("无效事件")


GROUP_EVENTS: List[str] = []

for _, subTypes in RELATIONS["group"].items():
    GROUP_EVENTS.extend(subTypes)

GROUP_EVENTS_WITH_LIFECYCLE = [*GROUP_EVENTS]
for event in GROUP_EVENTS:
    GROUP_EVENTS_WITH_LIFECYCLE.append("before_" + event)
    GROUP_EVENTS_WITH_LIFECYCLE.append("after_" + event)


def is_group_event(event: str) -> bool:
    return event in GROUP_EVENTS


def is_valid_group_method(methodName: str):
    return methodName in GROUP_EVENTS_WITH_LIFECYCLE
