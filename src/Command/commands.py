from src.Command import *


@as_command(
    needPrefix=True,
    prefix=["/", "#", "dan "],  # 都是正则，自动加上^
    also=["查询", "测试"],  # 都是正则
    includeClassName=False,  # 类名本身不作为指令
    exitPattern=["^/exit", "^退出", "我?退出(对话)?"],  # 都是正则
    at=False,  # 是否需要at机器人
    timeout=None,  # 会话超时时间，单位秒
)
class 查询装备:

    # todo context注入
    # 全局context，应该是实时同步的
    context: dict

    # 默认的initial，“开启指令“查询装备”的会话”
    async def initial(
        self, bot: GroupMessageBot, chain: MessageChain, sender: Sender, **kwargs
    ):
        await bot.group_msg(Text(f"{sender.user_id}"))
        await bot.group_msg(Text("开始执行指令"))
        # await bot.group_msg(Text("请按照 /查询装备 游戏名 装备名 的格式输入"))

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
        # todo 类似pydantic，具体指出哪个参数出错
        onFormatError="请按照 /查询装备 游戏名 装备名 的格式输入",
    )
    async def first(
        self,
        bot: GroupMessageBot,
        chain: MessageChain,
        sender: Sender,
        context: Dict,
        **kwargs,
    ):
        # game = messages["game"]
        # reply("你选择的是{game}的{character}角色，需要查询他的什么装备呢？")
        await bot.group_msg(Text(f"{sender.user_id}"))
        await bot.group_msg(Text("第一个响应"))
        number = random.random()
        await bot.group_msg(Text(f"向context注入{number}"))
        context["test"] = number

        return self.second

    # ?:表示可选
    # 进入对话指令context，此时用户不再需要输入/查询装备
    # return True继续命令执行，return False触发中断
    @pattern(
        "<armor:str> <rarity?:int>",
    )
    async def second(
        self,
        bot: GroupMessageBot,
        chain: MessageChain,
        sender: Sender,
        context: Dict,
        **kwargs,
    ):
        # if messages['rarity']:
        #     results = getData(armor, rarity)
        #     reply("查询到以下装备{results}")

        #     return None
        # else:
        #     reply("armor有如下稀有度{1 2 3 4 5}")
        #     reply("你要查询的是哪一个呢？")

        #     return self.third
        await bot.group_msg(Text(f"{sender.user_id}"))
        await bot.group_msg(Text("第二个响应"))
        await bot.group_msg(Text(f"从context中获取到{context['test']}"))

        debug(context)

    # @pattern("<rarity:int>", )
    # async def third( self, bot:GroupMessageBot,chain:MessageChain,sender:Sender,**kwargs):
    #         # 可以从指令的context中获取到之前几次对话获取到的参数
    #     armor = self.context['second']['args']['armor']
    #     results = getData(armor, rarity)
    #     reply("查询到以下装备{results}")

    #     return None
    #     # 显式return None，或者不return，都会结束会话，触发finish生命周期

    # 用户主动退出
    @pattern("<something?:str>")
    async def exit(
        self, bot: GroupMessageBot, chain: MessageChain, sender: Sender, **kwargs
    ):
        await bot.group_msg(Text("用户主动退出"))

    # 流程正常退出(在中间的流程return False/None也是正常退出)
    async def finish(
        self, bot: GroupMessageBot, chain: MessageChain, sender: Sender, **kwargs
    ):
        await bot.group_msg(Text(f"{sender.user_id}"))
        await bot.group_msg(Text("命令正常执行完毕后退出"))

        # reply("以下为对话历史")
        # for order, info in self.context:
        #     reply("第{order}次对话")
        #     reply("用户输入{info["message"]}")
        #     reply("解析出如下参数")
        #     for argName, argValue in info['args']:
        #         reply("{argName} {argValue}")

    async def timeout(
        self, bot: GroupMessageBot, chain: MessageChain, sender: Sender, **kwargs
    ):
        await bot.group_msg(Text("用户超时未回复，结束会话"))

    # async def error(self, error, **messages):
    #     reply("执行过程中未捕获的错误")
    #     reply(f"{error.message}")
    #     reply(f"{error.trace}")


