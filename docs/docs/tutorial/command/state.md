---
title: 指令的状态
---






## 更新指令状态(回滚)

我们定义了几个阶段，首先， 选择游戏，其次，选择装备，那么，怎么将这两个`方法`链接起来呢？

```py
def choose_game():
    ...
    return self.choose_kind

def choose_kind():
    ...
    return self.whether_continue
```

通过`方法`的返回值，返回下一步要执行的函数

```py

def choose_game():
    return self.choose_kind

```

:::warning
注意，返回函数对象

```py
return self.function_name
```

而不是返回函数调用

```py
return self.function_call()
```

:::

不但可以向下跳转，还可以向上跳转

在该示例中，我们实现了继续查询，跳转回上一步

```py
def whether_continue():
    if "继续" in chain:
        return self.choose_game

```

如果没有 return 语句，或者 return None，那么，会触发 finish 钩子

```py
def func():
    ...
    # no return

def func():
    return
    # implicit return None隐式返回None

def func():
    return None

def func():
    return self.finish
```

这四种都等价
自然退出
