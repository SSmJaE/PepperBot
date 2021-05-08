from typing import List, Literal

from pydantic import BaseModel
from src.User import GroupMember


class get_group_member_list_return(BaseModel):
    data: List[GroupMember]
    retcode: int
    status: Literal["ok"]


class get_group_member_info_return(BaseModel):
    data: GroupMember
    retcode: int
    status: Literal["ok"]
