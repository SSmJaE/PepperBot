---
title: 事件响应机制
---


## PepperBot 的事件响应

事件响应的实现，很像是 Django 的类视图，如果你对 Django 很熟悉，对 PepperBot 的事件响应也一定很眼熟

```py
class MyClassHandler:
    async def group_message(self,...):
        ...

    async def group_request(self,...):
        ...

    async def been_invited_to_group(self,...):
        ...

    async def group_member_increased(self,...):
        ...
```

在 PepperBot 中，我们通过`类的方法`的名字，将所有事件映射了上去，就像 Django 的类视图，`get` 方法，对应 `get` 请求，`post` 方法，对应 `post` 请求，

在 PepperBot 中，比如，我们想处理群消息事件，我们只需要将`方法`的名字，设置为 `group_message`，当接收到群消息事件时，就会自动调用这个方法

同理，加群事件触发时，会自动调用 `group_request` 方法

:::info
并不需要定义所有事件对应的方法，只需要定义需要处理的事件即可
:::

## 同步还是异步？

方法可以同步也可以异步

```py
    def group_message(self):
        ...
```

和

```py
    async def group_message(self):
        ...
```

都是可以的

不过 PepperBot 的 API 基本都是异步的，所以建议没有讲究的话，默认选择异步就好

因为只有在async函数中，才能使用await关键字，其它和同步没啥区别

## 可用的事件名

目前尚未实现所有的事件，已实现的事件和对应的参数，可以参考[这个文件](../../API/事件参数/跨平台.md)

该参数列表的具体使用，我们会在[事件参数](./event_args.md)部分具体讲解

如果你打开了上方的文件，会发现事件根据平台做了区分，比如 QQ 的事件，都是以 onebot 开头的，微信的事件，都是以 keaimao 开头的

没有 onebot、keaimao 之类的前缀的事件，都是跨平台事件，我们接下来具体讨论

## 跨平台事件

什么是跨平台事件呢？比如群聊消息事件，如果我们说，我们实现了跨平台的群聊消息事件，意思就是，不管我们是接受到了 QQ 的群消息事件，还是微信的群消息事件，PepperBot 都会将其转化为统一的，PepperBot 风格的群消息事件，也就是说，我们可以在同一个函数定义中，实现对多个平台类似事件的响应。

不同平台的`协议端`，哪怕都只是发送一条文字消息，其实现的 API 也各不相同，如果要对每一个平台都手动选择对应的 API，显然很难称之为跨平台。为了解决跨平台的 API 调用，PepperBot 也提供了跨平台的，统一的 API。

我们可以通过 PepperBot 提供的统一的 API 书写逻辑，PepperBot 内部，会将跨平台的 API 调用，转化为各个平台特定的数据结构，这一切都是由框架完成的，所以用户看到的，就是在平台间保持一致的 API

总的来说，跨平台 == 跨平台事件 + 跨平台 API

API 的使用，会在[调用 API](../action/call_api.md)中具体讲解

## 平台独立事件

使用平台独立事件的场景有三种

### 第一，尚未实现跨平台事件，只能使用平台独立事件

### 第二，只想对特定平台的特定事件做出响应

比如，我们同时对接了 QQ 和微信的`协议端`，但是我们只想对 QQ 的私聊消息响应，只对微信的群聊消息响应，那么显然，此时直接使用平台独立事件，要比使用跨平台事件，再在其内判断消息是来自哪个平台，代码的可读性要好得多

```py

async def onebot_private_message(self):
    ...

async def keaimao_group_message(self):
    ...

```

### 第三，实现了跨平台事件，但是相对不同平台做一些不同的操作

还是群消息事件，比如，我们想收到来自 QQ 的群消息时，做这些操作；收到来自微信的消息时，做那些操作，那么，就可以将两者共有的操作放在`跨平台事件`下，再在各自的`平台独立事件`下，定义专属的逻辑

```py

async def group_message(self):
    # 收到QQ和微信的群消息时，都执行的操作

async def onebot_group_message(self):
    # 只有当收到QQ消息时，执行的操作

async def keaimao_group_message(self):
    # 只有当收到微信消息时，执行的操作

```

## 都定义了的情况

如果`平台独立事件`有对应的`跨平台事件`，而你也定义了该事件的`跨平台事件`和`平台独立事件`，那么，都会调用，先调用`跨平台事件`，再调用`平台独立事件`

还是一样的示例代码

```py

async def group_message(self):
    # 收到QQ和微信的群消息时，都执行的操作

async def onebot_group_message(self):
    # 只有当收到QQ消息时，执行的操作

async def keaimao_group_message(self):
    # 只有当收到微信消息时，执行的操作

```

当收到 QQ 消息时，先执行`group_message`，然后执行`onebot_group_message`

当收到微信消息时，先执行`group_message`,然后执行`keaimao_group_message`
