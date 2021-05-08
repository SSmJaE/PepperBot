from typing import Optional
from src.Mixins.Mixins import *
from src.User.User import User


class Sender(User, GroupMemberMixin):
    api: Optional[Any] = None
    event: Optional[Any] = None

    def __init__(self, api, event: dict):
        super().__init__(**event)

        self.api = api
        self.event = event
