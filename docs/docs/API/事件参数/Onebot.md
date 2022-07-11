## group_message

> 群普通消息 [原始事件的字段定义](https://docs.go-cqhttp.org/event/#%E7%BE%A4%E6%B6%88%E6%81%AF)

|参数名称|类型|
|:---:|:---:|
|raw_event|`from typing import Dict`|
|bot|`from pepperbot.adapters.onebot.api import OnebotV11GroupBot`|
|chain|`from pepperbot.core.message.chain import MessageChain`|

```py
from typing import Dict
from pepperbot.adapters.onebot.api import OnebotV11GroupBot
from pepperbot.core.message.chain import MessageChain


class MyHandler:
    async def group_message(
        raw_event: Dict,
        bot: OnebotV11GroupBot,
        chain: MessageChain,
    ):
        pass
```

## group_anonymous_message

> 群匿名消息  [原始事件的字段定义](https://docs.go-cqhttp.org/event/#%E7%BE%A4%E6%B6%88%E6%81%AF)

|参数名称|类型|
|:---:|:---:|
|raw_event|`from typing import Dict`|
|bot|`from pepperbot.adapters.onebot.api import OnebotV11GroupBot`|
|chain|`from pepperbot.core.message.chain import MessageChain`|

```py
from typing import Dict
from pepperbot.adapters.onebot.api import OnebotV11GroupBot
from pepperbot.core.message.chain import MessageChain


class MyHandler:
    async def group_anonymous_message(
        raw_event: Dict,
        bot: OnebotV11GroupBot,
        chain: MessageChain,
    ):
        pass
```

## group_message_been_withdraw

> 尚未实现

|参数名称|类型|
|:---:|:---:|
|raw_event|`from typing import Dict`|
|bot|`from pepperbot.adapters.onebot.api import OnebotV11GroupBot`|

```py
from typing import Dict
from pepperbot.adapters.onebot.api import OnebotV11GroupBot


class MyHandler:
    async def group_message_been_withdraw(
        raw_event: Dict,
        bot: OnebotV11GroupBot,
    ):
        pass
```

## group_honor_change

> 群荣誉变更  [原始事件的字段定义](https://docs.go-cqhttp.org/event/#%E7%BE%A4%E6%88%90%E5%91%98%E8%8D%A3%E8%AA%89%E5%8F%98%E6%9B%B4%E6%8F%90%E7%A4%BA)

|参数名称|类型|
|:---:|:---:|
|raw_event|`from typing import Dict`|
|bot|`from pepperbot.adapters.onebot.api import OnebotV11GroupBot`|

```py
from typing import Dict
from pepperbot.adapters.onebot.api import OnebotV11GroupBot


class MyHandler:
    async def group_honor_change(
        raw_event: Dict,
        bot: OnebotV11GroupBot,
    ):
        pass
```

## group_admin_change

> 尚未实现

|参数名称|类型|
|:---:|:---:|
|raw_event|`from typing import Dict`|
|bot|`from pepperbot.adapters.onebot.api import OnebotV11GroupBot`|

```py
from typing import Dict
from pepperbot.adapters.onebot.api import OnebotV11GroupBot


class MyHandler:
    async def group_admin_change(
        raw_event: Dict,
        bot: OnebotV11GroupBot,
    ):
        pass
```

## group_ban_change

> 尚未实现

|参数名称|类型|
|:---:|:---:|
|raw_event|`from typing import Dict`|
|bot|`from pepperbot.adapters.onebot.api import OnebotV11GroupBot`|

```py
from typing import Dict
from pepperbot.adapters.onebot.api import OnebotV11GroupBot


class MyHandler:
    async def group_ban_change(
        raw_event: Dict,
        bot: OnebotV11GroupBot,
    ):
        pass
```

## member_increased

> 新成员入群  [原始事件的字段定义](https://docs.go-cqhttp.org/event/#%E7%BE%A4%E6%88%90%E5%91%98%E5%A2%9E%E5%8A%A0)

|参数名称|类型|
|:---:|:---:|
|raw_event|`from typing import Dict`|
|bot|`from pepperbot.adapters.onebot.api import OnebotV11GroupBot`|

```py
from typing import Dict
from pepperbot.adapters.onebot.api import OnebotV11GroupBot


class MyHandler:
    async def member_increased(
        raw_event: Dict,
        bot: OnebotV11GroupBot,
    ):
        pass
```

## member_declined

> 群成员减少  [原始事件的字段定义](https://docs.go-cqhttp.org/event/#%E7%BE%A4%E6%88%90%E5%91%98%E5%87%8F%E5%B0%91)

|参数名称|类型|
|:---:|:---:|
|raw_event|`from typing import Dict`|
|bot|`from pepperbot.adapters.onebot.api import OnebotV11GroupBot`|

```py
from typing import Dict
from pepperbot.adapters.onebot.api import OnebotV11GroupBot


class MyHandler:
    async def member_declined(
        raw_event: Dict,
        bot: OnebotV11GroupBot,
    ):
        pass
```

## new_file_uploaded

> 尚未实现

|参数名称|类型|
|:---:|:---:|
|raw_event|`from typing import Dict`|
|bot|`from pepperbot.adapters.onebot.api import OnebotV11GroupBot`|

```py
from typing import Dict
from pepperbot.adapters.onebot.api import OnebotV11GroupBot


class MyHandler:
    async def new_file_uploaded(
        raw_event: Dict,
        bot: OnebotV11GroupBot,
    ):
        pass
```

## group_join_request

> 加群请求  [原始事件的字段定义](https://docs.go-cqhttp.org/event/#%E5%8A%A0%E7%BE%A4%E8%AF%B7%E6%B1%82-%E9%82%80%E8%AF%B7)

|参数名称|类型|
|:---:|:---:|
|raw_event|`from typing import Dict`|
|bot|`from pepperbot.adapters.onebot.api import OnebotV11GroupBot`|

```py
from typing import Dict
from pepperbot.adapters.onebot.api import OnebotV11GroupBot


class MyHandler:
    async def group_join_request(
        raw_event: Dict,
        bot: OnebotV11GroupBot,
    ):
        pass
```

## been_group_poked

> 群POKE事件  [原始事件的字段定义](https://docs.go-cqhttp.org/event/#%E7%BE%A4%E5%86%85%E6%88%B3%E4%B8%80%E6%88%B3)

|参数名称|类型|
|:---:|:---:|
|raw_event|`from typing import Dict`|
|bot|`from pepperbot.adapters.onebot.api import OnebotV11GroupBot`|

```py
from typing import Dict
from pepperbot.adapters.onebot.api import OnebotV11GroupBot


class MyHandler:
    async def been_group_poked(
        raw_event: Dict,
        bot: OnebotV11GroupBot,
    ):
        pass
```

## been_invited

> 机器人被邀请入群 [原始事件的字段定义](https://docs.go-cqhttp.org/event/#%E5%8A%A0%E7%BE%A4%E8%AF%B7%E6%B1%82-%E9%82%80%E8%AF%B7)

|参数名称|类型|
|:---:|:---:|
|raw_event|`from typing import Dict`|
|bot|`from pepperbot.adapters.onebot.api import OnebotV11GroupBot`|

```py
from typing import Dict
from pepperbot.adapters.onebot.api import OnebotV11GroupBot


class MyHandler:
    async def been_invited(
        raw_event: Dict,
        bot: OnebotV11GroupBot,
    ):
        pass
```

## been_added

> 机器人接收到添加好友请求  [原始事件的字段定义](https://docs.go-cqhttp.org/event/#%E5%8A%A0%E5%A5%BD%E5%8F%8B%E8%AF%B7%E6%B1%82)

|参数名称|类型|
|:---:|:---:|
|raw_event|`from typing import Dict`|
|bot|`from pepperbot.adapters.onebot.api import OnebotV11PrivateBot`|

```py
from typing import Dict
from pepperbot.adapters.onebot.api import OnebotV11PrivateBot


class MyHandler:
    async def been_added(
        raw_event: Dict,
        bot: OnebotV11PrivateBot,
    ):
        pass
```

## been_friend_poked

> 尚未实现

|参数名称|类型|
|:---:|:---:|
|raw_event|`from typing import Dict`|
|bot|`from pepperbot.adapters.onebot.api import OnebotV11PrivateBot`|

```py
from typing import Dict
from pepperbot.adapters.onebot.api import OnebotV11PrivateBot


class MyHandler:
    async def been_friend_poked(
        raw_event: Dict,
        bot: OnebotV11PrivateBot,
    ):
        pass
```

## temp_message

> 群临时会话  [原始事件的字段定义](https://docs.go-cqhttp.org/event/#%E7%A7%81%E8%81%8A%E6%B6%88%E6%81%AF)

|参数名称|类型|
|:---:|:---:|
|raw_event|`from typing import Dict`|
|bot|`from pepperbot.adapters.onebot.api import OnebotV11PrivateBot`|
|chain|`from pepperbot.core.message.chain import MessageChain`|

```py
from typing import Dict
from pepperbot.adapters.onebot.api import OnebotV11PrivateBot
from pepperbot.core.message.chain import MessageChain


class MyHandler:
    async def temp_message(
        raw_event: Dict,
        bot: OnebotV11PrivateBot,
        chain: MessageChain,
    ):
        pass
```

## friend_message

> 好友私聊消息  [原始事件的字段定义](https://docs.go-cqhttp.org/event/#%E7%A7%81%E8%81%8A%E6%B6%88%E6%81%AF)

|参数名称|类型|
|:---:|:---:|
|raw_event|`from typing import Dict`|
|bot|`from pepperbot.adapters.onebot.api import OnebotV11PrivateBot`|
|chain|`from pepperbot.core.message.chain import MessageChain`|

```py
from typing import Dict
from pepperbot.adapters.onebot.api import OnebotV11PrivateBot
from pepperbot.core.message.chain import MessageChain


class MyHandler:
    async def friend_message(
        raw_event: Dict,
        bot: OnebotV11PrivateBot,
        chain: MessageChain,
    ):
        pass
```

## friend_message_been_withdraw

> 尚未实现

|参数名称|类型|
|:---:|:---:|
|raw_event|`from typing import Dict`|
|bot|`from pepperbot.adapters.onebot.api import OnebotV11PrivateBot`|
|chain|`from pepperbot.core.message.chain import MessageChain`|

```py
from typing import Dict
from pepperbot.adapters.onebot.api import OnebotV11PrivateBot
from pepperbot.core.message.chain import MessageChain


class MyHandler:
    async def friend_message_been_withdraw(
        raw_event: Dict,
        bot: OnebotV11PrivateBot,
        chain: MessageChain,
    ):
        pass
```

