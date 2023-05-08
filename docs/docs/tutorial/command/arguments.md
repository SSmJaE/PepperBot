---
title: 指令的参数
---

`PepperBot`中，不管是`class handler`的`event handler`，还是`class command`的`method`，所有的参数，都是按需使用的

如果用的到的话，就在该`method`的函数签名中定义即可

“稳定”参数的顺序是无所谓的，`CLIArgument`的顺序，需要和用户的输入一致

还是一贯的`PepperBot`风格，所有参数，都需要提供类型注解

## 可用的参数

> 这些参数是稳定存在的，这里的稳定，是相对于`CLIArgument`这样，可以任意定义的随意性

| 配置名称  | 配置类型        | 可用于            |
| --------- | --------------- | ----------------- |
| prefix    | `str`           | 所有 method       |
| alias     | `str`           | 所有 method       |
| context   | `dict or Dict`          | 所有 method       |
| raw_event   | `dict or Dict`          | 所有 method       |
| history   | `list or List`          | 所有 method       |
| config    | `Optional[Any]` | 所有 method       |
| exception | `Exception`     | 仅`catch`生命周期 |
| sender| `CommandSender`| 所有method|
| chain | `MessageChain` | 所有method|
|stop_propagation | `T_StopPropagation` | 生命周期除外 |

## prefix，前缀

最终触发当前指令的前缀

## alias，别名

最终触发当前指令的指令的名称

## context，上下文字典

可以通过该字典，在当前指令的不同 method 中，传递变量；跨进程

是一个从外部传入的dict的应用，所以如果要清空当前指令的context的话，用context.clear()，而不要直接context = {}

## raw_event，原始事件

原始(未处理的)事件，和class handler中的一致

## history，历史记录

存储历次事件的 raw_event，以及所有成功匹配的 pattern 的结果

如果有参数解析，只有成功解析了参数的用户输入，会被收录

可以通过在函数签名中，定义`history`参数，来获得

```py
from typing import List
from pepperbot.store.command import HistoryItem

async def func(self, history: List[HistoryItem]):
    for history_item in history:

```

`HistoryItem`绑定了历次成功触发对应`method`的`chain`和`raw_event`

```python
history_item.chain
history_item.raw_event
```

## config，配置

如果用户配置了`as_command`中的 config 参数，这可以从这里获取到

## sender，消息发送者

提供`send_message`、`reply`等消息交互能力的对象，自动处理普通消息来源(群聊、私聊)以及协议(QQ、微信、Telegram)

可以发现，我们在指令中，并没有使用 bot.group_message 之类的 api，而是 sender.send_message

那么，我们为什么引入 sender 这样一个新概念呢？

sender，其实就是个快捷方式，自动向不同消息来源的对象发送消息的快捷方式

因为作为指令的话，你不知道，用户是从私聊消息，还是从群消息发送的

新引入 sender 对象，通过 sender.send_message，可以自动判断，不需要手动 bot.onebot 之类了

当然，我们在指令中也是可以继续使用 bot.xxx 风格的 api 的，见`arbitrary API`

## exception，异常

除了`catch`自身和`cleanup`，其他所有 method 抛出的异常

## chain，消息链

和`class handler`中`group_message`等消息事件的`chain`参数一致，当前消息链

## stop_propagation，停止传播

用来阻断传播，具体见[事件传播与优先级](../advance/propagation.md)
