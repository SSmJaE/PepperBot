""" 大多数机器人协议共有的事件 """


class UniversalCommonEvent:
    pass


class UniversalGroupEvent:
    """群事件"""

    group_message = "group_message"
    group_request = "group_request"


class UniversalPrivateEvent:
    friend_message = "friend_message"
    friend_request = "friend_request"



async def get_universal_kwargs():
    pass


ALL_META_EVENTS = []
ALL_GROUP_EVENTS = []
ALL_PRIVATE_EVENTS = []


GROUP_COMMAND_TRIGGER_EVENTS = [
    # group_message, onebot_group_message, keaimao_group_message
]
PRIVATE_COMMAND_TRIGGER_EVENTS = ["friend_message" or "onebot_temp_message"]

