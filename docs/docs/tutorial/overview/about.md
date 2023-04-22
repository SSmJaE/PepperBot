---
title: 关于
---

## 为什么叫 PepperBot？

我喜欢吃农家小炒肉(辣椒炒肉)

## 命名约定

基于`类(class)`的handler，也被称为`class_handler`

同样，指令也是基于`类`的，所以也被称为`class_command`

对于`class`上的`method(方法)`，如果是`class_handler`，有时也被称为`event_handler`，比如`group_message`这个`method`

如果是`class_command`的method，直接就是`method(方法)`

### 什么是协议端(后端backend)

PepperBot 本身并没有实现与 QQ、微信、TG 等平台通信的能力，只负责处理“业务逻辑”

PepperBot 通过与协议端的通信，实现了与平台的通信

能够模拟 QQ、微信等客户端的行为，实现了与 QQ、微信等平台的直接通信(接收并发送 QQ 消息)的能力，被称为“协议端”或者“后端”

## 常见异常

### InitializationError

在运行机器人之前，`PepperBot`会通过AST对代码进行检查

如果代码写的有问题，就会抛出这个异常

### EventHandleError

机器人运行后，事件响应过程中，出现了问题，会抛出这个异常

### BackendApiError

机器人运行后，调用后端的API过程中，出现了问题，会抛出这个异常
