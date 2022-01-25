# from __future__ import annotations

from typing import Dict, TYPE_CHECKING, List, Literal

from pepperbot.models.user import *
from pydantic import BaseModel

# if TYPE_CHECKING:
from pepperbot.models.stranger import Stranger


class CommonReturn(BaseModel):
    retcode: int
    status: Literal["ok"]


class get_group_member_list_return(CommonReturn):
    data: List[GroupMember]


class get_group_member_info_return(CommonReturn):
    data: GroupMember


class get_stranger_info_return(CommonReturn):
    # data: Dict
    data: Stranger


get_stranger_info_return.update_forward_refs()


class get_login_info(CommonReturn):
    data: SelfInfo
