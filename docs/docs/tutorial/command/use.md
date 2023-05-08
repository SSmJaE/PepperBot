---
title: 使用指令
---



## 在`BotRoute`中注册

和`事件响应`中的`handler`一样，我们也需要将`指令`，通过`BotRoute`注册之后，才能跑起来

配置和`handler`类似

```py
@as_command()
class MyCommand:
    pass

bot.apply_routes([
    BotRoute(
        friends=None,
        groups={
            "onebot": ["123456"]
        },
        handlers=[],
        commands = [MyCommand],
    )
])
```

## 通过装饰器形式定义指令

```py
@as_command()
class MyCommand:
    pass
```

## 手动“调用”装饰器，将同一个`class`注册为多个指令

当我们从社区获取指令时，有时，指令的作者并没有对指令应用as_command，而是将这一步讲给了我们来实现

这样，我们就能通过配置`as_command`的参数，来实现不同的效果

我们已经可以获取到指令的`class`，但是似乎没有办法在这个`class`上使用装饰器了，因为这个`class`定义好了

这时候，我们就可以手动调用`as_command`，来将这个`class`注册为指令

因为`as_command`装饰器的本质，就是一个函数，这个函数，会返回第二个函数，这个第二个函数，接受一个`class`，将其注册为指令

所以

```py
@as_command()
class MyCommand:
    pass
```

等价于

```py
as_command()(MyCommand)
```

因为我们之后要将注册完成的`class`，再应用到`BotRoute`中，所以，我们可以将这个`class`，赋值给一个变量

```py
my_command = as_command()(MyCommand)

bot.apply_routes([
    BotRoute(
        friends=None,
        groups={
            "onebot": ["123456"]
        },
        handlers=[],
        commands = [my_command],
    )
])
```
