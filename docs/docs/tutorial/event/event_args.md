---
title: 事件参数
---

在了解 PepperBot 的[事件响应机制](./mechanism.md)之后，我们可以进一步研究，如何根据实际情况，选择和使用我们需要的参数了

事件和参数之间有一个大概的关系，也就是“每个事件，都有其对应的参数”

## “智能”的参数识别

python 是一门十分灵活的语言，通过 python 的元编程手段，我们可以按需选择我们用到的参数，多余的参数可以不写

而且参数的顺序，也是完全无所谓的，只要保证 self 是第一个即可

如果你对 PepperBot 是如何实现这一点感到好奇的话，可以看一下[技术细节]

来看一个具体的例子，还是`group_message`事件，对应的参数列表[在此](../../API/事件参数/跨平台.md)

可以看到，群消息事件有`raw_event`, `chain`, `bot`这三个参数，`raw_event`是从`协议端`收到的，未经处理的原始事件，`bot`身上绑定了许多 API，`chain`是[消息链](./message_chain.md)

根据我们的业务逻辑不同，可能会使用到这三个参数中的其中几个，也可能是全部，我们只需要按需定义我们用到的参数即可

比如，我们只用到了`bot`参数，那么我们只需要

```py
async def group_message(self, bot: UniversalGroupBot):
    ...

```

即可，`chain`和`raw_event`这两个没用到的参数，甚至到可以不用定义

如果我们的业务逻辑变了，需要用到`chain`这个参数了，我们只需要加上`chain`即可

直接在`bot`后面加入

```py
async def group_message(self, bot: UniversalGroupBot, chain: MessageChain):
    pass
```

或者在`bot`之前加入

```py
async def group_message(self, chain: MessageChain, bot: UniversalGroupBot):
    pass
```

都是可以的，参数的顺序也是完全无所谓的

:::warning
PepperBot 是完全类型提示的，所以我们也建议开发者使用完全的类型提示

表现在事件响应的定义上，所有参数也需要提供类型注解，且类型注解需要与对应的类型一致
:::

:::info
类型提示保证使用的正确

vscode 配合 pylance 插件，或者 pycharm，都对 python 的类型注解有着不错的支持
:::

## 参数的类型

上文提到，PepperBot 是完全类型提示的，我们也建议开发者使用类型注解

所以如果出现这样的定义

```py
class WhateverNameYouWant:

    async def group_message(self, bot, chain,):
        pass
```

在 PepperBot 初始化时，就会出现友好的报错

```
群消息事件响应.py中的类响应器WhateverNameYouWant的group_message事件的参数bot未提供类型注解，其类型
为<class 'pepperbot.parse.bots.GroupCommonBot'>
```

pepperbot.parse.bots.GroupCommonBot，提示了该类型的导入路径

如果类型错误，如

```py
async def group_message(self, bot:int, chain,):
        pass
```

则会提示

```
群消息事件响应.py中的类响应器WhateverNameYouWant的
group_message事件的参数bot的类型应该为<class 'pepperbot.parse.bots.GroupCommonBot'>，而不是<class 'int'>
```

## 不存在的参数

```py
async def group_message(self, bottt,):
        pass
```

如果参数名不存在与该事件可用的参数中，则会提示

```
群消息事件响应.py中的类响应器WhateverNameYouWant的group_message事件不存在参数bottt
可用的参数及类型有bot: <class 'pepperbot.parse.bots.GroupCommonBot'>, sender: <class 'pepperbot.models.sender.Sender'>, chain: <class 'pepperbot.message.chain.MessageChain'>, event: typing.Union[dict, typing.Dict, typing.Dict[str, typing.Any]]
```

`raw_event: typing.Union[dict, typing.Dict, typing.Dict[str, typing.Any]`

这里看到了一长串 type hints，不用害怕，这是 Union type，我们只需要从中选择一种即可

比如`raw_event : dict`
