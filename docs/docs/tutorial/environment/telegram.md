---
title: Telegram
---

## 技术选型

由于`Telegram`开放的机器人生态，市面上已经有非常多第三方的机器人框架

同时，当前(2022年)，还尚未有可用的onebot telegram协议实现，如果要在实现`PepperBot`的同时，实现符合`onebot`的`Telegram`协议，工作量有点太大，所以最终选择，直接整合[`pyrogram`](https://docs.pyrogram.org/)，一个生态还算不错，异步的`Telegram`协议实现，

`pyrogram`支持`MTProto`，也就是说，可以直接与`Telegram`的bot(比如bot father)交互，实现模拟用户的能力

即使使用bot账号，我们也需要配置`api_id`和`api_hash`，因为我们使用了`MTProto`直接和`Telegram`主服务器通信，这也是`pyrogram`可以模拟用户操作的前提

比仅仅使用`bot_token`进行的中转通信，会快上不少

## 配置

因为`pyrogram`也是基于python，而且已经封装好了和`Telegram`主服务器的通信，所以没有必要再抽象成协议端

因此，配置`Telegram`时，我们使用的并不是一贯的`bot.register_adapter`，而是`bot.register_telegram`

```py
bot.register_telegram(
    "telegram", # 随意设置
    api_id=12345,
    api_hash="kalsjdflajfksdjfkasdf",
    bot_token="1237928:dakhfkajsdhfasdhfldhkfh",
    proxy={
        "scheme": "http",
        "hostname": "127.0.0.1",
        "port": 1080,
    },
)
```

proxy代理是可选的，不过一般需要，毕竟可能被墙

`bot.register_telegram`其实只是转发了一下参数，转发给谁呢？`pyrogram`的[`Client`](https://docs.pyrogram.org/api/client)

`bot.register_telegram`的参数，直接看`Client`的文档即可

常用参数，就是上方代码片段中所展现的

`pyrogram`中的`Client`，和`PepperBot`中的`api_caller`或者说`ProtocolApi`概念很像，封装了各种常用的api接口，比如`send_message`，`add_user`之类

既然`pyrogram`已经实现了这样的功能，那我们就直接拿来用

## 简单示例

当配置好之后，其实和`Onebot`、`可爱猫`的使用一样，又回到了经典的`PepperBot`风格的事件响应机制上

目前已经适配的事件，[见此](../../API/事件参数/Telegram.md)

可以看到，`pyrogram`的`client`，也是事件参数之一，可以直接调用`client`上绑定的方法

直接通过`get_telegram_caller`，返回的也是同一个`client`

`Telegram`的消息类型的事件中，比如`group_message`，`private_message`，也有`bot`对象，使用和其它协议一致

也同样支持`chain`

```py
class MyHandler:
    async def telegram_private_message(
        self,
        raw_event: Dict,
        client: Client,
        message: Message,
        chain: MessageChain,
        bot: TelegramPrivateBot,
    ):
        await bot.private_message(
            Text("test"),
            Text("test2"),
        )

        await message.reply(message.text)
```

## 直接使用`pyrogram`的参数

仔细查看`pyrogram`的[`update handlers`](https://docs.pyrogram.org/api/handlers#pyrogram.handlers.MessageHandler)文档，我们可以发现，每个`handler`都有一个特殊的参数，比如`MessageHandler`中的`Message`，我们在`PepperBot`的事件参数中，也可以访问到，名称和类型都和`pyrogram`的一致

所以`Message`对象上，绑定的`send_message`，`reply_message`等方法，也可以直接调用，不用非得通过`PepperBot`的`bot`对象或者`chain`对象

```py
class MyHandler:
    async def telegram_callback_query(
        self,
        raw_event: Dict,
        client: Client,
        callback_query: CallbackQuery,
    ):
        await callback_query.answer(
            f"Button contains: '{callback_query.data}'",
            show_alert=True,
        )

    async def telegram_inline_query(
        self,
        raw_event: Dict,
        client: Client,
        inline_query: InlineQuery,
    ):
        await inline_query.answer(
            results=[
                InlineQueryResultArticle(
                    title="Installation",
                    input_message_content=InputTextMessageContent(
                        "Here's how to install **Pyrogram**"
                    ),
                    url="https://docs.pyrogram.org/intro/install",
                    description="How to install Pyrogram",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(
                                    "Open website",
                                    url="https://docs.pyrogram.org/intro/install",
                                )
                            ]
                        ]
                    ),
                ),
                InlineQueryResultArticle(
                    title="Usage",
                    input_message_content=InputTextMessageContent(
                        "Here's how to use **Pyrogram**"
                    ),
                    url="https://docs.pyrogram.org/start/invoking",
                    description="How to use Pyrogram",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(
                                    "Open website",
                                    url="https://docs.pyrogram.org/start/invoking",
                                )
                            ]
                        ]
                    ),
                ),
            ],
            cache_time=1,
        )
```
