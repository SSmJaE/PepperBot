<h1 align="center">PepperBot</h1>

<p align="center">
<img  src="./archive/icon.png" width="200" />
</p>

<p align="center">一个符合直觉的跨社交平台机器人框架，轻松地在平台间传递消息，支持QQ、微信、Telegram</p>
<p align="center">
<a href="https://ssmjae.github.io/PepperBot/">文档</a> ·
<a href="https://jq.qq.com/?_wv=1027&k=EPhcRRib">QQ交流群</a>  
</p>

<p align="center">
<img src="./archive/coverage-badge.svg" />
</p>

## 生而跨平台

- QQ 基于 `Onebot`，`Mirai`(待实现)、`OPQ`(待实现)
- 微信基于`可爱猫`
- Telegram基于`Pyrogram`
- 提供了跨平台、易用的消息类型(片段)
- 通用事件，比如群消息、私聊消息等，提供了统一的接口，只需要写一次代码，就可以无缝应用到各个平台上，跨平台的消息传递从未如此轻松随意
- 可以跨群、跨平台共享指令(的状态)，或者全局锁定用户(不管用户是通过群聊还是私聊)

## 性能也够用

- 底层基于异步的 Sanic 框架，目前有一定生态的 python web 框架中，[性能最好的](https://www.techempower.com/benchmarks/)
- 轻量，主要处理消息，对于其他功能，暴露底层接口，方便实现深度定制
- 几行代码，即可实现**多进程负载均衡**

## 自带全家桶

- 支持 `Django`或`starlette` 风格的集中化路由，或者`flask`或`fastAPI` 风格的装饰器式路由
- 非常灵活的权限系统，支持路由、class、method级别的权限控制
- Django 类视图风格或Vue 生命周期风格的**指令系统**
- 定时任务
- 日志支持
- 基于`ormar`的异步数据库支持(ormar基于`sqlalchemy` + `pydantic`)
- 自带插件市场，可以安装社区指令
- [ ] 提供cli工具，快速创建项目
- [ ] 类似`Selenium`的事件等待
- [ ] `fastAPI`风格的**依赖注入**

## 接口合语义

- API 符合直觉，直观，流畅地把想法映射到代码上
- 基于 python3.6 之后的类型注解，提供了完全的类型提示
- 大部分可以自动获取的参数，都会自动获取，不需要每次手动提供了
- 只会动态注入用到的参数，没必要每次写一长串用不到的参数了！
- 文档中，均有可直接复制使用的代码片段，快速开发

## 测试文档全

- 通过元编程(AST 之类)手段，对编写的各种代码进行规则检查，并输出易于理解的错误信息，将问题消灭在框架启动之前
- 文档比较全
- 测试覆盖比较全面
- 大量官方示例/指令
- 来自作者的 QA(加群以获取)

## 安装

目前只能3.10及以上，因为用了点新特性，之后会恢复对3.8的支持

```bash
pip install pepperbot
```

## 使用

[具体使用见文档](https://ssmjae.github.io/PepperBot/)

## 示例

六行代码实现消息互转

```py
class WhateverNameYouWant:
    async def group_message(self, bot: UniversalGroupBot, chain: MessageChain):
        if bot.onebot: # 转发qq消息至微信、TG
            await bot.arbitrary.keaimao.group_message("19521241254@chatroom", *chain.segments)
            await bot.arbitrary.telegram.group_message("bot_father", *chain.segments)

        if bot.keaimao: # 转发微信消息至qq、TG
            await bot.arbitrary.onebot.group_message("1041902989", *chain.segments)
            await bot.arbitrary.telegram.group_message("bot_father", *chain.segments)
```

只需要非常少的代码，就可以实现**跨平台**的群消息的响应

```py
@register()
class WhateverNameYouWant:

    # 注册跨平台群事件
    async def group_message(self, bot: GroupBot, chain: MessageChain, sender: Sender):
        # chain即为消息链，pure_text是消息中的纯文本，不包含表情、图片等
        if "撤回我" == chain.pure_text:
            await chain.withdraw() # 可以直接“撤回消息”，符合直觉

        if "踢出我" == chain.pure_text:
            await sender.kickout() # 可以直接踢出发言群员

        # 也可以对消息链进行in操作，相当于in chain.pure_text
        if "禁言我" in chain:
            await sender.ban(10) # 可以直接禁言发言群员

        if chain.regex("有人(在|吗|嘛|在吗).?"):
            # 发送一条群消息
            # 接受任意个参数，必须是合法的消息片段，比如Text，Face，Image
            await bot.group_message(
                Text("没人"),
                Image("http://123.jpg"),
            )
```

## 生态

### 可以记忆上下文的GPT群聊机器人

[PepperBot-GPT]( )

### 通过GPT，自动检测群聊中的广告信息
