from .User import User
from pydantic import BaseModel


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
