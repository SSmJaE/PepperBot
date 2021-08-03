<h1 align="center">PepperBot</h1>

<p align="center">一个符合直觉的跨平台机器人框架，支持TG, Discord, QQ基于OneBot协议</p>

<p align="center">
<a href="https://ssmjae.github.io/PepperBot/">文档</a> · 
<a href="https://jq.qq.com/?_wv=1027&k=EPhcRRib">交流群</a>
</p>

## 特性
- QQ部分基于OneBot协议
- 渐进式
- 新手友好，完全的类型提示
- 符合直觉，直观，流畅的把想法映射到代码上
- 易扩展，基于class mixin的扩展
- 使用原生import，而不是自己造一套模块轮子
- 注入参数，无限overload
- 异步，反向ws，性能
- 支持集中化路由管理

## 安装
```bash
pip install pepperbot
```
## 食用
 [Go to wiki](https://github.com/SSmJaE/PepperBot/wiki)

 [Go to Docs](https://ssmjae.github.io/PepperBot/)

## 示例
```py
# 注册群事件
@register(groupId=819441084)
class WhateverNameYouWant:
    
    async def group_message(self, bot: GroupCommonBot, chain: MessageChain, sender: Sender):
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
            await bot.group_msg( 
                Text("没人"),
                Face(150)
            )
```
