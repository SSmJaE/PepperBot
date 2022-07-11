## inline_query

|参数名称|类型|
|:---:|:---:|
|raw_event|`from typing import Dict`|
|client|`from pyrogram.client import Client`|
|inline_query|`from pyrogram.types.inline_mode.inline_query import InlineQuery`|

```py
from typing import Dict
from pyrogram.client import Client
from pyrogram.types.inline_mode.inline_query import InlineQuery


class MyHandler:
    async def inline_query(
        raw_event: Dict,
        client: Client,
        inline_query: InlineQuery,
    ):
        pass
```

## callback_query

|参数名称|类型|
|:---:|:---:|
|raw_event|`from typing import Dict`|
|client|`from pyrogram.client import Client`|
|callback_query|`from pyrogram.types.bots_and_keyboards.callback_query import CallbackQuery`|

```py
from typing import Dict
from pyrogram.client import Client
from pyrogram.types.bots_and_keyboards.callback_query import CallbackQuery


class MyHandler:
    async def callback_query(
        raw_event: Dict,
        client: Client,
        callback_query: CallbackQuery,
    ):
        pass
```

## edited_message

|参数名称|类型|
|:---:|:---:|
|raw_event|`from typing import Dict`|
|client|`from pyrogram.client import Client`|
|message|`from pyrogram.types.messages_and_media.message import Message`|
|bot|`from pepperbot.adapters.telegram.api import TelegramPrivateBot`|
|chain|`from pepperbot.core.message.chain import MessageChain`|

```py
from typing import Dict
from pyrogram.client import Client
from pyrogram.types.messages_and_media.message import Message
from pepperbot.adapters.telegram.api import TelegramPrivateBot
from pepperbot.core.message.chain import MessageChain


class MyHandler:
    async def edited_message(
        raw_event: Dict,
        client: Client,
        message: Message,
        bot: TelegramPrivateBot,
        chain: MessageChain,
    ):
        pass
```

## private_message

|参数名称|类型|
|:---:|:---:|
|raw_event|`from typing import Dict`|
|client|`from pyrogram.client import Client`|
|message|`from pyrogram.types.messages_and_media.message import Message`|
|bot|`from pepperbot.adapters.telegram.api import TelegramPrivateBot`|
|chain|`from pepperbot.core.message.chain import MessageChain`|

```py
from typing import Dict
from pyrogram.client import Client
from pyrogram.types.messages_and_media.message import Message
from pepperbot.adapters.telegram.api import TelegramPrivateBot
from pepperbot.core.message.chain import MessageChain


class MyHandler:
    async def private_message(
        raw_event: Dict,
        client: Client,
        message: Message,
        bot: TelegramPrivateBot,
        chain: MessageChain,
    ):
        pass
```

## group_message

|参数名称|类型|
|:---:|:---:|
|raw_event|`from typing import Dict`|
|client|`from pyrogram.client import Client`|
|message|`from pyrogram.types.messages_and_media.message import Message`|
|bot|`from pepperbot.adapters.telegram.api import TelegramGroupBot`|
|chain|`from pepperbot.core.message.chain import MessageChain`|

```py
from typing import Dict
from pyrogram.client import Client
from pyrogram.types.messages_and_media.message import Message
from pepperbot.adapters.telegram.api import TelegramGroupBot
from pepperbot.core.message.chain import MessageChain


class MyHandler:
    async def group_message(
        raw_event: Dict,
        client: Client,
        message: Message,
        bot: TelegramGroupBot,
        chain: MessageChain,
    ):
        pass
```

