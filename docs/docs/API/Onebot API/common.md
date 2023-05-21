## accept_friend_request

|参数名称|类型|默认值|
|:---:|:---:|:---:|
|flag|<class 'str'>|无|

## accept_group_request

|参数名称|类型|默认值|
|:---:|:---:|:---:|
|flag|<class 'str'>|无|

## can_send_image


检查是否可以发送图片

Returns:
    bool: 是否可以发送图片


## can_send_record


https://docs.go-cqhttp.org/api/#检查是否可以发送语音

Returns:
    bool: 是否可以发送语音


## delete_friend

https://docs.go-cqhttp.org/api/#删除好友

|参数名称|类型|默认值|
|:---:|:---:|:---:|
|user_id|<class 'str'>|无|

## delete_unidirectional_friend

https://docs.go-cqhttp.org/api/#删除好友

|参数名称|类型|默认值|
|:---:|:---:|:---:|
|user_id|<class 'str'>|无|

## get_all_files

|参数名称|类型|默认值|
|:---:|:---:|:---:|
|group_id|<class 'str'>|无|

## get_essence_msg_list


https://docs.go-cqhttp.org/api/#获取精华消息列表

Args:
    group_id (int): 群号

Returns:
    List[dict]: 精华消息列表，每个元素包含以下字段：
        - `sender_id` (int): 发送者 QQ 号
        - `sender_nick` (str): 发送者昵称
        - `sender_time` (int): 消息发送时间
        - `operator_id` (int): 操作者 QQ 号
        - `operator_nick` (str): 操作者昵称
        - `operator_time` (int): 精华设置时间
        - `message_id` (int): 消息 ID


|参数名称|类型|默认值|
|:---:|:---:|:---:|
|group_id|<class 'int'>|无|

## get_forward_msg


获取合并转发内容

https://docs.go-cqhttp.org/api/#获取合并转发内容

Args:
    message_id (str): 消息 ID

Returns:
    List[Dict[str, Any]]: 消息列表，包含以下字段：
        - `content` (str): 消息内容
        - `sender` (Dict[str, Any]): 消息发送者信息，包含以下字段：
            - `nickname` (str): 发送者昵称
            - `user_id` (int): 发送者 QQ 号
        - `time` (int): 消息发送时间的时间戳


|参数名称|类型|默认值|
|:---:|:---:|:---:|
|message_id|<class 'str'>|无|

## get_friend_list

https://docs.go-cqhttp.org/api/#获取好友列表

## get_group_at_all_remain


获取群 @全体成员 剩余次数

Args:
    group_id (int): 群号

Returns:
    Tuple[bool, int, int]: 返回元组，包含三个元素：
        can_at_all (bool): 是否可以 @全体成员
        remain_at_all_count_for_group (int): 群内所有管理当天剩余 @全体成员 次数
        remain_at_all_count_for_uin (int): Bot 当天剩余 @全体成员 次数


|参数名称|类型|默认值|
|:---:|:---:|:---:|
|group_id|<class 'int'>|无|

## get_group_honor_info


https://docs.go-cqhttp.org/api/#获取群荣誉信息

Args:
    group_id (int): 群号
    hon_type (str, optional): 要获取的群荣誉类型，可传入 "talkative" "performer" "legend" "strong_newbie" "emotion" 以分别获取单个类型的群荣誉数据，或传入 "all" 获取所有数据。默认为 None。

Returns:
    Union[List[dict], dict]: 如果传入的是单个类型，返回一个 dict，包含该类型的群荣誉数据；如果传入的是 "all"，返回一个 list，包含所有类型的群荣誉数据。


|参数名称|类型|默认值|
|:---:|:---:|:---:|
|group_id|<class 'int'>|无|
|hon_type|typing.Union[str, NoneType]|无|

## get_group_info


https://docs.go-cqhttp.org/api/#获取群信息

Args:
    group_id (int): 群号
    no_cache (bool, optional): 是否不使用缓存（使用缓存可能更新不及时，但响应更快）. Defaults to False.

Returns:
    Dict[str, Any]: 包含群信息的字典，具体字段说明如下：
        - group_id (int): 群号
        - group_name (str): 群名称
        - group_memo (str): 群备注
        - group_create_time (int): 群创建时间
        - group_level (int): 群等级
        - member_count (int): 成员数
        - max_member_count (int): 最大成员数（群容量）


|参数名称|类型|默认值|
|:---:|:---:|:---:|
|group_id|<class 'int'>|无|
|no_cache|<class 'bool'>|无|

## get_group_list


https://docs.go-cqhttp.org/api/#获取群列表

Args:
    no_cache (bool, optional): 是否不使用缓存（使用缓存可能更新不及时, 但响应更快）. Defaults to False.

