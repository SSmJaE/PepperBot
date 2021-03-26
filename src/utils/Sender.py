from src.utils.MessageChain import *
from src.utils.Mixins import *
from src.utils.User import User


class Sender(User, GroupMemberMixin):
    def __init__(self, api, event: dict):
        super().__init__(**event)

        self.api = api
        self.event = event
