::: danger
指令系统尚未实现，这里只是展示指令系统可能的样子
:::

```py
@as_command(
    needPrefix=True,
    prefix=["/", "#", "dan "],#都是正则，自动加上^
    also=["查询", "测试"],#都是正则
    excludeClassName=False,#类名本身不作为指令
    exit=["^/exit", "^退出", "我?退出(对话)?"],#都是正则
    at=False,#是否需要at机器人
    timeout=30,# 会话超时时间，单位秒
)
class 查询装备:

    context: dict


    # 默认的initial，“开启指令“查询装备”的会话”
    async def initial(self, **messages):
        reply("开始执行指令")
        reply("请按照 /查询装备 游戏名 装备名 的格式输入")

        return self.first

    # onFormatError默认按照pattern自动组合输出 
    # 请按照 /查询装备 game character 的格式输入
    # first和之后的FormatError格式应该有点区别
    # 输入参数无效，character应为文字， 数字
    # <:face> <:image>
    # pattern间的空格，表示至少1个空白字符
    # 参数全部以关键字参数的形式传入，
    # 所以方法的参数的顺序可以随意，但是参数名称必须和pattern中的名称一致
    # 参数的类型由框架保证
    # pattern <something:123> 中的123并不是有效的python类型
    @pattern(
        # 不提供类型，默认全部str
        "<game:str> <character:str>", 
        onFormatError="请按照 /查询装备 游戏名 装备名 的格式输入"
    )
    async def first(self, **messages):
        game = messages["game"]
        reply("你选择的是{game}的{character}角色，需要查询他的什么装备呢？")

        return self.second

    # ?:表示可选
    # 进入对话指令context，此时用户不再需要输入/查询装备
    # return True继续命令执行，return False触发中断
    @pattern("<armor:str> <rarity?:int>", )
    async def second(self, **messages):
        if messages['rarity']:
            results = getData(armor, rarity)
            reply("查询到以下装备{results}")

            return None
        else:
            reply("armor有如下稀有度{1 2 3 4 5}")
            reply("你要查询的是哪一个呢？")

            return self.third

    @pattern("<rarity:int>", )
    async def third(self, **messages):
            # 可以从指令的context中获取到之前几次对话获取到的参数
        armor = self.context['second']['args']['armor']
        results = getData(armor, rarity)
        reply("查询到以下装备{results}")

        return None
        # 显式return None，或者不return，都会结束会话，触发finish生命周期

    # 用户主动退出
    @pattern("<something?:str>")
    async def exit(self, **messages):
        reply(f"收到了离开消息{messages['something']}")

    # 流程正常退出(在中间的流程return False/None也是正常退出)
    async def finish(self):
        reply("以下为对话历史")
        for order, info in self.context:
            reply("第{order}次对话")
            reply("用户输入{info["message"]}")
            reply("解析出如下参数")
            for argName, argValue in info['args']:
                reply("{argName} {argValue}")

    async def timeout(self, **messages):
        reply("用户超时未回复，结束会话")

    async def error(self, error, **messages):
        reply("执行过程中未捕获的错误")
        reply(f"{error.message}")
        reply(f"{error.trace}")
        


# 另一种定义pattern的方式
class FirstMethodPatternModel(PatternModel):
    game:Optional[str]
    character:str
    onFormatError="请按照 /查询装备 游戏名 装备名 的格式输入"

```