Returns:
    List[Dict[str, Any]]: 响应内容为 json 数组, 每个元素和上面的 `get_group_info` 接口相同.


|参数名称|类型|默认值|
|:---:|:---:|:---:|
|no_cache|<class 'bool'>|无|

## get_group_member_info

|参数名称|类型|默认值|
|:---:|:---:|:---:|
|group_id|<class 'str'>|无|
|user_id|<class 'str'>|无|

## get_group_member_list


获取群成员列表

Args:
    group_id (int): 群号
    no_cache (bool, optional): 是否不使用缓存（使用缓存可能更新不及时, 但响应更快）, defaults to False.

Returns:
    List[Dict[str, Any]]: 响应内容为 json 数组, 每个元素的内容和上面的 `get_group_member_info` 接口相同, 但对于同一个群组的同一个成员,
    获取列表时和获取单独的成员信息时, 某些字段可能有所不同, 例如 `area`、`title` 等字段在获取列表时无法获得, 具体应以单独的成员信息为准。


|参数名称|类型|默认值|
|:---:|:---:|:---:|
|group_id|<class 'int'>|无|
|no_cache|typing.Union[bool, NoneType]|无|

## get_group_msg_history


获取群消息历史记录

Args:
    group_id (int): 群号
    message_seq (int, optional): 起始消息序号, 可通过 `get_msg` 获得，默认为 0

Returns:
    List[dict]: 从起始序号开始的前19条消息

Raises:
    TypeError: 当消息序号非整数时抛出该异常


|参数名称|类型|默认值|
|:---:|:---:|:---:|
|group_id|<class 'int'>|无|
|message_seq|<class 'int'>|无|

## get_group_system_msg


获取群系统消息

Returns:
    Dict[str, Union[List[InvitedRequest], List[JoinRequest]]]: 群系统消息


## get_image


获取图片信息

Args:
    file (str): 图片缓存文件名

Returns:
    Dict[str, Any] or None: 图片信息
        - size (int): 图片源文件大小
        - filename (str): 图片文件原名
        - url (str): 图片下载地址


|参数名称|类型|默认值|
|:---:|:---:|:---:|
|file|<class 'str'>|无|

## get_login_info

https://docs.go-cqhttp.org/api/#%E8%8E%B7%E5%8F%96%E7%99%BB%E5%BD%95%E5%8F%B7%E4%BF%A1%E6%81%AF

## get_online_clients

https://docs.go-cqhttp.org/api/#获取当前账号在线客户端列表

|参数名称|类型|默认值|
|:---:|:---:|:---:|
|no_cache|<class 'inspect._empty'>|True|

## get_status


https://docs.go-cqhttp.org/api/#获取状态

Returns:
    Dict[str, Any]: 状态信息


## get_stranger_info

https://docs.go-cqhttp.org/api/#获取陌生人信息

        字段名	数据类型	默认值	说明
        user_id	int64	-	QQ 号
        no_cache	boolean	false	是否不使用缓存（使用缓存可能更新不及时, 但响应更快）


|参数名称|类型|默认值|
|:---:|:---:|:---:|
|user_id|<class 'str'>|无|
|no_cache|<class 'bool'>|无|

## get_unidirectional_friend_list

https://docs.go-cqhttp.org/api/#获取单向好友列表

## group_message

|参数名称|类型|默认值|
|:---:|:---:|:---:|
|group_id|<class 'str'>|无|
|segments|T_SegmentInstance|无|

## mark_msg_as_read

https://docs.go-cqhttp.org/api/#标记消息已读

        Args:
            message_id (int): 消息 ID

        Returns:
            None


|参数名称|类型|默认值|
|:---:|:---:|:---:|
|message_id|<class 'int'>|无|

## private_message

https://docs.go-cqhttp.org/api/#发送私聊消息

|参数名称|类型|默认值|
|:---:|:---:|:---:|
|user_id|<class 'str'>|无|
|segments|T_SegmentInstance|无|

## reject_friend_request

|参数名称|类型|默认值|
|:---:|:---:|:---:|
|flag|<class 'str'>|无|
|reason|<class 'str'>|无|

## reject_group_request

|参数名称|类型|默认值|
|:---:|:---:|:---:|
|flag|<class 'str'>|无|
|reason|<class 'str'>|无|

## send_group_forward_msg


发送合并转发 ( 群聊 )

https://docs.go-cqhttp.org/api/#发送合并转发-群聊-

Args:
    group_id (int): 群号
    messages (List[dict]): 自定义转发消息, 具体看 https://docs.go-cqhttp.org/cqcode/#合并转发消息节点

