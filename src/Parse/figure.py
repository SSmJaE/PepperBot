from typing import Union
from src.Parse import GROUP_EVENTS_T, GroupEvent


def figure_out(receive: dict):
    finalType: Union[str, None, GROUP_EVENTS_T] = ""

    post_type = receive["post_type"]

    if post_type == "meta_event":
        finalType = GroupEvent.MetaEvent

    if post_type == "request":
        request_type = receive["request_type"]
        sub_type = receive["sub_type"]

        if request_type == "group":
            if sub_type == "add":
                print("加群请求")
                finalType = GroupEvent.AddGroup

            elif sub_type == "invite":
                print("机器人被邀请入群")
                finalType = GroupEvent.BeenInvited

    if post_type == "notice":
        notice_type = receive["notice_type"]
        sub_type = receive["sub_type"]

        if notice_type == "group_increase":
            print("新成员入群")
            finalType = GroupEvent.MemberIncreased

        elif notice_type == "notify":
            if sub_type == "poke":
                print("机器人在群中被POKE")
                finalType = GroupEvent.BeenGroupPoked

            if sub_type == "honor":
                print("群荣誉变更")
                finalType = GroupEvent.GroupHonorChange

    if post_type == "message":
        message_type = receive["message_type"]
        sub_type = receive["sub_type"]

        if message_type == "private":

            if sub_type == "friend":
                print("好友私聊消息")
                finalType = GroupEvent.FriendMessage

            elif sub_type == "group":
                # todo 临时会话可能获取不到groupId
                print("群临时会话")
                finalType = GroupEvent.TempMessage

        elif message_type == "group":

            if sub_type == "normal":
                print("群普通消息")
                finalType = GroupEvent.GroupMessage

            elif sub_type == "anonymous":
                print("群匿名消息")
                finalType = GroupEvent.GroupAnonymousMessage

            elif sub_type == "notice":
                print("群通知消息")
                finalType = GroupEvent.GroupNotice

    return finalType