@as_command(
    needPrefix=False,
    prefix=[],
    also=[],
    includeClassName=True,
    exitPattern=["我?退出(对话)?"],
    at=False,
    timeout=30,
)
class 模拟:

    # todo context注入
    # 全局context，应该是实时同步的
    context: dict

    # 默认的initial，“开启指令“查询装备”的会话”
    async def initial(
        self, bot: GroupMessageBot, chain: MessageChain, sender: Sender, **kwargs
    ):
        await bot.group_msg()
        await bot.group_msg(
            Text(f"{sender.user_id}"), Text("开始执行指令"), Text("请按照 游戏名 装备名 的格式输入")
        )

        return self.first

    @pattern(
        # 不提供类型，默认全部str
        "<game:str> <character:str>",
        onFormatError="请按照 /查询装备 游戏名 装备名 的格式输入",
    )
    async def first(
        self, bot: GroupMessageBot, chain: MessageChain, sender: Sender, **kwargs
    ):
        # game = messages["game"]
        # reply("你选择的是{game}的{character}角色，需要查询他的什么装备呢？")

        try:
            # 参数过多需要报错吗？还是省略就好了——省略
            # todo 友好的定义pattern的方式
            # todo 支持表情，图片等等，而不仅是文字
            match = re.search(r".*?(\S*)\s*(\S*)", chain.pure_text)
            if not match or not len(match.groups()) == 2:

                raise Exception()

            for part in match.groups():
                if not part:
                    raise Exception()

            debug(match.groups())
            await bot.group_msg(
                Text(f"成功解析参数 游戏名{match.groups()[0]} 装备名{match.groups()[1]}")
            )

        except:
            await bot.group_msg(Text("请按照 /查询装备 游戏名 装备名 的格式输入"))
            # todo 参数不够(需要哪几个，什么类型，只提供了什么)，
            # todo 参数类型错误(哪个参数类型错误)，
            # todo 友好的提示信息

            return self.first

        # return self.second

    # ?:表示可选
    # 进入对话指令context，此时用户不再需要输入/查询装备
    # return True继续命令执行，return False触发中断
    @pattern(
        "<armor:str> <rarity?:int>",
    )
    async def second(
        self, bot: GroupMessageBot, chain: MessageChain, sender: Sender, **kwargs
    ):
        # if messages['rarity']:
        #     results = getData(armor, rarity)
        #     reply("查询到以下装备{results}")

        #     return None
        # else:
        #     reply("armor有如下稀有度{1 2 3 4 5}")
        #     reply("你要查询的是哪一个呢？")

        #     return self.third
        await bot.group_msg(Text(f"{sender.user_id}"))
        await bot.group_msg(Text("第二个响应"))

    # @pattern("<rarity:int>", )
    # async def third( self, bot:GroupMessageBot,chain:MessageChain,sender:Sender,**kwargs):
    #         # 可以从指令的context中获取到之前几次对话获取到的参数
    #     armor = self.context['second']['args']['armor']
    #     results = getData(armor, rarity)
    #     reply("查询到以下装备{results}")

    #     return None
    #     # 显式return None，或者不return，都会结束会话，触发finish生命周期

    # 用户主动退出
    @pattern("<something?:str>")
    async def exit(
        self, bot: GroupMessageBot, chain: MessageChain, sender: Sender, **kwargs
    ):
        await bot.group_msg(Text("用户主动退出"))

    # 流程正常退出(在中间的流程return False/None也是正常退出)
    async def finish(
        self, bot: GroupMessageBot, chain: MessageChain, sender: Sender, **kwargs
    ):
        await bot.group_msg(Text(f"{sender.user_id}"))
        await bot.group_msg(Text("命令正常执行完毕后退出"))

        # reply("以下为对话历史")
        # for order, info in self.context:
        #     reply("第{order}次对话")
        #     reply("用户输入{info["message"]}")
        #     reply("解析出如下参数")
        #     for argName, argValue in info['args']:
        #         reply("{argName} {argValue}")

    async def timeout(
        self, bot: GroupMessageBot, chain: MessageChain, sender: Sender, **kwargs
    ):
        await bot.group_msg(Text("用户超时未回复，结束会话"))


