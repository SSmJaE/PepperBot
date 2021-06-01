from typing import Any, Optional

from pepperbot.utils.mixins import FriendMixin

from .user import User
from .UserInfo import *


# todo 在pydantic实例化时，挂载event，怎么做？init似乎不行
class Friend(User, FriendMixin):
    api: Optional[Any] = None
    event: Optional[Any] = None

    def __init__(self, api, event: dict):
        super().__init__(**event)

        self.api = api
        self.event = event
