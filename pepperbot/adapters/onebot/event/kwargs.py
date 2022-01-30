from typing import Dict, List
from pepperbot.adapters.onebot.api import OnebotV11GroupBot
from pepperbot.adapters.onebot.event.event import OnebotV11GroupEvent
# from pepperbot.core.message.chain import MessageChain

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


# def construct_chain(event: Dict[str, Any], groupId) -> MessageChain:
#     return MessageChain(event=event, groupId=groupId, api=globalApi.api)


# def construct_sender(event: Dict[str, Any]):
#     return Sender(event=event, api=globalApi.api)


# def construct_friend(event: Dict[str, Any]):
#     return Friend(event=event, api=globalApi.api)


# def construct_stranger(event: Dict[str, Any]):
#     return Stranger(event=event, api=globalApi.api)


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
        # todo 对kwarg的value也fit_kwargs
        EventHandlerKwarg(
            name="bot",
            type_=OnebotV11GroupBot,
            value=lambda bot: bot,
        ),
        EventHandlerKwarg(
            name="chain",
            type_="MessageChain",
            value=lambda protocol, mode, raw_event, source_id: MessageChain(
                protocol, mode, raw_event, source_id
            ),
        ),
        # EventHandlerKwarg(
        #     name="sender",
        #     type_=Sender,
        #     value=lambda event, **kwargs: construct_sender(event),
        # ),
    ],
    # OnebotV11GroupEvent.friend_message: [
    #     EventHandlerKwarg(
    #         name="friend",
    #         type_=Friend,
    #         value=lambda event, **kwargs: construct_friend(event),
    #     ),
    #     EventHandlerKwarg(
    #         name="chain",
    #         type_=MessageChain,
    #         value=lambda event, **kwargs: construct_chain(event, groupId=None),
    #     ),
    # ],
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
