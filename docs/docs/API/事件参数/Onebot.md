## group_message

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

## friend_message

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

