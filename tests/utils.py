from typing import Dict, Union

from pepperbot.core.message.segment import T_SegmentInstance


async def fake_group_event(*segments: Union[Dict, T_SegmentInstance]):
    message = []

    for segment in segments:
        if isinstance(segment, dict):
            message.append(segment)
        else:
            message.append(await segment.onebot())

    return {
        "time": 1651692010,
        "self_id": 123456789,
        "post_type": "message",
        "message_type": "group",
        "sub_type": "normal",
        "message_id": 1234,
        "user_id": 987654321,
        "message": message,
        "raw_message": "Hello, World!",
        "font": 123,
        "sender": {
            "user_id": 987654321,
            "nickname": "Alice",
            "card": "",
            "sex": "unknown",
            "age": 0,
            "area": "",
            "level": "",
            "role": "member",
            "title": "",
            "title_expire_time": 0,
            "card_changeable": False,
        },
        "group_id": 1041902989,
    }
