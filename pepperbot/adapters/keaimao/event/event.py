# https://www.kancloud.cn/yangtaott/dsaw/1179271


class KeaimaoMetaEvent:
    pass


class KeaimaoCommonEvent:
    AcceptAccounts = "EventAcceptAccounts"
    SysMsg = "EventSysMsg"


class KeaimaoGroupEvent:
    group_message = "group_message"
    AddGroupMember = "EventAddGroupMember"
    DecreaseGroupMember = "EventDecreaseGroupMember"


class KeaimaoPrivateEvent:
    friend_message = "friend_message"
    FriendVerify = "EventFriendVerify"
