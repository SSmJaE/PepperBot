from typing import Dict

from pepperbot.action.chain import *
from pepperbot.message.chain import MessageChain
from pepperbot.models.friend import Friend
from pepperbot.models.sender import Sender
from pepperbot.models.stranger import Stranger
from pepperbot.parse import GROUP_EVENTS_T, GroupEvent
from pepperbot.parse.bots import (
    AddGroupBot,
    BeenAddedBot,
    FriendMessageBot,
    GroupCommonBot,
    TempMessageBot,
)
from pepperbot.types import HandlerValue_T


class HandlerKwarg(BaseModel):
    name: str
    type: Any
    value: Union[Any]


def construct_GroupCommonBot(event: Dict[str, Any], bot: GroupCommonBot, **kwargs):
    return (
        bot
        if bot
        else GroupCommonBot(
            event,
            globalApi.api,
        )
    )


def construct_AddGroupBot(event: Dict[str, Any], **kwargs):
    return AddGroupBot(
        event,
        globalApi.api,
    )


def construct_BeenAddedBot(event: Dict[str, Any], **kwargs):
    return BeenAddedBot(
        event,
        globalApi.api,
    )


def construct_FriendMessageBot(event: Dict[str, Any], **kwargs):
    return FriendMessageBot(
        event,
        globalApi.api,
    )


def construct_TempMessageBot(event: Dict[str, Any], **kwargs):
    return TempMessageBot(
        event,
        globalApi.api,
    )


# 双重awaitable，因为不支持async lambda
async def get_member_info(event: Dict[str, Any], userId: int):
    return await globalApi.member(
        groupId=event["group_id"],
        userId=userId,
    )


async def get_stranger_info(event: Dict[str, Any], userId: int):
    return await globalApi.stranger(
        userId=userId,
    )


def construct_chain(event: Dict[str, Any], groupId) -> MessageChain:
    return MessageChain(event=event, groupId=groupId, api=globalApi.api)


def construct_sender(event: Dict[str, Any]):
    return Sender(event=event, api=globalApi.api)


def construct_friend(event: Dict[str, Any]):
    return Friend(event=event, api=globalApi.api)


def construct_stranger(event: Dict[str, Any]):
    return Stranger(event=event, api=globalApi.api)


DEFAULT_KWARGS = [
    HandlerKwarg(name="bot", type=GroupCommonBot, value=construct_GroupCommonBot),
]

# 所有handler都注入event:receive，所以就不重复写了，最后统一注入
HANDLER_KWARGS_MAP: Dict[GROUP_EVENTS_T, List[HandlerKwarg]] = {
    GroupEvent.been_group_poked: [
        HandlerKwarg(name="bot", type=GroupCommonBot, value=construct_GroupCommonBot),
        HandlerKwarg(
            name="sender",
            type=GroupMember,
            value=lambda event, **kwargs: get_member_info(event, event["sender_id"]),
        ),
        HandlerKwarg(
            name="target",
            type=GroupMember,
            value=lambda event, **kwargs: get_member_info(event, event["target_id"]),
        ),
    ],
    GroupEvent.group_message: [
        HandlerKwarg(name="bot", type=GroupCommonBot, value=construct_GroupCommonBot),
        HandlerKwarg(
            name="sender",
            type=Sender,
            value=lambda event, **kwargs: construct_sender(event),
        ),
        HandlerKwarg(
            name="chain",
            type=MessageChain,
            value=lambda event, **kwargs: construct_chain(
                event, groupId=event["group_id"]
            ),
        ),
    ],
    GroupEvent.friend_message: [
        HandlerKwarg(
            name="bot", type=FriendMessageBot, value=construct_FriendMessageBot
        ),
        HandlerKwarg(
            name="friend",
            type=Friend,
            value=lambda event, **kwargs: construct_friend(event),
        ),
        HandlerKwarg(
            name="chain",
            type=MessageChain,
            value=lambda event, **kwargs: construct_chain(event, groupId=None),
        ),
    ],
    GroupEvent.temp_message: [
        HandlerKwarg(name="bot", type=TempMessageBot, value=construct_TempMessageBot),
        HandlerKwarg(
            name="chain",
            type=MessageChain,
            value=lambda event, **kwargs: construct_chain(event, groupId=None),
        ),
        HandlerKwarg(
            name="stranger",
            type=Stranger,
            value=lambda event, **kwargs: get_stranger_info(event, event["user_id"]),
        ),
        HandlerKwarg(
            name="groupId",
            type=int,
            value=lambda event, **_: event["sender"]["group_id"],
        ),
    ],
    GroupEvent.member_increased: [
        HandlerKwarg(name="bot", type=GroupCommonBot, value=construct_GroupCommonBot),
        HandlerKwarg(
            name="member",
            type=GroupMember,
            value=lambda event, **kwargs: get_member_info(event, event["user_id"]),
        ),
    ],
    GroupEvent.group_honor_change: [
        HandlerKwarg(name="bot", type=GroupCommonBot, value=construct_GroupCommonBot),
        HandlerKwarg(
            name="member",
            type=GroupMember,
            value=lambda event, **kwargs: get_member_info(event, event["user_id"]),
        ),
    ],
    GroupEvent.add_group: [
        HandlerKwarg(name="bot", type=AddGroupBot, value=construct_AddGroupBot),
        # 这样就可以通过用户名来判断，是否允许加群
        HandlerKwarg(
            name="stranger",
            type=Stranger,
            value=lambda event, **kwargs: get_stranger_info(event, event["user_id"]),
        ),
    ],
    GroupEvent.been_added: [
        HandlerKwarg(name="bot", type=BeenAddedBot, value=construct_AddGroupBot),
        HandlerKwarg(
            name="stranger",
            type=Stranger,
            value=lambda event, **kwargs: get_stranger_info(event, event["user_id"]),
        ),
        HandlerKwarg(
            name="comment", type=str, value=lambda event, **kwargs: event["comment"]
        ),
    ],
}
