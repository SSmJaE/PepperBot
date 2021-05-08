from typing import Optional
from pydantic import BaseModel


class Stat(BaseModel):
    disconnect_times: int
    last_message_time: int
    lost_times: int
    message_received: int
    message_sent: int
    packet_lost: int
    packet_received: int
    packet_sent: int


class Status(BaseModel):
    app_enabled: bool
    app_good: bool
    app_initialized: bool
    good: bool
    online: bool
    plugins_good: None
    stat: Stat

    class Config:
        arbitrary_types_allowed = True


class MetaEvent(BaseModel):
    interval: int
    meta_event_type: str
    post_type: str
    self_id: int
    status: Optional[Status]
    time: int

    class Config:
        arbitrary_types_allowed = True
