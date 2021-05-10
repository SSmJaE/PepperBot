from typing import Optional
from pydantic import BaseModel


class User(BaseModel):
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
