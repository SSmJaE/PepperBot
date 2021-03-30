<h1 align="center">PepperBot</h1>

<p align="center">A lightweight QQ bot logic framework, for human</p>

<p align="center">
<a href="https://ssmjae.github.io/PepperBot/">文档</a>
</p>

## Features
- based on OneBot protocol
- 渐进式
- 符合直觉，直观，流畅的把想法映射到代码上
- 新手友好，类型提示
- 易扩展
- 基于class mixin的扩展
- 使用原生import，而不是自己造一套模块轮子
- 注入参数，无限overload
- 异步，反向ws，性能
- 支持集中化路由管理

## 示例
```py
# 注册群事件
@register(groupId=123456789)
class WhateverNameYouWant:
    """class名称可以随意设置"""

    # 如方法名add_group所示，这是加群请求的事件响应
    async def add_group(self, bot: GroupRequestBot, comment: str, **kwargs):
        if "加入我" in comment:
            await bot.resolve() # 接受
        else:
            await bot.reject() # 拒绝

    # 事件也有生命周期，before，after，可以进行拦截等操作
    async def before_group_message(**kwargs):
        pass

    # 群聊消息的事件响应
    # 所有参数都有完善的类型提示，不需要记忆，以PascalCase的方法名加上参数名即可
    # 如GroupMessageBot=group_message + bot
    async def group_message(self, bot: GroupMessageBot, chain: MessageChain, sender: Sender, **kwargs):
        # chain即为消息链，pure_text是消息中的纯文本，不包含表情、图片等
        if "撤回我" == chain.pure_text:
            await chain.withdraw() # 可以直接“撤回消息”，符合直觉

        if "踢出我" == chain.pure_text:
            await sender.kickout() # 可以直接踢出发言群员

        # 也可以对消息链进行in操作，相当于in chain.pure_text
        if "禁言我" in chain:
            await sender.ban(10) # 可以直接禁言发言群员

        # 与上一条语句等价，判断消息链中，是否包含文本消息"禁言我"
        if Text("禁言我") in chain:
            pass

        # 可以直接判断消息链中是否包含表情，并不指定是哪一个表情
        if Face in chain:
            pass

        # 指定了是“笑脸”表情，判断消息链中是否包含笑脸
        if Face(100) in chain:
            pass

        # 一个快捷操作，返回表情存在与否，与最后一个表情
        # 也可以指定具体的表情是否存在，has_and_last(Face(100))
        hasFace, face = chain.has_and_last(Face) 
        if hasFace:
            await bot.group_msg(face)

        # 获取消息链中的所有表情
        faces = chain.faces

        # 支持切片操作
        firstFace = faces[0]

        # 也支持其它消息片段
        images = chain.images
        images[1:3]

        # 可以直接对chain进行正则操作，不用手动使用re库
        if chain.regex("请?禁言我?"):
            await sender.ban(10)

        if chain.regex("有人(在|吗|嘛|在吗).?"):
            # 发送一条群消息
            # 接受任意个参数，必须是合法的消息片段，比如Text，Face，Image
            await bot.group_msg( 
                Text("没人"),
                Face(150)
            )

        # 对于多条件判断，提供了any，每一个参数都是一个正则
        if chain.any("能", "可以") and chain.any("考试", "测试"):
            # 引用回复
            await chain.reply( 
                Text("支持班级测试，不过题目收录不完整\n"),
                Text("为什么不自己试一试呢？"),
                Face(100)
            )
```