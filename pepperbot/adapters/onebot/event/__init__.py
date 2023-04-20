from typing import Dict

from pydantic import root_validator

from pepperbot.adapters.onebot.api import (
    OnebotV11API,
    OnebotV11GroupBot,
    OnebotV11PrivateBot,
)
from pepperbot.adapters.onebot.models.user import GroupMember
from pepperbot.store.event import EventHandlerKwarg, EventMetadata, ProtocolEvent


async def get_group_member_info(raw_event: dict):
    """lambda不支持async，所以得单独搞出来"""
    return await OnebotV11API.get_group_member_info(
        raw_event["group_id"], raw_event["user_id"]
    )


def construct_chain(event_meta: EventMetadata):
    from pepperbot.core.message.chain import chain_factory

    return chain_factory(event_meta)


raw_event = EventHandlerKwarg(
    name="raw_event",
    type_=Dict | dict,
    value=lambda raw_event: raw_event,
)
group_bot = EventHandlerKwarg(
    name="bot",
    type_=OnebotV11GroupBot,
    value=lambda bot: bot,
)
private_bot = EventHandlerKwarg(
    name="bot",
    type_=OnebotV11PrivateBot,
    value=lambda bot: bot,
)
chain = EventHandlerKwarg(
    name="chain",
    type_="MessageChain",
    value=construct_chain,
    # value=chain_factory,
)


class OnebotV11ProtocolEvent(ProtocolEvent):
    @root_validator
    def compute_size(cls, values) -> dict:
        if values["protocol_event_name"] is None:
            values["protocol_event_name"] = f"onebot_{values['raw_event_name']}"

        values["keyword_arguments"].append(raw_event)

        if "group" in values["event_type"]:
            values["keyword_arguments"].append(group_bot)

        if "private" in values["event_type"]:
            values["keyword_arguments"].append(private_bot)

        for conversation_type in ("message",):
            if conversation_type in values["event_type"]:
                values["keyword_arguments"].append(chain)

        return values


