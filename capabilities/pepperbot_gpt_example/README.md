
<h1 align="center">PepperBot GPT Example</h1>

<p align="center">
一个基于PepperBot，可以保留上下文的ChatGPT群聊机器人实现
</p>

## 如何使用？

先保证你能正常的运行起来PepperBot + go-cqhttp，具体见PepperBot的文档

然后，通过包管理器安装本项目

```bash
pip install pepperbot-gpt-example
```

或者

```bash
pdm add pepperbot-gpt-example
```

在你的入口文件中，添加如下代码

```python

from pepperbot.extensions.command import as_command

from pepperbot_gpt_example import GPTExample, GPTExampleConfig


async def query_gpt(messages:list[str]):
    """ 自己实现调用GPT API的方法 """
    return completion

my_gpt_command = as_command(
    need_prefix=True,
    prefixes=["/"],
    aliases=["gpt"],
    include_class_name=False,
    exit_patterns=["我?退出(对话)?"],
    require_at=False,
    timeout=120,
    config=GPTExampleConfig(
        # 直接提供token + proxy_token，或者自己实现proxy_call，二选一
        proxy_call=query_gpt,
    )
)(GPTExample)


bot.apply_routes(
    [
        BotRoute(
            commands=[my_gpt_command],
            groups={
                "onebot": [
                    "893609211",  
                    "819441084",
                ]
            },
        ),
    ]
)
```

如果通过token的方式，需要在`根目录`新建一个`.env`文件，内容如下

也可以直接通过环境变量设置

```env
gpt_example_super_users=["qq123", "234792"]
gpt_example_super_groups=["123123"]
gpt_example_times_per_group={"12341234":10}
gpt_example_token="your_openai_token", 
gpt_example_proxy_token="your_proxy_token", 
```

proxy_token是为了避免代理被滥用，需要是PepperBot群员才能调用
