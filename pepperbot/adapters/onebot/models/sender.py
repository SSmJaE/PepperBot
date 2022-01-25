from typing import Any, Optional

from pepperbot.utils.mixins import GroupMemberMixin

from .user import User
from .UserInfo import *


class Sender(User, GroupMemberMixin):
    api: Optional[Any] = None
    event: Optional[Any] = None

    def __init__(self, api, event: dict):
        super().__init__(**event)

        self.api = api
        self.event = event