class OnebotV11Event:
    """https://docs.go-cqhttp.org/event/#%E5%8A%A0%E5%A5%BD%E5%8F%8B%E8%AF%B7%E6%B1%82"""

    on_connect = OnebotV11ProtocolEvent(
        event_type=("meta",),
        raw_event_name="on_connect",
        description="连接成功",
    )
    client_status_change = OnebotV11ProtocolEvent(
        event_type=("meta",),
        raw_event_name="client_status_change",
        description="客户端状态变更",
    )
    heartbeat = OnebotV11ProtocolEvent(
        event_type=("meta",),
        raw_event_name="heartbeat",
        description="心跳",
    )
    group_message = OnebotV11ProtocolEvent(
        event_type=("group", "message"),
        raw_event_name="group_message",
        description=(
            "群普通消息 [原始事件的字段定义]"
            + "(https://docs.go-cqhttp.org/event/#%E7%BE%A4%E6%B6%88%E6%81%AF)"
        ),
        keyword_arguments=[
            EventHandlerKwarg(
                name="member",
                type_=GroupMember,
                value=lambda raw_event, **kwargs: get_group_member_info(raw_event),
            ),
        ],
    )
    group_anonymous_message = OnebotV11ProtocolEvent(
        event_type=("group", "message"),
        raw_event_name="group_anonymous_message",
        description=(
            "群匿名消息  [原始事件的字段定义]"
            + "(https://docs.go-cqhttp.org/event/#%E7%BE%A4%E6%B6%88%E6%81%AF)"
        ),
    )
    group_message_been_withdraw = OnebotV11ProtocolEvent(
        event_type=("group", "notice"),
        raw_event_name="group_message_been_withdraw",
        description="群消息撤回事件",
    )
    group_honor_change = OnebotV11ProtocolEvent(
        event_type=("group",),
        raw_event_name="group_honor_change",
        description=(
            "群荣誉变更  [原始事件的字段定义]"
            + "(https://docs.go-cqhttp.org/event/#%E7%BE%A4%E6%88%90%E5%91%98%E8%8D%A3%E8%AA%89%E5%8F%98%E6%9B%B4%E6%8F%90%E7%A4%BA)"
        ),
    )
    group_admin_change = OnebotV11ProtocolEvent(
        event_type=("group",),
        raw_event_name="group_admin_change",
        description="群管理员变更事件",
    )
    group_ban_change = OnebotV11ProtocolEvent(
        event_type=("group",),
        raw_event_name="group_ban_change",
        description=("")
        + "群禁言事件 [原始事件的字段定义]"
        + "(https://docs.go-cqhttp.org/event/#%E7%BE%A4%E7%A6%81%E8%A8%80%E4%BA%8B%E4%BB%B6)",
    )
    group_member_title_change = OnebotV11ProtocolEvent(
        event_type=("group",),
        raw_event_name="group_member_title_change",
        description="群成员头衔变更事件",
    )
    group_member_card_change = OnebotV11ProtocolEvent(
        event_type=("group",),
        raw_event_name="group_member_card_change",
        description="群成员名片变更事件",
    )
    been_group_poked = OnebotV11ProtocolEvent(
        event_type=("group",),
        raw_event_name="been_group_poked",
        description=(
            "群POKE事件  [原始事件的字段定义]"
            + "(https://docs.go-cqhttp.org/event/#%E7%BE%A4%E5%86%85%E6%88%B3%E4%B8%80%E6%88%B3)"
        ),
    )
    group_lucky_king_notice = OnebotV11ProtocolEvent(
        event_type=("group",),
        raw_event_name="group_lucky_king_notice",
        description="红包运气王通知",
    )
    group_new_file_uploaded = OnebotV11ProtocolEvent(
        event_type=("group",),
        raw_event_name="group_new_file_uploaded",
        description="群文件上传事件",
    )
    been_group_invited = OnebotV11ProtocolEvent(
        event_type=("group",),
        raw_event_name="been_invited",
        description=(
            "机器人被邀请入群 [原始事件的字段定义]"
            + "(https://docs.go-cqhttp.org/event/#%E5%8A%A0%E7%BE%A4%E8%AF%B7%E6%B1%82-%E9%82%80%E8%AF%B7)"
        ),
    )
    group_join_request = OnebotV11ProtocolEvent(
        event_type=("group",),
        raw_event_name="group_join_request",
        description=(
            "加群请求  [原始事件的字段定义]"
            + "(https://docs.go-cqhttp.org/event/#%E5%8A%A0%E7%BE%A4%E8%AF%B7%E6%B1%82-%E9%82%80%E8%AF%B7)"
        ),
    )
    group_member_increased = OnebotV11ProtocolEvent(
        event_type=("group",),
        raw_event_name="group_member_increased",
        description=(
            "新成员入群  [原始事件的字段定义]"
            + "(https://docs.go-cqhttp.org/event/#%E7%BE%A4%E6%88%90%E5%91%98%E5%A2%9E%E5%8A%A0)"
        ),
        keyword_arguments=[
            EventHandlerKwarg(
                name="member",
                type_=GroupMember,
                value=lambda raw_event, **kwargs: get_group_member_info(raw_event),
            ),
        ],
    )
    group_member_declined = OnebotV11ProtocolEvent(
        event_type=("group",),
        raw_event_name="group_member_declined",
        description=(
            "群成员减少  [原始事件的字段定义]"
            + "(https://docs.go-cqhttp.org/event/#%E7%BE%A4%E6%88%90%E5%91%98%E5%87%8F%E5%B0%91)"
        ),
        keyword_arguments=[
            # 退群的时候，获取不到，或者说，该api返回的是None
            # EventHandlerKwarg(
            #     name="member",
            #     type_=GroupMember,
            #     value=lambda raw_event, **kwargs: get_group_member_info(raw_event),
            # ),
        ],
    )
    temporary_message = OnebotV11ProtocolEvent(
        event_type=("private", "message"),
        raw_event_name="temporary_message",
        description=(
            "群临时会话  [原始事件的字段定义]"
            + "(https://docs.go-cqhttp.org/event/#%E7%A7%81%E8%81%8A%E6%B6%88%E6%81%AF)"
        ),
    )
    friend_message = OnebotV11ProtocolEvent(
        event_type=("private", "message"),
        raw_event_name="friend_message",
        description=(
            "好友私聊消息  [原始事件的字段定义]"
            + "(https://docs.go-cqhttp.org/event/#%E7%A7%81%E8%81%8A%E6%B6%88%E6%81%AF)"
        ),
    )
    friend_message_been_withdraw = OnebotV11ProtocolEvent(
        event_type=("private",),
        raw_event_name="friend_message_been_withdraw",
        description="好友私聊消息撤回",
    )
    been_friend_added = OnebotV11ProtocolEvent(
        event_type=("private",),
        raw_event_name="friend_added",
        description=(
            "机器人接收到添加好友请求  [原始事件的字段定义]"
            + "(https://docs.go-cqhttp.org/event/#%E5%8A%A0%E5%A5%BD%E5%8F%8B%E8%AF%B7%E6%B1%82)"
        ),
    )
    been_friend_poked = OnebotV11ProtocolEvent(
        event_type=("private",),
        raw_event_name="friend_poked",
        description="好友戳一戳",
    )


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
