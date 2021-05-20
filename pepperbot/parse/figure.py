from typing import Optional
from pepperbot.parse import GROUP_EVENTS_T, GroupEvent


def figure_out(receive: dict):
    finalType: Optional[GROUP_EVENTS_T] = None

    post_type = receive["post_type"]

    if post_type == "meta_event":
        finalType = GroupEvent.meta_event

    if post_type == "request":
        request_type = receive["request_type"]
        sub_type = receive["sub_type"]

        if request_type == "group":
            if sub_type == "add":
                print("加群请求")
                finalType = GroupEvent.add_group

            elif sub_type == "invite":
                print("机器人被邀请入群")
                finalType = GroupEvent.been_invited

    if post_type == "notice":
        notice_type = receive["notice_type"]
        sub_type = receive["sub_type"]

        if notice_type == "group_increase":
            print("新成员入群")
            finalType = GroupEvent.member_increased

        elif notice_type == "notify":
            if sub_type == "poke":
                print("群POKE事件")
                finalType = GroupEvent.been_group_poked

            if sub_type == "honor":
                print("群荣誉变更")
                finalType = GroupEvent.group_honor_change

    if post_type == "message":
        message_type = receive["message_type"]
        sub_type = receive["sub_type"]

        if message_type == "private":

            if sub_type == "friend":
                print("好友私聊消息")
                finalType = GroupEvent.friend_message

            elif sub_type == "group":
                # todo 临时会话可能获取不到groupId
                print("群临时会话")
                finalType = GroupEvent.temp_message

        elif message_type == "group":

            if sub_type == "normal":
                print("群普通消息")
                finalType = GroupEvent.group_message

            elif sub_type == "anonymous":
                print("群匿名消息")
                finalType = GroupEvent.group_anonymous_essage

            elif sub_type == "notice":
                print("群通知消息")
                finalType = GroupEvent.group_notice

    return finalType
