from multiprocessing import Event
from typing import Any, Dict, Union
from pepperbot.adapters.onebot.api import (
    OnebotV11Api,
    OnebotV11GroupBot,
    OnebotV11PrivateBot,
)
from pepperbot.adapters.onebot.event import (
    OnebotV11GroupEvent,
    OnebotV11PrivateEvent,
)
from pepperbot.adapters.onebot.models.user import GroupMember
from pepperbot.store.meta import (
    EventHandlerKwarg,
    T_HandlerKwargMapping,
    EventMeta,
    get_onebot_caller,
)


async def get_group_member_info(raw_event: dict[str, Any]):
    """lambda不支持async，所以得单独搞出来"""
    return await OnebotV11Api.get_group_member_info(
        raw_event["group_id"], raw_event["user_id"]
    )


# async def get_stranger_info(event: Dict[str, Any], userId: int):
#     return await globalApi.stranger(
#         userId=userId,
#     )


def construct_chain(event_meta: EventMeta):
    from pepperbot.core.message.chain import chain_factory

    return chain_factory(event_meta)


# def construct_sender(event: Dict[str, Any]):
#     return Sender(event=event, api=globalApi.api)


# def construct_friend(event: Dict[str, Any]):
#     return Friend(event=event, api=globalApi.api)


# def construct_stranger(event: Dict[str, Any]):
#     return Stranger(event=event, api=globalApi.api)

raw_event = EventHandlerKwarg(
    name="raw_event",
    type_=Union[Dict, dict],
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
common_chain = EventHandlerKwarg(
    name="chain",
    type_="MessageChain",
    value=construct_chain,
    # value=chain_factory,
)

# 所有handler都注入raw_event，所以就不重复写了，最后统一注入
ONEBOTV11_KWARGS_MAPPING: T_HandlerKwargMapping = {
    OnebotV11GroupEvent.group_message: [
        raw_event,
        group_bot,
        common_chain,
        # EventHandlerKwarg(
        #     name="sender",
        #     type_=Sender,
        #     value=lambda event, **kwargs: construct_sender(event),
        # ),
    ],
    OnebotV11GroupEvent.group_anonymous_message: [
        raw_event,
        group_bot,
        common_chain,
        # EventHandlerKwarg(
        #     name="sender",
        #     type_=Sender,
        #     value=lambda event, **kwargs: construct_sender(event),
        # ),
    ],
    OnebotV11GroupEvent.group_message_been_withdraw: [
        raw_event,
        group_bot,
    ],
    OnebotV11GroupEvent.group_honor_change: [
        raw_event,
        group_bot,
    ],
    OnebotV11GroupEvent.group_admin_change: [
        raw_event,
        group_bot,
    ],
    OnebotV11GroupEvent.group_ban_change: [
        raw_event,
        group_bot,
    ],
    OnebotV11GroupEvent.member_increased: [
        raw_event,
        group_bot,
        EventHandlerKwarg(
            name="member",
            type_=GroupMember,
            value=lambda raw_event, **kwargs: get_group_member_info(raw_event),
        ),
    ],
    OnebotV11GroupEvent.member_declined: [
        raw_event,
        group_bot,
        # 退群的时候，获取不到，或者说，该api返回的是None
        # EventHandlerKwarg(
        #     name="member",
        #     type_=GroupMember,
        #     value=lambda raw_event, **kwargs: get_group_member_info(raw_event),
        # ),
    ],
    OnebotV11GroupEvent.new_file_uploaded: [
        raw_event,
        group_bot,
        #     EventHandlerKwarg(
        #         name="member",
        #         type_=GroupMember,
        #         value=lambda event, **kwargs: get_stranger_info(event, event["user_id"]),
        #     ),
    ],
    OnebotV11GroupEvent.group_join_request: [
        raw_event,
        group_bot
        # 这样就可以通过用户名来判断，是否允许加群,
        #     EventHandlerKwarg(
        #         name="member",
        #         type_=GroupMember,
        #         value=lambda event, **kwargs: get_stranger_info(event, event["user_id"]),
        #     ),
    ],
    OnebotV11GroupEvent.been_group_poked: [
        raw_event,
        group_bot,
        #     EventHandlerKwarg(
        #         name="sender",
        #         type_=GroupMember,
        #         value=lambda event, **kwargs: get_member_info(event, event["sender_id"]),
        #     ),
        #     EventHandlerKwarg(
        #         name="target",
        #         type_=GroupMember,
        #         value=lambda event, **kwargs: get_member_info(event, event["target_id"]),
        #     ),
    ],
    OnebotV11GroupEvent.been_invited: [
        raw_event,
        group_bot,
        #     EventHandlerKwarg(
        #         name="sender",
        #         type_=GroupMember,
        #         value=lambda event, **kwargs: get_member_info(event, event["sender_id"]),
        #     ),
        #     EventHandlerKwarg(
        #         name="target",
        #         type_=GroupMember,
        #         value=lambda event, **kwargs: get_member_info(event, event["target_id"]),
        #     ),
    ],
    OnebotV11PrivateEvent.been_added: [
        raw_event,
        private_bot,
        #     EventHandlerKwarg(
        #         name="stranger",
        #         type_=Stranger,
        #         value=lambda event, **kwargs: get_stranger_info(event, event["user_id"]),
        #     ),
        #     EventHandlerKwarg(
        #         name="comment", type_=str, value=lambda event, **kwargs: event["comment"]
        #     ),
    ],
    OnebotV11PrivateEvent.been_friend_poked: [
        raw_event,
        private_bot,
        #     EventHandlerKwarg(
        #         name="sender",
        #         type_=GroupMember,
        #         value=lambda event, **kwargs: get_member_info(event, event["sender_id"]),
        #     ),
        #     EventHandlerKwarg(
        #         name="target",
        #         type_=GroupMember,
        #         value=lambda event, **kwargs: get_member_info(event, event["target_id"]),
        #     ),
    ],
    OnebotV11PrivateEvent.temp_message: [
        raw_event,
        private_bot,
        common_chain,
        # EventHandlerKwarg(
        #     name="friend",
        #     type_=Friend,
        #     value=lambda event, **kwargs: construct_friend(event),
        # ),
        #     EventHandlerKwarg(
        #         name="chain",
        #         type_=MessageChain,
        #         value=lambda event, **kwargs: construct_chain(event, groupId=None),
        #     ),
        #     EventHandlerKwarg(
        #         name="stranger",
        #         type_=Stranger,
        #         value=lambda event, **kwargs: get_stranger_info(event, event["user_id"]),
        #     ),
        #     EventHandlerKwarg(
        #         name="group_id",
        #         type_=int,
        #         value=lambda event, **_: event["sender"]["group_id"],
        #     ),
    ],
    OnebotV11PrivateEvent.friend_message: [
        raw_event,
        private_bot,
        common_chain,
        # EventHandlerKwarg(
        #     name="friend",
        #     type_=Friend,
        #     value=lambda event, **kwargs: construct_friend(event),
        # ),
    ],
    OnebotV11PrivateEvent.friend_message_been_withdraw: [
        raw_event,
        private_bot,
        common_chain,
        # EventHandlerKwarg(
        #     name="friend",
        #     type_=Friend,
        #     value=lambda event, **kwargs: construct_friend(event),
        # ),
    ],
}
