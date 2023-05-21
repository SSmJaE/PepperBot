## callback_query

|参数名称|类型|
|:---:|:---:|
|callback_query|from pyrogram.types.bots_and_keyboards.callback_query import CallbackQuery|
|raw_event|from typing import Dict|
|client|from pyrogram.client import Client|

```python
from pyrogram.types.bots_and_keyboards.callback_query import CallbackQuery
from typing import Dict
from pyrogram.client import Client


class MyHandler:
    async def callback_query(
        self,
        callback_query: CallbackQuery,
        raw_event: Dict,
        client: Client,
    ):
        pass

```

## chosen_inline_result

|参数名称|类型|
|:---:|:---:|
|raw_event|from typing import Dict|
|client|from pyrogram.client import Client|

```python
from typing import Dict
from pyrogram.client import Client


class MyHandler:
    async def chosen_inline_result(
        self,
        raw_event: Dict,
        client: Client,
    ):
        pass

```

## edited_message

|参数名称|类型|
|:---:|:---:|
|message|from pyrogram.types.messages_and_media.message import Message|
|bot|from pepperbot.adapters.telegram.api import TelegramPrivateBot|
|chain|from pepperbot.core.message.chain import MessageChain|
|raw_event|from typing import Dict|
|client|from pyrogram.client import Client|

```python
from pyrogram.types.messages_and_media.message import Message
from pepperbot.adapters.telegram.api import TelegramPrivateBot
from pepperbot.core.message.chain import MessageChain
from typing import Dict
from pyrogram.client import Client


class MyHandler:
    async def edited_message(
        self,
        message: Message,
        bot: TelegramPrivateBot,
        chain: MessageChain,
        raw_event: Dict,
        client: Client,
    ):
        pass

```

## group_message

|参数名称|类型|
|:---:|:---:|
|message|from pyrogram.types.messages_and_media.message import Message|
|bot|from pepperbot.adapters.telegram.api import TelegramGroupBot|
|chain|from pepperbot.core.message.chain import MessageChain|
|raw_event|from typing import Dict|
|client|from pyrogram.client import Client|

```python
from pyrogram.types.messages_and_media.message import Message
from pepperbot.adapters.telegram.api import TelegramGroupBot
from pepperbot.core.message.chain import MessageChain
from typing import Dict
from pyrogram.client import Client


class MyHandler:
    async def group_message(
        self,
        message: Message,
        bot: TelegramGroupBot,
        chain: MessageChain,
        raw_event: Dict,
        client: Client,
    ):
        pass

```

## inline_query

|参数名称|类型|
|:---:|:---:|
|inline_query|from pyrogram.types.inline_mode.inline_query import InlineQuery|
|raw_event|from typing import Dict|
|client|from pyrogram.client import Client|

```python
from pyrogram.types.inline_mode.inline_query import InlineQuery
from typing import Dict
from pyrogram.client import Client


class MyHandler:
    async def inline_query(
        self,
        inline_query: InlineQuery,
        raw_event: Dict,
        client: Client,
    ):
        pass

```

## private_message

|参数名称|类型|
|:---:|:---:|
|message|from pyrogram.types.messages_and_media.message import Message|
|bot|from pepperbot.adapters.telegram.api import TelegramPrivateBot|
|chain|from pepperbot.core.message.chain import MessageChain|
|raw_event|from typing import Dict|
|client|from pyrogram.client import Client|

```python
from pyrogram.types.messages_and_media.message import Message
from pepperbot.adapters.telegram.api import TelegramPrivateBot
from pepperbot.core.message.chain import MessageChain
from typing import Dict
from pyrogram.client import Client


class MyHandler:
    async def private_message(
        self,
        message: Message,
        bot: TelegramPrivateBot,
        chain: MessageChain,
        raw_event: Dict,
        client: Client,
    ):
        pass

```

## raw_update

|参数名称|类型|
|:---:|:---:|
|raw_event|from typing import Dict|
|client|from pyrogram.client import Client|

```python
from typing import Dict
from pyrogram.client import Client


class MyHandler:
    async def raw_update(
        self,
        raw_event: Dict,
        client: Client,
    ):
        pass

```

