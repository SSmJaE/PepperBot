<h1 align="center">PepperBot</h1>

<p align="center">一个符合直觉的跨平台机器人框架，支持TG, Discord, QQ基于OneBot协议</p>

<p align="center">
<a href="https://ssmjae.github.io/PepperBot/">文档</a> · 
<a href="https://jq.qq.com/?_wv=1027&k=EPhcRRib">交流群</a>
</p>

## 特性
- 底层基于异步的Sanic框架，性能相当不错
- 轻量，主要处理消息，对于其他功能，暴露底层接口，方便实现深度定制
- api符合直觉，直观，流畅地把想法映射到代码上
- 基于python3.6之后的类型注解，提供了完全的类型提示
- 只会动态注入用到的参数，没必要每次写一长串用不到的参数了！
- 支持集中化路由、装饰器式路由

## 安装
```bash
pip install pepperbot
```
## 食用
- [Go to wiki](https://github.com/SSmJaE/PepperBot/wiki)
- [Go to Docs](https://ssmjae.github.io/PepperBot/)

## 示例
只需要非常少的代码，就可以实现群消息的响应
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

指令系统，用户消息可以自动解析为pydantic的model

支持str, int, float, bool

支持所有有效CQ码，如Face, Image, Video, Poke等等
```py
class TestComplexText(BaseModel):
    游戏名: str
    装备数: int
    加强: bool
    价格: float
    表情: Face
    另一个字符: str

    class Config:
        arbitrary_types_allowed = True

    @validator("装备数")
    def check_装备数(cls, value):
        if value not in [11, 12, 13]:
            raise PatternFormotError("请输入有效序号")
```