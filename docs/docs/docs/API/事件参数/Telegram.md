



# 

## inline_query

|参数名称|类型|
| :---: | :---: |
|raw_event|typing.Dict|
|client|<class 'pyrogram.client.Client'>|
|inline_query|<class 'pyrogram.types.inline_mode.inline_query.InlineQuery'>|

## callback_query

|参数名称|类型|
| :---: | :---: |
|raw_event|typing.Dict|
|client|<class 'pyrogram.client.Client'>|
|callback_query|<class 'pyrogram.types.bots_and_keyboards.callback_query.CallbackQuery'>|

## private_message

|参数名称|类型|
| :---: | :---: |
|raw_event|typing.Dict|
|client|<class 'pyrogram.client.Client'>|
|message|<class 'pyrogram.types.messages_and_media.message.Message'>|
|bot|<class 'pepperbot.adapters.telegram.api.TelegramPrivateBot'>|
|chain|<class 'pepperbot.core.message.chain.MessageChain'>|

## group_message

|参数名称|类型|
| :---: | :---: |
|raw_event|typing.Dict|
|client|<class 'pyrogram.client.Client'>|
|message|<class 'pyrogram.types.messages_and_media.message.Message'>|
|bot|<class 'pepperbot.adapters.telegram.api.TelegramGroupBot'>|
|chain|<class 'pepperbot.core.message.chain.MessageChain'>|
