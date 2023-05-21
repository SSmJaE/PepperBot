## been_friend_added

> 机器人接收到添加好友请求  [原始事件的字段定义](https://docs.go-cqhttp.org/event/#%E5%8A%A0%E5%A5%BD%E5%8F%8B%E8%AF%B7%E6%B1%82)

|参数名称|类型|
|:---:|:---:|
|raw_event|from typing import Dict|
|bot|from pepperbot.adapters.onebot.api import OnebotV11PrivateBot|

```python
from typing import Dict
from pepperbot.adapters.onebot.api import OnebotV11PrivateBot


class MyHandler:
    async def been_friend_added(
        self,
        raw_event: Dict,
        bot: OnebotV11PrivateBot,
    ):
        pass

```

## been_friend_poked

> 好友戳一戳

|参数名称|类型|
|:---:|:---:|
|raw_event|from typing import Dict|
|bot|from pepperbot.adapters.onebot.api import OnebotV11PrivateBot|

```python
from typing import Dict
from pepperbot.adapters.onebot.api import OnebotV11PrivateBot


class MyHandler:
    async def been_friend_poked(
        self,
        raw_event: Dict,
        bot: OnebotV11PrivateBot,
    ):
        pass

```

## been_group_invited

> 机器人被邀请入群 [原始事件的字段定义](https://docs.go-cqhttp.org/event/#%E5%8A%A0%E7%BE%A4%E8%AF%B7%E6%B1%82-%E9%82%80%E8%AF%B7)

|参数名称|类型|
|:---:|:---:|
|raw_event|from typing import Dict|
|bot|from pepperbot.adapters.onebot.api import OnebotV11GroupBot|

```python
from typing import Dict
from pepperbot.adapters.onebot.api import OnebotV11GroupBot


class MyHandler:
    async def been_group_invited(
        self,
        raw_event: Dict,
        bot: OnebotV11GroupBot,
    ):
        pass

```

## been_group_poked

> 群POKE事件  [原始事件的字段定义](https://docs.go-cqhttp.org/event/#%E7%BE%A4%E5%86%85%E6%88%B3%E4%B8%80%E6%88%B3)

|参数名称|类型|
|:---:|:---:|
|raw_event|from typing import Dict|
|bot|from pepperbot.adapters.onebot.api import OnebotV11GroupBot|

```python
from typing import Dict
from pepperbot.adapters.onebot.api import OnebotV11GroupBot


class MyHandler:
    async def been_group_poked(
        self,
        raw_event: Dict,
        bot: OnebotV11GroupBot,
    ):
        pass

```

## client_status_change

> 客户端状态变更

|参数名称|类型|
|:---:|:---:|
|raw_event|from typing import Dict|

```python
from typing import Dict


class MyHandler:
    async def client_status_change(
        self,
        raw_event: Dict,
    ):
        pass

```

## friend_message

> 好友私聊消息  [原始事件的字段定义](https://docs.go-cqhttp.org/event/#%E7%A7%81%E8%81%8A%E6%B6%88%E6%81%AF)

|参数名称|类型|
|:---:|:---:|
|raw_event|from typing import Dict|
|bot|from pepperbot.adapters.onebot.api import OnebotV11PrivateBot|
|chain|from pepperbot.core.message.chain import MessageChain|

```python
from typing import Dict
from pepperbot.adapters.onebot.api import OnebotV11PrivateBot
from pepperbot.core.message.chain import MessageChain


class MyHandler:
    async def friend_message(
        self,
        raw_event: Dict,
        bot: OnebotV11PrivateBot,
        chain: MessageChain,
    ):
        pass

```

## friend_message_been_withdraw

> 好友私聊消息撤回

|参数名称|类型|
|:---:|:---:|
|raw_event|from typing import Dict|
|bot|from pepperbot.adapters.onebot.api import OnebotV11PrivateBot|

```python
from typing import Dict
from pepperbot.adapters.onebot.api import OnebotV11PrivateBot


class MyHandler:
    async def friend_message_been_withdraw(
        self,
        raw_event: Dict,
        bot: OnebotV11PrivateBot,
    ):
        pass

```

## group_admin_change

> 群管理员变更事件

|参数名称|类型|
|:---:|:---:|
|raw_event|from typing import Dict|
|bot|from pepperbot.adapters.onebot.api import OnebotV11GroupBot|

```python
from typing import Dict
from pepperbot.adapters.onebot.api import OnebotV11GroupBot


class MyHandler:
    async def group_admin_change(
        self,
        raw_event: Dict,
        bot: OnebotV11GroupBot,
    ):
        pass

```

## group_anonymous_message

> 群匿名消息  [原始事件的字段定义](https://docs.go-cqhttp.org/event/#%E7%BE%A4%E6%B6%88%E6%81%AF)

|参数名称|类型|
|:---:|:---:|
|raw_event|from typing import Dict|
|bot|from pepperbot.adapters.onebot.api import OnebotV11GroupBot|
|chain|from pepperbot.core.message.chain import MessageChain|

```python
from typing import Dict
from pepperbot.adapters.onebot.api import OnebotV11GroupBot
from pepperbot.core.message.chain import MessageChain


class MyHandler:
    async def group_anonymous_message(
        self,
        raw_event: Dict,
        bot: OnebotV11GroupBot,
        chain: MessageChain,
    ):
        pass

```

## group_ban_change

> 群禁言事件 [原始事件的字段定义](https://docs.go-cqhttp.org/event/#%E7%BE%A4%E7%A6%81%E8%A8%80%E4%BA%8B%E4%BB%B6)

|参数名称|类型|
|:---:|:---:|
|raw_event|from typing import Dict|
|bot|from pepperbot.adapters.onebot.api import OnebotV11GroupBot|

```python
from typing import Dict
from pepperbot.adapters.onebot.api import OnebotV11GroupBot


class MyHandler:
    async def group_ban_change(
        self,
        raw_event: Dict,
        bot: OnebotV11GroupBot,
    ):
        pass

```

## group_honor_change

> 群荣誉变更  [原始事件的字段定义](https://docs.go-cqhttp.org/event/#%E7%BE%A4%E6%88%90%E5%91%98%E8%8D%A3%E8%AA%89%E5%8F%98%E6%9B%B4%E6%8F%90%E7%A4%BA)

|参数名称|类型|
|:---:|:---:|
|raw_event|from typing import Dict|
|bot|from pepperbot.adapters.onebot.api import OnebotV11GroupBot|

```python
from typing import Dict
from pepperbot.adapters.onebot.api import OnebotV11GroupBot


class MyHandler:
    async def group_honor_change(
        self,
        raw_event: Dict,
        bot: OnebotV11GroupBot,
    ):
        pass

```

## group_join_request

> 加群请求  [原始事件的字段定义](https://docs.go-cqhttp.org/event/#%E5%8A%A0%E7%BE%A4%E8%AF%B7%E6%B1%82-%E9%82%80%E8%AF%B7)

|参数名称|类型|
|:---:|:---:|
|raw_event|from typing import Dict|
|bot|from pepperbot.adapters.onebot.api import OnebotV11GroupBot|

```python
from typing import Dict
from pepperbot.adapters.onebot.api import OnebotV11GroupBot


class MyHandler:
    async def group_join_request(
        self,
        raw_event: Dict,
        bot: OnebotV11GroupBot,
    ):
        pass

```

## group_lucky_king_notice

> 红包运气王通知

|参数名称|类型|
|:---:|:---:|
|raw_event|from typing import Dict|
|bot|from pepperbot.adapters.onebot.api import OnebotV11GroupBot|

```python
from typing import Dict
from pepperbot.adapters.onebot.api import OnebotV11GroupBot


class MyHandler:
    async def group_lucky_king_notice(
        self,
        raw_event: Dict,
        bot: OnebotV11GroupBot,
    ):
        pass

```

## group_member_card_change

> 群成员名片变更事件

|参数名称|类型|
|:---:|:---:|
|raw_event|from typing import Dict|
|bot|from pepperbot.adapters.onebot.api import OnebotV11GroupBot|

```python
from typing import Dict
from pepperbot.adapters.onebot.api import OnebotV11GroupBot


class MyHandler:
    async def group_member_card_change(
        self,
        raw_event: Dict,
        bot: OnebotV11GroupBot,
    ):
        pass

```

## group_member_declined

> 群成员减少  [原始事件的字段定义](https://docs.go-cqhttp.org/event/#%E7%BE%A4%E6%88%90%E5%91%98%E5%87%8F%E5%B0%91)

|参数名称|类型|
|:---:|:---:|
|raw_event|from typing import Dict|
|bot|from pepperbot.adapters.onebot.api import OnebotV11GroupBot|

```python
from typing import Dict
from pepperbot.adapters.onebot.api import OnebotV11GroupBot


class MyHandler:
    async def group_member_declined(
        self,
        raw_event: Dict,
        bot: OnebotV11GroupBot,
    ):
        pass

```

## group_member_increased

> 新成员入群  [原始事件的字段定义](https://docs.go-cqhttp.org/event/#%E7%BE%A4%E6%88%90%E5%91%98%E5%A2%9E%E5%8A%A0)

|参数名称|类型|
|:---:|:---:|
|member|from pepperbot.adapters.onebot.models.user import GroupMember|
|raw_event|from typing import Dict|
|bot|from pepperbot.adapters.onebot.api import OnebotV11GroupBot|

```python
from pepperbot.adapters.onebot.models.user import GroupMember
from typing import Dict
from pepperbot.adapters.onebot.api import OnebotV11GroupBot


class MyHandler:
    async def group_member_increased(
        self,
        member: GroupMember,
        raw_event: Dict,
        bot: OnebotV11GroupBot,
    ):
        pass

```

## group_member_title_change

> 群成员头衔变更事件

|参数名称|类型|
|:---:|:---:|
|raw_event|from typing import Dict|
|bot|from pepperbot.adapters.onebot.api import OnebotV11GroupBot|

```python
from typing import Dict
from pepperbot.adapters.onebot.api import OnebotV11GroupBot


class MyHandler:
    async def group_member_title_change(
        self,
        raw_event: Dict,
        bot: OnebotV11GroupBot,
    ):
        pass

```

## group_message

> 群普通消息 [原始事件的字段定义](https://docs.go-cqhttp.org/event/#%E7%BE%A4%E6%B6%88%E6%81%AF)

|参数名称|类型|
|:---:|:---:|
|member|from pepperbot.adapters.onebot.models.user import GroupMember|
|raw_event|from typing import Dict|
|bot|from pepperbot.adapters.onebot.api import OnebotV11GroupBot|
|chain|from pepperbot.core.message.chain import MessageChain|

```python
from pepperbot.adapters.onebot.models.user import GroupMember
from typing import Dict
from pepperbot.adapters.onebot.api import OnebotV11GroupBot
from pepperbot.core.message.chain import MessageChain


class MyHandler:
    async def group_message(
        self,
        member: GroupMember,
        raw_event: Dict,
        bot: OnebotV11GroupBot,
        chain: MessageChain,
    ):
        pass

```

## group_message_been_withdraw

> 群消息撤回事件

|参数名称|类型|
|:---:|:---:|
|raw_event|from typing import Dict|
|bot|from pepperbot.adapters.onebot.api import OnebotV11GroupBot|

```python
from typing import Dict
from pepperbot.adapters.onebot.api import OnebotV11GroupBot


class MyHandler:
    async def group_message_been_withdraw(
        self,
        raw_event: Dict,
        bot: OnebotV11GroupBot,
    ):
        pass

```

## group_new_file_uploaded

> 群文件上传事件

|参数名称|类型|
|:---:|:---:|
|raw_event|from typing import Dict|
|bot|from pepperbot.adapters.onebot.api import OnebotV11GroupBot|

```python
from typing import Dict
from pepperbot.adapters.onebot.api import OnebotV11GroupBot


class MyHandler:
    async def group_new_file_uploaded(
        self,
        raw_event: Dict,
        bot: OnebotV11GroupBot,
    ):
        pass

```

## heartbeat

> 心跳

|参数名称|类型|
|:---:|:---:|
|raw_event|from typing import Dict|

```python
from typing import Dict


class MyHandler:
    async def heartbeat(
        self,
        raw_event: Dict,
    ):
        pass

```

## on_connect

> 连接成功

|参数名称|类型|
|:---:|:---:|
|raw_event|from typing import Dict|

```python
from typing import Dict


class MyHandler:
    async def on_connect(
        self,
        raw_event: Dict,
    ):
        pass

```

## temporary_message

> 群临时会话  [原始事件的字段定义](https://docs.go-cqhttp.org/event/#%E7%A7%81%E8%81%8A%E6%B6%88%E6%81%AF)

|参数名称|类型|
|:---:|:---:|
|raw_event|from typing import Dict|
|bot|from pepperbot.adapters.onebot.api import OnebotV11PrivateBot|
|chain|from pepperbot.core.message.chain import MessageChain|

```python
from typing import Dict
from pepperbot.adapters.onebot.api import OnebotV11PrivateBot
from pepperbot.core.message.chain import MessageChain


class MyHandler:
    async def temporary_message(
        self,
        raw_event: Dict,
        bot: OnebotV11PrivateBot,
        chain: MessageChain,
    ):
        pass

```

