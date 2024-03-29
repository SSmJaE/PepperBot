---
title: 路由
---


我们经常会有这样的使用需求

- 某些群，或者某些特定的好友，只针对他们执行机器人的某些功能
- 某些功能，对所有群都启用
- 你手头有一份白名单，其中的用户 id(QQ 号、微信号)是动态添加、删除的，你只希望机器人响应白名单中的用户/群

通过 `PepperBot` 提供的 django/starlette 风格的路由，可以轻松地实现这些功能

## 最简单的 `register`

如果你希望对任意消息来源(群、好友)响应，可以使用没有任何参数的 `register` 装饰器

```py
from pepperbot.core.route import register

@register()
class YourClassHandler:
    async def group_message(self,...):
        ...
```

:::info
`register` 的参数与 `BotRoute` 完全相同，可以理解为 flask 风格的路由控制

当你仅有一个 `handler` 时，可以考虑使用 `register`；复杂情况还是使用 `BotRoute` 更直观
:::

## apply_routes

我们在环境配置中，已经实例化了一个 bot，通过 bot 的 `apply_routes` 方法，可以注册多个 `BotRoute`，以实现复杂的权限控制

`apply_routes` 接受一个列表，其中每一个元素都是一个 `BotRoute` 的实例

```py
from pepperbot.core.route import BotRoute

bot.apply_routes([
    BotRoute(),
    BotRoute(),
    ...
])
```

## 默认情况

默认情况下，`BotRoute` 响应所有的消息来源

```py
BotRoute()
```

等价于

```py
BotRoute(groups="*", friends="*")
```

## 全局事件响应器&指令

假设我们有一个名为`MyHandler`的事件响应器(class based event handler)，我们希望它响应所有的消息来源

我们可以

```py
bot.apply_routes([
    BotRoute(handlers=[MyHandler]),
])
```

如果你想要的直观一点，可以把对群消息和私聊消息的配置也加上

```py
bot.apply_routes([
    BotRoute(
        groups="*",
        friends="*",
        handlers=[MyHandler],
    ),
])
```

假设你有名为`指令1`，`指令2`，`指令3`，这三个指令，希望把他们应用到全局

同理

```py
bot.apply_routes([
    BotRoute(
        groups="*",
        friends="*",
        commands=[指令1, 指令2, 指令3],
    ),
])
```

你也可以同时指定全局事件响应器和指令

```py
bot.apply_routes([
    BotRoute(
        groups="*",
        friends="*",
        handlers=[ MyHandler ],
        commands=[指令1, 指令2, 指令3],
    ),
])
```

## 指定消息来源

如果我们只希望响应某些消息来源，那么需要我们手动指定

需要指定协议和 id(QQ 号、群号、微信号)

```py
BotRoute(
    groups={
        "onebot": ["1041902989"],
        "keaimao": ["19521241254@chatroom"],
    },
    handlers=[MyHandler]
),
```

其中，`groups` 对应群号，`friends` 对应 QQ 号、微信号

:::info
你可以配置两个 `BotRoute`，其中一个配置全局响应，另一个配置指定消息来源
:::

:::info
微信群号，可以先绑定任意群，从事件中查看
:::

## 一个协议指定来源，另一个协议全局应用

可以配置一个协议响应指定消息来源，另一个协议全局响应

```py
BotRoute(
    groups={
        "onebot": "*",
        "keaimao": ["19521241254@chatroom"],
    },
    handlers=[MyHandler]
),
```

## 不响应

设置为 `None`，即可不响应该类型的消息

比如，我只想响应群消息，不想响应私聊消息

```py
BotRoute(
    groups="*",
    friends=None,
    handlers=[MyHandler]
),
```

## 动态判断是否响应消息来源

我们可以通过提供一个 `validator`，来动态的判断是否响应

函数签名如下

```py
def validator(bot_protocol : Literal["onebot", "keaimao", "telegram"], source_id : str)-> bool:
    ...
```

即，我们定义的 `validator`，会接收到两个参数，第一个是协议名称，第二个是消息来源的 id

需要返回 `bool`，如果为 `True`，就响应

一个简单的示例

```py
BotRoute(
    handlers=[MyHandler]
    groups=is_valid_group,
    friends=is_valid_friend,
)
```

## 合到一起的最佳实践

`BotRoute` 提供了强大的可定制性，但是如果将所有的配置都耦合到一起，时间长了，难免会有点难以理解

既然我们可以应用任意个 `BotRoute`，完全可以让一个 `BotRoute` 只做一件事

比如

- 负责全局指令的 `route`
- 负责配置群消息的 `route`
- 负责配置私聊消息的 `route`
- 负责动态判断的 `route`

等等

这样，我们的 `handler` 也可以分开来定义，不用都放在一起

## 重复的指令

假定有一条`指令1`(`handler` 同理)，你同时将其注册为全局指令，指定了消息来源，指定了动态 `validator`，而后两者又同时满足

也就是说，我们现在有 3 条 `route` 规则，指向了同一个 `handler`

```py
bot.apply_routes(
    [
        # 为所有消息渠道注册的commands
        BotRoute(
            groups="*",
            friends="*",
            commands=[指令1],
        ),
        # 指定消息来源
        BotRoute(
            groups={
                "onebot": ["1041902989"],
                "keaimao": ["19521241254@chatroom"],
            },
            friends=None,
            commands=[指令1],
        ),
        # 动态判断消息渠道
        BotRoute(
            groups=is_valid_group,
            friends=None,
            commands=[指令1],
        ),
    ]
)
```

PepperBot 内部做了处理，对同一个 `handler` 或者指令，一次事件响应只会触发一次
