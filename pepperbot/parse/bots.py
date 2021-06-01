from pepperbot.types import API_Caller_T
from pepperbot.utils.mixins import *


class BotBase:
    pass


class GroupCommonBot(BotBase, GroupMessageMixin, GroupMemberMixin, GroupFileMixin):
    def __init__(self, event: Dict[str, Any], api: API_Caller_T) -> None:
        self.api: API_Caller_T = api
        self.groupId = event["group_id"]


class FriendMessageBot(BotBase, FriendMixin):
    def __init__(self, event: Dict[str, Any], api: API_Caller_T) -> None:
        self.api: API_Caller_T = api
        self.targetId = event["user_id"]


class TempMessageBot(BotBase, FriendMixin):
    def __init__(self, event: Dict[str, Any], api: API_Caller_T) -> None:
        self.api: API_Caller_T = api
        self.targetId = event["user_id"]


class AddGroupBot(BotBase, AddGroupMixin):
    def __init__(self, event: Dict[str, Any], api: API_Caller_T) -> None:
        self.api: API_Caller_T = api
        self.flag = event["flag"]


class BeenAddedBot(BotBase, BeenAddedMixin):
    def __init__(self, event: Dict[str, Any], api: API_Caller_T) -> None:
        self.api: API_Caller_T = api
        self.flag = event["flag"]
