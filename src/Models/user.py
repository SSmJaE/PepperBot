from typing import Optional
from pydantic import BaseModel

from src.Mixins.Mixins import *


class UserBase(BaseModel):
    pass


class User(UserBase):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        # self.userId = kwargs["user_id"]
        # self.aaa = 123

    # def __eq__(self, o: "User") -> bool:
    #     return self.userId == o.userId

    age: Optional[int]
    area: Optional[str]
    card: Optional[str]
    card_changeable: Optional[bool]
    group_id: Optional[int]
    join_time: Optional[int]
    last_sent_time: Optional[int]
    level: Optional[str]
    nickname: Optional[str]
    role: Optional[str]
    sex: Optional[str]
    title: Optional[str]
    title_expire_time: Optional[int]
    unfriendly: Optional[bool]
    user_id: Optional[int]


class Stranger(UserBase):
    user_id: int
    nickname: str
    sex: Literal["male", "female", "unknown"]
    age: int
    qid: str


class Friend(UserBase):
    pass


# ---------------------------------------------------------------------------


class GroupMember(User):
    age: int
    area: str
    card: str
    card_changeable: bool
    group_id: int
    join_time: int
    last_sent_time: int
    level: str
    nickname: str
    role: str
    sex: str
    title: str
    title_expire_time: int
    unfriendly: bool
    user_id: int

    def action_test(self):
        print(1)


class GroupAdmin(User):
    pass


class GroupOwner(User):
    pass


class Sender(User, GroupMemberMixin):
    api: Optional[Any] = None
    event: Optional[Any] = None

    def __init__(self, api, event: dict):
        super().__init__(**event)

        self.api = api
        self.event = event
