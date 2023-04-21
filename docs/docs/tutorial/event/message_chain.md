---
title: 消息链
---

## 最后一步

在真正开始动手定义事件响应之前，我们最后，还需要了解一下`消息链`的概念

## 为什么称为链

`消息链`就是我们实际上接受到的消息，通常又有表情，又有文字，或者又有文字，又有图片

组成消息的每一个单元，称为一个`消息片段`

比如这样一条消息

![](../../../static/img/1.png)

实际上由三个`消息片段`组成，分别是

- 文字片段(Text)——12345
- 表情片段(Face)——滑稽
- 文字片段(Text)——67890

## 消息链的跨平台

显而易见的是，QQ 的消息结构和微信的是不同的，QQ 的一条消息，可以同时包含文字、表情、图片，而微信一次只能包含一种类型，要么文字，要么图片，要么表情

为了兼容性考虑，以 QQ 的`消息链`模型为蓝本，也就是说，微信消息所组成的`消息链`，每次只有一个`消息片段`

如果你通过 API，向微信发送了一个有多个`消息片段`的`消息链`，PepperBot 会将`消息链`拆开，每次只发送一个`消息片段`

## 可用的消息片段

PepperBot 的消息类型基本符合 OneBot 协议，因为主要后端是 go-cqhttp，所以以 go-cqhttp 支持的有限

可用的消息片段可以参考[此处](./message_segment.md)

go-cqhttp 对消息片段的支持，可见[此处](https://docs.go-cqhttp.org/cqcode/#qq-%E8%A1%A8%E6%83%85)

:::info
发送语音和视频，需要将 ffmpeg 放至 go-cqhttp.exe 同目录下，或者将 ffmpeg 的可执行文件添加至系统变量
:::

## 未实现的消息片段

PepperBot并未实现所有QQ、微信支持的消息片段，如果PepperBot接受到尚未适配的消息类型，会报错

TODO : 注意，某些消息片段，并不能跨平台，打算实现，可以通过配置控制，遇到不能跨平台的消息片段，是直接报错，还是忽略

## 接受到的消息链

在接受到群消息之后，PepperBot 会自动将接收到的消息，转换成符合 PepperBot 的`消息链`，并在`消息链`上绑定了一些属性和方法，便于操作`消息链`

事件的参数中，类型为 `MessageChain` 的 `chain` 参数，即为`消息链`

`chain`上的`segments`属性，即 `chain.segments`，就是所有的`消息片段`了，他是一个列表，包含所有消息片段，可以迭代

当然，也可以直接迭代指定类型的`消息片段`，

比如迭代所有图片，可以直接

```py
for image in chain.images:
    ...
```

迭代所有表情

```py
for face in chain.faces:
    ...
```

诸如此类

文字有所不同，并没有提供 `chain.text` 这样一个属性，而是提供了 `chain.pure_text`,

还是![](../../../static/img/1.png)这个例子

`chain.pure_text` 无视了两个文字片段中间的`表情类型片段`，最后组合成了一个字符串，字符串的值为"1234567890"

其它消息类型，比如文字+图片+文字，也会忽略`文字片段`之间的`图片片段`，只拼接`文字片段`

`pure_text` 在判断消息的文字内容时比较有用

## 操作消息链

### 字符串可以直接 in

```py
assert "word" in chain
```

实际上就是判断

```py
"word" in chain.pure_text
```

### 可以判断是否指定类型

```py
assert Text in chain
assert chain.has(Text) == True
```

所有消息片段中，是否有指定类型的消息片段

### 可以判断是否指定类型的实例

```py
assert Text("word2") not in chain
assert Text("word word") in chain
assert chain.has(Text("word word")) == True
assert chain.has(Text("word word1")) == False
assert chain.has(Face(123)) == True
assert chain.has(Face(124)) == False
```

所有消息片段中，是否有指定的消息类型的消息片段，同时，该消息片段的内容应与提供的一致

### 快捷方式

```py
assert chain.has_and_first(Text) == (True, Text("word word"))
assert chain.has_and_last(Text) == (True, Text("word word2"))
assert chain.has_and_all(Text) == (True, [Text("word word"), Text("word word2")])
```

如果有 Text 类型的消息片段，直接返回该消息片段

### 获取所有指定类型实例

```py
assert chain.faces == [Face(123)]
assert chain.text == [Text("word word"), Text("word word2")]
```

获取消息链中，所有指定类型的消息片段

### 按 index 取 Segment

```py
assert chain[1] == Text("word word")
```

已知 chain.segments 是一个列表，当然也应该可以按 index 获取

### 可以直接判断实例

```py
assert Text("word word") == Text("word word")
assert Text("word word") != Text("word word2")
```

消息片段之间，也是可以直接比较的

## 手动构造消息链

> PepperBot 提供了非常方便的构造消息片段，以及组合消息链的方式

PepperBot 中，所有涉及到传递`消息链`或者`消息片段`的函数，基本都实现了这样的函数签名

```py
async def group_message(*segments, iterable: Optional[Iterable]=[]):
    ...
```

根据这个签名，我们可以总结出以下通用/常用用法

:::info
\*segments 这样的语法，意思是 varargs，即任意个未知参数，具体可以见 python 官方文档，或者`流畅的 python` 一书
:::

### 直接传入

在调用 API 时，直接将`消息片段`作为参数，传入函数调用中

```py
await group_message(
    Text("123"),
    Image("filepath"),
    Text("456"),
)
```

### 列表解构

```py
predefined_message_chain = [
    Text("123"),
    Image("filepath"),
    Text("456"),
]
```

如果你在别处已经定义好了一个消息片段组成的列表/元组，想要将它作为 API 调用时使用的消息片段，有两种方法

直接列表解构

```py
await group_message(*predefined_message_chain)
```

或者使用关键词参数`iterable`

```py
await group_message(iterable=predefined_message_chain)
```

:::warning
不要同时使用`varargs`和`iterable`，如果同时使用了，会忽略`varargs`，只传递`iterable`指定的消息片段
:::

:::info 迭代器的多处使用

:::

### 函数返回

假设有一个返回由消息片段组成列表的函数

```py
def gen_message():
    return [
        Text("123"),
        Image("filepath"),
        Text("456"),
    ]
```

那么，可以像使用列表一样使用

```py
await group_message(*gen_message())

await group_message(iterable=gen_message())
```

如果函数只返回一个消息片段，那么可以

```py
def get_image():
    return Image("filepath")

await group_message(
    Text("123"),
    gen_image(),
    Text("456"),
)
```

## 消息链上绑定的方法

消息链上绑定的方法，都是跨平台的，

chain.reply

chain.withdraw()