@as_command(
    needPrefix=False,
    prefix=[],
    also=[],
    includeClassName=True,
    exitPattern=["我?退出(对话)?"],
    at=False,
    timeout=30,
)
class 简单复读(CommonEndMixin):

    # 默认的initial，“开启指令“查询装备”的会话”
    async def initial(
        self,
        bot: GroupMessageBot,
        chain: MessageChain,
        sender: Sender,
        context: Dict,
        **kwargs,
    ):
        await bot.group_msg(Text(f"{sender.user_id}"), Text("开始执行复读"))

        context["maxTime"] = 3
        context["currentTime"] = 0

        return self.first

    @pattern(
        # 不提供类型，默认全部str
        "<game:str> <character:str>",
        onFormatError="请按照 /查询装备 游戏名 装备名 的格式输入",
    )
    async def first(
        self,
        bot: GroupMessageBot,
        chain: MessageChain,
        sender: Sender,
        context: Dict,
        messageQueue: List[UserMessage],
        **kwargs,
    ):

        context["currentTime"] = context["currentTime"] + 1
        await bot.group_msg(*chain.chain)
        await bot.group_msg(Text(f"已复读{context['currentTime']}次"))

        buffer = []
        for message in messageQueue:
            buffer.append(Text(f"来自群 {message.groupId: <12} "))
            buffer.append(Text(f"用户 {message.userId: <12} "))
            buffer.extend(message.message)
            buffer.append(Text("\n"))

        await bot.group_msg(Text(f"历史消息\n"), *buffer)

        if context["currentTime"] >= context["maxTime"]:
            return True
        else:
            return self.first

        # return self.second


@as_command(
    needPrefix=False,
    prefix=[],
    also=[],
    includeClassName=True,
    exitPattern=["我?退出(对话)?"],
    at=False,
    timeout=30,
    mode="crossGroup",
)
class 跨群复读(CommonEndMixin):
    async def initial(
        self,
        bot: GroupMessageBot,
        chain: MessageChain,
        sender: Sender,
        context: Dict,
        messageQueue: List[UserMessage],
        **kwargs,
    ):
        await bot.group_msg(Text(f"{sender.user_id}"), Text("开始执行跨群复读，跨群，不跨用户"))

        context["maxTime"] = 3
        context["currentTime"] = 0

        return self.first

    async def first(
        self,
        bot: GroupMessageBot,
        chain: MessageChain,
        sender: Sender,
        context: Dict,
        messageQueue: List[UserMessage],
        **kwargs,
    ):

        context["currentTime"] = context["currentTime"] + 1
        await bot.group_msg(*chain.chain)
        await bot.group_msg(Text(f"已复读{context['currentTime']}次"))

        buffer = []
        for message in messageQueue:
            buffer.append(Text(f"来自群 {message.groupId: <12} "))
            buffer.append(Text(f"用户 {message.userId: <12} "))
            buffer.extend(message.message)
            buffer.append(Text("\n"))

        await bot.group_msg(Text(f"历史消息\n"), *buffer)

        if context["currentTime"] >= context["maxTime"]:
            return True
        else:
            return self.first


