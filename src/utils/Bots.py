from src.utils.Mixins import *


class GroupMessageBot(GroupMessageMixin):
    def __init__(self, api, groupId) -> None:
        self.api = api
        self.groupId = groupId

# todo 加群信息只能获取到qq号和群号
# 获取不到用户信息，
# 找一个接口，可以查询到用户信息
# 这样就可以通过用户名来判断，是否允许加群


class GroupMemberBot(GroupMemberMixin):
    def __init__(self, api, groupId) -> None:
        self.api = api
        self.groupId = groupId


class GroupRequestBot(GroupRequestMixin):
    def __init__(self, api, flag) -> None:
        self.api = api
        self.flag = flag
