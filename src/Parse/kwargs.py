from src.action.main import *
from src.parse import GROUP_EVENTS_T, GroupEvent
from src.parse.bots import AddGroupBot, GroupCommonBot
from src.types import HandlerValue_T


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


def construct_AddGroupBot(event: Dict[str, Any]) -> AddGroupBot:
    return AddGroupBot(
        event,
        globalApi.api,
    )


# 双重awaitable，因为不支持async lambda
async def get_member_info(event: Dict[str, Any], userId: int):
    return await globalApi.member(
        groupId=event["group_id"],
        userId=userId,
    )


def construct_chain(event: Dict[str, Any], groupId) -> MessageChain:
    return MessageChain(event=event, groupId=groupId, api=globalApi.api)


def construct_sender(event: Dict[str, Any]):
    return Sender(event=event, api=globalApi.api)


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
        # todo 加群信息只能获取到qq号和群号
        # 获取不到用户信息，
        # 找一个接口，可以查询到用户信息
        # 这样就可以通过用户名来判断，是否允许加群
        HandlerKwarg(name="bot", type=AddGroupBot, value=construct_AddGroupBot),
        # HandlerKwarg(
        #     name="member",
        #     type=Sender,
        #     value=lambda event, **kwargs: get_member_info(event, event["user_id"]),
        # ),
    ],
}
