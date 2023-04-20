from pydantic import BaseModel


class GroupInfo(BaseModel):
    pass


from typing import Optional
from pydantic import BaseModel


class InvitedRequest(BaseModel):
    request_id: Optional[int]
    invitor_uin: Optional[int]
    invitor_nick: Optional[str]
    group_id: Optional[int]
    group_name: Optional[str]
    checked: Optional[bool] = False
    actor: Optional[int] = 0


class JoinRequest(BaseModel):
    request_id: Optional[int]
    requester_uin: Optional[int]
    requester_nick: Optional[str]
    message: Optional[str] = ""
    group_id: Optional[int]
    group_name: Optional[str]
    checked: Optional[bool] = False
    actor: Optional[int] = 0
