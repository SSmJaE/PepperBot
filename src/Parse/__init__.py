from enum import Enum, unique
from typing import Union


# @unique
class GroupEvent:
    # 针对群
    GroupMessage = "GroupMessage"
    GroupAnonymousMessage = "GroupAnonymousMessage"
    GroupNotice = "GroupNotice"
    GroupMessageBeenWithdraw = "GroupMessageBeenWithdraw"
    GroupHonorChange = "GroupHonorChange"
    MemberIncreased = "MemberIncreased"
    MemberDecline = "MemberDecline"
    UploadNewFIle = "uploadNewFIle"
    AdminChange = "adminChange"
    BanChange = "banChange"
    AddGroup = "AddGroup"
    # 针对个人，群相关
    BeenGroupPoked = "BeenGroupPoked"
    BeenInvited = "BeenInvited"
    # 针对个人，个人相关
    BeenAdded = "addFriend"
    FriendMessage = "FriendMessage"
    FriendPokeYou = "FriendPokeYou"
    FriendWithdraw = "FriendWithdraw"
    TempMessage = "TempMessage"
    # 其它
    MetaEvent = "MetaEvent"


RELATIONS = {
    "group": {
        "GroupMessage": [
            "GroupMessage",
            "GroupAnonymousMessage",
        ],
        "GroupNotice": [
            "GroupNotice",
            "GroupMessageBeenWithdraw",
            "MemberIncreased",
            "MemberDecline",
            "uploadNewFIle",
            "adminChange",
            "banChange",
            "BeenGroupPoked",
            GroupEvent.GroupHonorChange,
        ],
        "GroupRequest": ["AddGroup", "BeenInvited"],
    },
    "friend": [
        {
            "FriendMessage": [
                "FriendMessage",
            ],
            "FriendRequest": ["addFriend"],
            "FriendNotice": [
                "FriendPokeYou",
                "FriendWithdraw",
            ],
        }
    ],
    "temp": ["TempMessage"],
}


GROUP_EVENTS_T = Union[
    str
    # Literal[
    # GroupEvent.GroupMessage,
    # GroupEvent.GroupAnonymousMessage,
    # GroupEvent.GroupNotice,
    # GroupEvent.GroupMessageBeenWithdraw,
    # GroupEvent.MemberIncrease,
    # GroupEvent.MemberDecline,
    # GroupEvent.UploadNewFIle,
    # GroupEvent.AdminChange,
    # GroupEvent.BanChange,
    # GroupEvent.GroupPokeYou,
    # GroupEvent.AddGroup,
    # GroupEvent.BeenInvited,
    # GroupEvent.FriendMessage,
    # GroupEvent.BeenAdded,
    # GroupEvent.FriendPokeYou,
    # GroupEvent.FriendWithdraw,
    # GroupEvent.TempMessage,
    # GroupEvent.MetaEvent,
    # ]
]
