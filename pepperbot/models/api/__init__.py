from typing import List, Literal

from pepperbot.models.user import *
from pydantic import BaseModel


class CommonReturn(BaseModel):
    retcode: int
    status: Literal["ok"]


class get_group_member_list_return(CommonReturn):
    data: List[GroupMember]


class get_group_member_info_return(CommonReturn):
    data: GroupMember


class get_stranger_info_return(CommonReturn):
    data: Stranger


class get_login_info(CommonReturn):
    data: SelfInfo
