from typing import Dict
from pepperbot.adapters.onebot.api import OnebotV11GroupBot, OnebotV11PrivateBot
from pepperbot.adapters.onebot.event.event import (
    OnebotV11GroupEvent,
    OnebotV11PrivateEvent,
)
from pepperbot.store.meta import EventHandlerKwarg, T_HandlerKwargMapping

# # 双重awaitable，因为不支持async lambda
# async def get_member_info(event: Dict[str, Any], userId: int):
#     return await globalApi.member(
#         groupId=event["group_id"],
#         userId=userId,
#     )


# async def get_stranger_info(event: Dict[str, Any], userId: int):
#     return await globalApi.stranger(
#         userId=userId,
#     )


def construct_chain(protocol, mode, raw_event, source_id):
    from pepperbot.core.message.chain import MessageChain

    return MessageChain(protocol, mode, raw_event, source_id)


# def construct_sender(event: Dict[str, Any]):
#     return Sender(event=event, api=globalApi.api)


# def construct_friend(event: Dict[str, Any]):
#     return Friend(event=event, api=globalApi.api)


# def construct_stranger(event: Dict[str, Any]):
#     return Stranger(event=event, api=globalApi.api)

raw_event = EventHandlerKwarg(
    name="raw_event", type_=Dict, value=lambda raw_event: raw_event
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
)

# 所有handler都注入raw_event，所以就不重复写了，最后统一注入
ONEBOTV11_KWARGS_MAPPING: T_HandlerKwargMapping = {
    # OnebotV11GroupEvent.been_group_poked: [
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
    # ],
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
    # OnebotV11GroupEvent.temp_message: [
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
    # ],
    # OnebotV11GroupEvent.member_increased: [
    #     EventHandlerKwarg(
    #         name="member",
    #         type_=GroupMember,
    #         value=lambda event, **kwargs: get_member_info(event, event["user_id"]),
    #     ),
    # ],
    # OnebotV11GroupEvent.member_declined: [
    #     EventHandlerKwarg(
    #         name="member",
    #         type_=GroupMember,
    #         value=lambda event, **kwargs: get_stranger_info(event, event["user_id"]),
    #     ),
    # ],
    # OnebotV11GroupEvent.group_honor_change: [
    #     EventHandlerKwarg(
    #         name="member",
    #         type_=GroupMember,
    #         value=lambda event, **kwargs: get_member_info(event, event["user_id"]),
    #     ),
    # ],
    # OnebotV11GroupEvent.add_group: [
    #     # 这样就可以通过用户名来判断，是否允许加群
    #     EventHandlerKwarg(
    #         name="stranger",
    #         type_=Stranger,
    #         value=lambda event, **kwargs: get_stranger_info(event, event["user_id"]),
    #     ),
    # ],
    # OnebotV11GroupEvent.been_added: [
    #     EventHandlerKwarg(
    #         name="stranger",
    #         type_=Stranger,
    #         value=lambda event, **kwargs: get_stranger_info(event, event["user_id"]),
    #     ),
    #     EventHandlerKwarg(
    #         name="comment", type_=str, value=lambda event, **kwargs: event["comment"]
    #     ),
    # ],
}