@as_command(
    needPrefix=False,
    prefix=[],
    also=[],
    includeClassName=True,
    exitPattern=["我?退出(对话)?"],
    at=False,
    timeout=30,
    mode="crossUser",
)
class 跨用户复读(CommonEndMixin):
    async def initial(
        self,
        bot: GroupMessageBot,
        chain: MessageChain,
        sender: Sender,
        context: Dict,
        messageQueue: List[UserMessage],
        **kwargs,
    ):
        await bot.group_msg(Text(f"{sender.user_id}"), Text("开始执行跨用户复读，不跨群，跨用户"))

        context["maxTime"] = 3
        context["currentTime"] = 0

        return self.first

    async def first(
        self,
        bot: GroupMessageBot,
        chain: MessageChain,
        sender: Sender,
        context: Dict,
        messageQueue: List[UserMessage],
        **kwargs,
    ):

        context["currentTime"] = context["currentTime"] + 1
        await bot.group_msg(*chain.chain)
        await bot.group_msg(Text(f"已复读{context['currentTime']}次"))

        buffer = []
        for message in messageQueue:
            buffer.append(Text(f"来自群 {message.groupId: <12} "))
            buffer.append(Text(f"用户 {message.userId: <12} "))
            buffer.extend(message.message)
            buffer.append(Text("\n"))

        await bot.group_msg(Text(f"历史消息\n"), *buffer)

        if context["currentTime"] >= context["maxTime"]:
            return True
        else:
            return self.first


@as_command(
    needPrefix=False,
    prefix=[],
    also=[],
    includeClassName=True,
    exitPattern=["我?退出(对话)?"],
    at=False,
    timeout=30,
    mode="global",
)
class 全局复读(CommonEndMixin):
    async def initial(
        self,
        bot: GroupMessageBot,
        chain: MessageChain,
        sender: Sender,
        context: Dict,
        messageQueue: List[UserMessage],
        **kwargs,
    ):
        await bot.group_msg(Text(f"{sender.user_id}"), Text("开始执行全局复读，即跨群，也跨用户"))

        context["maxTime"] = 3
        context["currentTime"] = 0

        return self.first

    async def first(
        self,
        bot: GroupMessageBot,
        chain: MessageChain,
        sender: Sender,
        context: Dict,
        messageQueue: List[UserMessage],
        **kwargs,
    ):

        context["currentTime"] = context["currentTime"] + 1
        await bot.group_msg(*chain.chain)
        await bot.group_msg(Text(f"已复读{context['currentTime']}次"))

        buffer = []
        for message in messageQueue:
            buffer.append(Text(f"来自群 {message.groupId: <12} "))
            buffer.append(Text(f"用户 {message.userId: <12} "))
            buffer.extend(message.message)
            buffer.append(Text("\n"))

        await bot.group_msg(Text(f"历史消息\n"), *buffer)

        if context["currentTime"] >= context["maxTime"]:
            return True
        else:
            return self.first


@as_command(
    needPrefix=True,
    prefix=["/"],
    also=[],
    includeClassName=True,
    exitPattern=["我?退出(对话)?"],
    at=False,
    timeout=30,
    mode="normal",
)
class 查询天气(CommonEndMixin):
    async def initial(
        self,
        bot: GroupMessageBot,
        chain: MessageChain,
        sender: Sender,
        context: Dict,
        messageQueue: List[UserMessage],
        **kwargs,
    ):
        try:
            match = re.search(r".*?(\S*)", chain.pure_text)
            if not match or not len(match.groups()) >= 1:

                raise Exception()

            for part in match.groups():
                if not part:
                    raise Exception()

            debug(match.groups())

            await bot.group_msg(Text(f"成功解析参数 城市{match.groups()[0]}"))

        except:
            await bot.group_msg(Text("请按照 /查询装备 城市 的格式输入"))

        return self.initial


@as_command(
    needPrefix=False,
    also=[""],
    includeClassName=True,
    exitPattern=["我?退出(对话)?"],
    at=True,
    timeout=30,
    mode="normal",
)
class 人工智障(CommonEndMixin):
    async def initial(
        self,
        bot: GroupMessageBot,
        chain: MessageChain,
        sender: Sender,
        context: Dict,
        messageQueue: List[UserMessage],
        **kwargs,
    ):

        await bot.group_msg(Text("从接口获得的回复"))
        return self.initial
