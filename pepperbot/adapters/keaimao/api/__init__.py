# https://doc.vwzx.com/web/#/6?page_id=123

# /**
#      * 命令机器人去做某事
#      * @param array $param
#      * @param string $authorization
#      * @return string
#      *
#      * param
#      * >>>  event 事件名称
#      * >>>  robot_wxid 机器人id
#      * >>>  group_wxid 群id
#      * >>>  member_wxid 群艾特人id
#      * >>>  member_name 群艾特人昵称
#      * >>>  to_wxid 接收方(群/好友)
#      * >>>  msg 消息体(str/json)
#      *
#      * param.event
#      * >>> SendTextMsg 发送文本消息 robot_wxid to_wxid(群/好友) msg
#      * >>> SendImageMsg 发送图片消息 robot_wxid to_wxid(群/好友) msg(name[md5值或其他唯一的名字，包含扩展名例如1.jpg], url)
#      * >>> SendVideoMsg 发送视频消息 robot_wxid to_wxid(群/好友) msg(name[md5值或其他唯一的名字，包含扩展名例如1.mp4], url)
#      * >>> SendFileMsg 发送文件消息 robot_wxid to_wxid(群/好友) msg(name[md5值或其他唯一的名字，包含扩展名例如1.txt], url)
#      * >>> SendGroupMsgAndAt 发送群消息并艾特(4.4只能艾特一人) robot_wxid, group_wxid, member_wxid, member_name, msg
#      * >>> SendEmojiMsg 发送动态表情 robot_wxid to_wxid(群/好友) msg(name[md5值或其他唯一的名字，包含扩展名例如1.gif], url)
#      * >>> SendLinkMsg 发送分享链接 robot_wxid, to_wxid(群/好友), msg(title, text, target_url, pic_url, icon_url)
#      * >>> SendMusicMsg 发送音乐分享 robot_wxid, to_wxid(群/好友), msg(music_name, type)
#      * >>> GetRobotName 取登录账号昵称 robot_wxid
#      * >>> GetRobotHeadimgurl 取登录账号头像 robot_wxid
#      * >>> GetLoggedAccountList 取登录账号列表 不需要参数
#      * >>> GetFriendList 取好友列表 robot_wxid
#      * >>> GetGroupList 取群聊列表 robot_wxid(不传返回全部机器人的)
#      * >>> GetGroupMemberList 取群成员列表 robot_wxid, group_wxid
#      * >>> GetGroupMemberInfo 取群成员详细 robot_wxid, group_wxid, member_wxid
#      * >>> AcceptTransfer 接收好友转账 robot_wxid, to_wxid, msg
#      * >>> AgreeGroupInvite 同意群聊邀请 robot_wxid, msg
#      * >>> AgreeFriendVerify 同意好友请求 robot_wxid, msg
#      * >>> EditFriendNote 修改好友备注 robot_wxid, to_wxid, msg
#      * >>> DeleteFriend 删除好友 robot_wxid, to_wxid
#      * >>> GetappInfo 取插件信息 无参数
#      * >>> GetAppDir 取应用目录 无
#      * >>> AddAppLogs 添加日志 msg
#      * >>> ReloadApp 重载插件 无
#      * >>> RemoveGroupMember 踢出群成员 robot_wxid, group_wxid, member_wxid
#      * >>> EditGroupName 修改群名称 robot_wxid, group_wxid, msg
#      * >>> EditGroupNotice 修改群公告 robot_wxid, group_wxid, msg
#      * >>> BuildNewGroup 建立新群 robot_wxid, msg(好友Id用"|"分割)
#      * >>> QuitGroup 退出群聊 robot_wxid, group_wxid
#      * >>> InviteInGroup 邀请加入群聊 robot_wxid, group_wxid, to_wxid


from typing import TYPE_CHECKING, Dict
from pepperbot.core.bot.api_caller import ApiCaller
from pepperbot.core.message.segment import Image, T_SegmentClass, Text
from pepperbot.exceptions import BackendApiError

# from pepperbot.core.message.segment import Text
from pepperbot.store.meta import get_bot_id, get_keaimao_caller
from pepperbot.types import BaseBot

if TYPE_CHECKING:
    from pepperbot.core.message.segment import T_SegmentInstance

KEAIMAO_SEGMENT_API_MAPPING: Dict[T_SegmentClass, str] = {
    Text: "SendTextMsg",
    Image: "SendImageMsg",
}


class KeaimaoApi:
    # @property
    # def api_caller(self):
    #     return get_keaimao_caller()  # 获取api_caller时，一定已经实例化了对应的api_caller

    @staticmethod
    async def get_login_accounts():
        return (await get_keaimao_caller()("GetLoggedAccountList")).json()["data"]

    @staticmethod
    async def group_message(group_id: str, *segments: "T_SegmentInstance"):
        api_caller = get_keaimao_caller()

        for segment in segments:
            segment_type = segment.__class__

            if api_name := KEAIMAO_SEGMENT_API_MAPPING[segment_type]:
                await api_caller(
                    api_name,
                    robot_wxid=get_bot_id("keaimao"),
                    to_wxid=group_id,
                    msg=segment.keaimao,
                )

            else:
                raise BackendApiError(f"尚未适配的消息类型 {segment_type}")

    # @static


class KeaimaoProperties(BaseBot):
    bot_id: str
    group_id: str
    private_id: str
    api_caller: ApiCaller


class KeaimaoCommonApi(KeaimaoProperties):
    pass


class KeaimaoGroupApi(KeaimaoProperties):
    async def group_message(self, *segment: "T_SegmentInstance"):
        return await KeaimaoApi.group_message(self.group_id, *segment)


class KeaimaoPrivateApi(KeaimaoProperties):
    pass


class KeaimaoGroupBot(KeaimaoCommonApi, KeaimaoGroupApi):
    __slots__ = (
        "bot_id",
        "group_id",
        "api_caller",
    )

    def __init__(self, bot_id: str, group_id: str):
        self.bot_id = bot_id
        self.group_id = group_id
        self.api_caller = get_keaimao_caller()


class KeaimaoPrivateBot(KeaimaoCommonApi, KeaimaoPrivateApi):
    __slots__ = (
        "bot_id",
        "private_id",
        "api_caller",
    )

    def __init__(self, bot_id: str, private_id: str):
        self.bot_id = bot_id
        self.private_id = private_id
        self.api_caller = get_keaimao_caller()
