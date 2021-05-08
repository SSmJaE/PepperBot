from typing_extensions import Literal
from pydantic import BaseModel


class GroupIncreaseEvent(BaseModel):
    group_id: int
    notice_type = "group_increase"
    operator_id: int
    post_type = "notice"
    self_id: int
    sub_type: Literal["approve"]
    time: int
    user_id: int

    class Config:
        arbitrary_types_allowed = True
