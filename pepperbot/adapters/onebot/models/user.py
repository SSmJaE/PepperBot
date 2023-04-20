from typing import Any, Literal, Optional
from pydantic import BaseModel


class UserBase(BaseModel):
    pass


class SelfInfo(UserBase):
    user_id: int
    nickname: str


class User(UserBase):
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
    user_id: int


# todo GroupMemberMixin


class GroupMember(User):
    async def ban(self, duration: int = 30):
        from pepperbot.adapters.onebot.api import OnebotV11API

        await OnebotV11API.set_group_ban(
            str(self.group_id),
            str(self.user_id),
            duration,
        )


class GroupAdmin(User):
    pass


class GroupOwner(User):
    pass


class Stranger(User):
    user_id: Optional[int]
    nickname: Optional[str]
    sex: Optional[Literal["male", "female", "unknown"]]
    age: Optional[int]
    qid: Optional[str]
    level: Optional[str]

    api: Optional[Any] = None
    event: Optional[Any] = None
