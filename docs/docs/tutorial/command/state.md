---
title: 指令的状态
---


## `PepperBot`中，指令的状态是指什么

对于一个交互式的，有多轮对话的指令来说，状态 == 指令执行到哪一步了

常见的机器人框架中，如果有交互式的指令，指令的执行顺序，往往都只是单向的、顺序执行

`PepperBot`基于`class`，可以随意指定指令的执行顺序(顺序、回滚、循环)，通过`method`的返回值，即可轻松实现

## 如何设置下一步要执行的`method`

返回下一次用户发送消息时，想要执行的`method_name`即可

注意，该`method`，必须在当前class中定义了

```py
def outside_function():
    ...

class TestCommand:
    def initial():
        ...
        return self.inner_method

    def inner_method():
        ...
```

:::warning
注意，返回函数对象

```py
return self.method_name
```

而不是返回函数调用

```py
return self.method_call()
```

:::

### 顺序执行

```py
class TestCommand(Command):
    def initial():
        ...
        return self.second

    def second():
        ...
        return self.third

    def third():
        ...
        return self.whether_continue

```

一般来说，我们组织代码的顺序，和实际的执行顺序是一致的

### 回滚

不但可以向下跳转，还可以向上跳转

```py
class TestCommand:
    ...

    def whether_continue():
        if "继续" in chain:
            return self.initial
        else:
            return None

```

### 循环

```py
class TestCommand:
    def initial():
        ...
        return self.initial
```

返回当前`method`自身，即可实现循环

这样，只有

- 用户主动退出
- 指令超时
- `method`执行出错

才会退出当前的指令执行

## 如何退出会话

如果没有 return 语句，或者 return None，那么，会触发 finish [生命周期](./lifecycle.md)

```py
class TestCommand(Command):
    def method():
        ...
        # no return

    def method():
        return
        # implicit return None隐式返回None

    def method():
        return None

    async def finish(self):
        ...
```
