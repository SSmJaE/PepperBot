---
title: 调用 API
---


在 PepperBot 中，所有的主动行为，比如发送群消息，接受加群请求，上传群文件，踢出群成员，都是通过调用 API 实现的

## 有哪些 API

所以 PepperBot 有哪些 API 呢？完整的 API 参考文档[在此]

PepperBot 标榜自己是一个“符合直觉”的框架，所以，所有的 API，绑定的`class`，基本都是和 API 有联系的，比如

对于`消息链`，或者说一条消息，比较符合直觉的操作，可以有“撤回这条消息”，“直接回复这条消息”之类，所以，在 chain 对象上，我们绑定了如下方法

```py
await chain.withdraw()
await chain.reply(
    Text("在QQ中，会自动使用消息的‘回复’功能")
)
```

对于发送当前消息的`群成员`来说，比较符合直觉的操作有“禁言该成员”，“踢出该成员”之类的操作，所以又

```py
await sender.ban(30) # 禁言30分钟
await sender.kick()
```

像“主动发送一条消息”，“主动上传群文件”之类的操作，显然，是由`bot`自己完成的，所以相应的

```py
await bot.group_message(Text("一条跨平台群消息"))
await bot.upload_group_file("filepath")
```

## 选择合适的 API

是否有注意到，在上方的的 API 示例中，我们并没有提供“QQ 群号”，“QQ 号”之类的参数？

为了尽量的减少模板代码，PepperBot 假设，所有操作，默认都是对当前发生的事件所在的群操作的，这样的话，用户就不需要手动注入很多“已知”的参数了

但是，如果我们想要实现类似，“当在 A 群收到消息时，向 B 群发送一条消息”，甚至“当在 QQ 的 A 群收到消息时，向微信的 B 群发送一条消息”，要怎么办呢？

这里，我们引入了`arbitrary API`(中文“任意 API”的意思)

:::info PepperBot 的 API 架构
简单来说，对于不同的平台(QQ、微信)，PepperBot 分别实现了对应的`adapter`，API 都是绑定到对应的`adapter`上的，`arbitrary API`，实际上，就是直接调用`adapter`上的 API，而不是绑定在如`bot`, `chain`上的，已经封装过一次的 API

具体见[贡献指南/更多 API]
:::

在上方举例的，`bot`，`chain`等对象的 API，都是没有前缀(`onebot`,`keaimao`)的，也就是说，他们都是跨平台的 API，收到 QQ 消息时，API 内部会自动调用 QQ 协议端(go-cqhttp)的接口，同理，收到微信消息时，API 内部会调用微信协议端(可爱猫)的接口

当我们使用 `arbitrary API`时，并没有这样的“自动化”，每次调用时，我们需要手动选择对应的平台

比如，想要调用 QQ 的群消息 API

```py
from pepperbot.adapters.onebot.api import OnebotV11Api

async def group_message(self):
    await OnebotV11Api.group_message("123456", Text("只发送给QQ的消息"))
```

调用微信的群消息 API

```py
from pepperbot.adapters.keaimao.api import KeaimaoApi

async def group_message(self):
    await KeaimaoApi.group_message("123456@chatroom", Text("只发送给微信的消息"))
```

每次使用`arbitrary API`时，都要导入，很麻烦，所以在`bot`上，直接绑定了`arbitrary API`，可以直接这样使用

```py
async def group_message(self, bot: UniversalGroupBot):
    await bot.arbitrary.onebot.group_message("123456", Text("QQ消息"))
    await bot.arbitrary.keaimao.group_message("123456@chatroom", Text("微信消息"))
```

封装过的 API，默认发送至当前消息来源，而我们使用`arbitrary API`时，则需要手动指定

### 在`handler`外部使用 arbitrary 风格的 API

在`bot`身上，我们绑定了 arbitrary 这样的工具字段，但是如果我们想要在`handler`外部，比如实现定时任务或者一次性任务时，也想要实现 arbitrary.onebot 这样的效果，而不是手动导入，要怎么做呢？

```py
from pepperbot.core.bot.universal import ArbitraryApi

async def main():
    ArbitraryApi.onebot.group_message("123456", Text("QQ消息"))

asyncio.run(main())
```

### 在跨平台事件内部，判断消息来源

但是现在，我们还是没法实现"QQ 中收到消息后，向微信发送消息"的功能，因为我们并不知道，我们收到的事件来自何方

可以通过`protocol`来判断，在`bot`上，我们绑定了一些工具属性

比如，当消息来自 QQ 时，`bot.onebot`为 True，不然为 False

但消息来自于微信是，`bot.keaimao`为 True，不然为 False

现在，我们可以实现我们的目标了

```py
async def group_message(self, bot: UniversalGroupBot, chain: MessageChain):
    if bot.onebot: # 转发qq消息至微信
        await bot.arbitrary.keaimao.group_message("19521241254@chatroom", *chain.segments)

    if bot.keaimao: # 转发微信消息至qq
        await bot.arbitrary.onebot.group_message("1041902989", *chain.segments)
```

### 获取需要的参数

那么，从哪里获取`群号`,`QQ号`呢？

PepperBot 中，所有的事件，都有`raw_event`这个参数，也就是未经 PepperBot 处理的，直接从`协议端`接受到的事件，都是字典格式

关于字典的字段，可以查看`go-cqhttp`和`可爱猫`自己的文档

```py
async def group_message(self, raw_event: Dict):
    if bot.onebot:
        group_id = raw_event["group_id"]
```

`bot`, `chain`等对象上，也有绑定一些参数，具体见[文档]

```py
bot.bot_id
chain.source_id
```

## PepperBot 未实现，但是`协议端`实现了的 API

PepperBot 只封装了最常用，最值得封装的 API，所以想要调用 PepperBot 尚未封装的 API 时，我们可以使用`api_caller`

`api_caller`其实就是一个维持了 session 的 http 客户端，方便我们向`协议端`发送 http 请求。PepperBot 中，基于`httpx`实现

不同平台的`api_caller`，都存放在 api_callers 中，但是每次通过

```py
api_callers["protocol"]
```

的形式调用，多少有些不便，所以提供了几个工具函数

```py
from pepperbot.store.meta import get_onebot_caller, get_keaimao_caller
```

`api_caller`都实现了这样的接口

```py
async def api_caller(action: str, **kwargs):
    ...
```

所以，我们可以总结出这样的用法

```py
await get_onebot_caller()("action", arg1="arg1", arg2=222, arg3=True)
```

action 一般对应具体的操作，在`go-cqhttp`中，对应 api 的`path`，在`可爱猫`中，对应 api 的`EventType`，诸如此类

kwargs 对应其余参数

:::info
注意，get_onebot_caller 之类的函数，返回的是 api_caller 对象，其本身也是可调用的，也就是说，要()()两次

```py
await get_onebot_caller()("action", arg1="arg1")
```

等价于

```py
onebot_caller = get_onebot_caller()
await onebot_caller("action", arg1="arg1")
```

:::