Returns:
    dict: 响应数据
        - `message_id` (int): 消息 ID
        - `forward_id` (str): 转发消息 ID


|参数名称|类型|默认值|
|:---:|:---:|:---:|
|group_id|<class 'int'>|无|
|messages|typing.List[dict]|无|

## send_group_notice


https://docs.go-cqhttp.org/api/#发送群公告

Args:
    group_id (int): 群号
    content (str): 公告内容
    image (str, optional): 图片路径（可选）

Returns:
    None


|参数名称|类型|默认值|
|:---:|:---:|:---:|
|group_id|<class 'int'>|无|
|content|<class 'str'>|无|
|image|<class 'str'>|无|

## send_private_forward_msg


发送合并转发 ( 好友 )

Args:
    user_id (int): 好友 QQ 号
    messages (List[dict]): 自定义转发消息, 具体看 CQcode

Returns:
    dict: 响应数据

参考文档：
https://docs.go-cqhttp.org/api/#发送合并转发-好友


|参数名称|类型|默认值|
|:---:|:---:|:---:|
|user_id|<class 'int'>|无|
|messages|typing.List[dict]|无|

## set_account_profile

https://docs.go-cqhttp.org/api/#%E8%AE%BE%E7%BD%AE%E7%99%BB%E5%BD%95%E5%8F%B7%E8%B5%84%E6%96%99

        字段名	数据类型	默认值	说明
        nickname	string	-	名称
        company	string	-	公司
        email	string	-	邮箱
        college	string	-	学校
        personal_note	string	-	个人说明


|参数名称|类型|默认值|
|:---:|:---:|:---:|
|nickname|typing.Union[str, NoneType]|无|
|company|typing.Union[str, NoneType]|无|
|email|typing.Union[str, NoneType]|无|
|college|typing.Union[str, NoneType]|无|
|personal_note|typing.Union[str, NoneType]|无|

## set_group_ban


群单人禁言

Args:
    group_id (int): 群号
    user_id (int): 要禁言的 QQ 号
    duration (int, optional): 禁言时长, 单位秒, 0 表示取消禁言. Defaults to 30 * 60.

Returns:
    None


|参数名称|类型|默认值|
|:---:|:---:|:---:|
|group_id|<class 'str'>|无|
|user_id|<class 'str'>|无|
|duration|<class 'int'>|30|

## set_group_card


https://docs.go-cqhttp.org/api/#设置群名片

Args:
    group_id (int): 群号
    user_id (int): 要设置的 QQ 号
    card (str, optional): 群名片内容，不填或空字符串表示删除群名片. Defaults to "".

Returns:
    None


|参数名称|类型|默认值|
|:---:|:---:|:---:|
|group_id|<class 'int'>|无|
|user_id|<class 'int'>|无|
|card|<class 'str'>|无|

## set_group_kick


群组踢人

Args:
    group_id (int): 群号
    user_id (int): 要踢的 QQ 号
    reject_add_request (bool, optional): 拒绝此人的加群请求，默认为 False

Returns:
    None


|参数名称|类型|默认值|
|:---:|:---:|:---:|
|group_id|<class 'str'>|无|
|user_id|<class 'str'>|无|
|permanent|<class 'bool'>|无|

## set_group_name


https://docs.go-cqhttp.org/api/#设置群名

Args:
    group_id (int): 群号
    group_name (str): 新群名

Returns:
    None


|参数名称|类型|默认值|
|:---:|:---:|:---:|
|group_id|<class 'int'>|无|
|group_name|<class 'str'>|无|

## set_group_whole_ban


https://docs.go-cqhttp.org/api/#群全员禁言

Args:
    group_id (int): 群号
    enable (bool, optional): 是否禁言. Defaults to True.

Returns:
    None


|参数名称|类型|默认值|
|:---:|:---:|:---:|
|group_id|<class 'int'>|无|
|enable|<class 'bool'>|True|

## upload_group_file

|参数名称|类型|默认值|
|:---:|:---:|:---:|
|group_id|<class 'str'>|无|
|path|<class 'str'>|无|
|display_name|<class 'str'>|无|
|folder_id|typing.Union[str, NoneType]|无|

## withdraw_message

https://docs.go-cqhttp.org/api/#撤回消息

        **参数**
        | 字段名       | 数据类型 | 默认值 | 说明    |
        | ------------ | -------- | ------ | ------- |
        | `message_id` | int32    | -      | 消息 ID |

        **响应数据**
        | 字段       | 类型              | 说明     |
        | ---------- | ----------------- | -------- |
        | `messages` | forward message[] | 消息列表 |


|参数名称|类型|默认值|
|:---:|:---:|:---:|
|message_id|<class 'str'>|无|

