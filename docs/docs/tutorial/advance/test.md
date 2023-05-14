---
title: 测试
---


得益于PepperBot精简的架构设计(event => route => handler => api)，测试业务逻辑非常轻松，甚至不需要提供专门的测试框架

详细的测试方式，可以参考`PepperBot`的测试代码(仓库根目录`tests`文件夹)，这里只是介绍一下实现思路

## 注册路由

路由正常注册即可

## 模拟事件

因为`PepperBot`本身就是一个事件驱动的框架，所以我们可以直接模拟事件，来测试业务逻辑是否正常执行

`PepperBot`处理事件的最上层抽象，是`handle_event`函数，所以我们可以直接调用这个函数，来模拟事件

```py
from pepperbot.core.event.handle import handle_event

await handle_event(
    "onebot",
    {
        "time": 1651692010,
        "self_id": 123456789,
        "post_type": "message",
        "message_type": "group",
        "sub_type": "normal",
        "message_id": 1234,
        "user_id": 987654321,
        "message": message,
        "raw_message": "Hello, World!",
        "font": 123,
        ...
        "group_id": 1041902989,
    }
)
```

## 获取API调用结果

一般来说，我们想要知道业务逻辑是否正常执行，只需要检测对应的API是否被调用即可

这里用QQ举例，`PepperBot`中，向`go-cqhttp`发送消息的最底层API是`to_onebot`，所以我们这里直接mock即可

```py
api_results = []


def new_caller(self, action: str, kwargs: dict[str, Any]):
    if action == "get_login_info":
        return {"user_id": "123456789", "nickname": "测试机器人"}

    else:
        api_results.append((action, kwargs))


@pytest.fixture(scope="class")
def patch_api_caller():
    with patch(
        "pepperbot.core.api.api_caller.ApiCaller.to_onebot",
        new=new_caller,
    ) as patched:
        yield patched
```

我们将调用情况，收录到`api_results`中，然后在测试用例中，断言`api_results`是否符合预期即可

比如，我先注册一个`command`，如果满足一定条件，就发送`hello world`，那么，我就可以这样判断

```py
bot = PepperBot()

bot.register_adapter(
    bot_protocol="onebot",
    receive_protocol="http",
    backend_protocol="http",
    backend_host="127.0.0.1",
    backend_port=5700,
)

@as_command(
    need_prefix=True,
    prefixes=["/"],
    aliases=["command"],
)
class TestCommand:
    async def initial(self, sender: CommandSender):
        await sender.send("Hello, World!")


bot.apply_routes(
    [
        BotRoute(
            commands=[TestCommand],
            groups="*",
        )
    ]
)

# 不需要run，我们直接调用handle_event来模拟事件
await handle_event(
    "onebot",
    {
        "time": 1651692010,
        "self_id": 123456789,
        "post_type": "message",
        "message_type": "group",
        "sub_type": "normal",
        "message_id": 1234,
        "user_id": 987654321,
        "message": message,
        "raw_message": "/command",
        "font": 123,
        ...
        "group_id": 1041902989,
    }
)

# 这里不一定和实际的参数一致，理解思路即可
assert api_results == [
    ("send_group_msg", {"message": "Hello, World!", "group_id": 1041902989}) 
]
```
