from typing import Any, Literal, Optional

from .user import User


class Stranger(User):
    user_id: Optional[int]
    nickname: Optional[str]
    sex: Optional[Literal["male", "female", "unknown"]]
    age: Optional[int]
    qid: Optional[str]
    level: Optional[str]

    api: Optional[Any] = None
    event: Optional[Any] = None
