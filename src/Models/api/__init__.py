from typing import List, Literal

from pydantic import BaseModel
from src.models.user import GroupMember


class get_group_member_list_return(BaseModel):
    data: List[GroupMember]
    retcode: int
    status: Literal["ok"]


class get_group_member_info_return(BaseModel):
    data: GroupMember
    retcode: int
    status: Literal["ok"]


class SelfInfo(BaseModel):
    user_id: int
    nickname: str


class get_login_info(BaseModel):
    data: SelfInfo
    retcode: int
    status: Literal["ok"]
