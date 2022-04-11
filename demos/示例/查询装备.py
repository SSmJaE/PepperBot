from typing import Deque

from pepperbot.core.message.chain import MessageChain
from pepperbot.core.message.segment import Text
from pepperbot.extensions.command import PatternArg, as_command
from pepperbot.extensions.command.handle import CommandSender
from pepperbot.store.command import HistoryItem


@as_command(
    need_prefix=True,
    prefixes=["/", "#", "dan "],  # 都是正则，自动加上^
    aliases=["查询", "测试"],  # 都是正则
    include_class_name=True,  # 类名本身不作为指令
    exit_patterns=["^/exit", "^退出", "我?退出(对话)?"],  # 都是正则
    require_at=False,  # 是否需要at机器人
    timeout=30,  # 会话超时时间，单位秒
)
class 查询装备:

    # 默认的initial，“开启指令“查询装备”的会话”
    async def initial(self, sender: CommandSender):
        await sender.send_message(
            Text("开始执行指令\n"),
            Text("请按照 游戏名 人物序号 的格式输入\n"),
        )

        return self.choose_game

    async def choose_game(
        self, sender: CommandSender, game: str = PatternArg(), npc: int = PatternArg()
    ):
        await sender.send_message(Text(f"你选择的是 {game} 的 {npc}，需要查询他的什么装备呢？稀有度为何？"))

        return self.choose_kind

    async def choose_kind(
        self,
        sender: CommandSender,
        kind: str = PatternArg(),
        rarity: int = PatternArg(),
    ):
        results = [
            "大剑",
            "操虫棍",
            "双手剑",
            "太刀",
        ]

        await sender.send_message(
            Text(f"查询到以下装备\n"),
            *[Text(f"- {result}\n") for result in results],
            Text("\n是否继续查询？回复“继续”以继续"),
        )

        return self.whether_continue

    async def whether_continue(self, chain: MessageChain):
        if "继续" in chain:
            return self.choose_game

        else:
            # 显式return None，或者不return，都会结束会话，触发finish生命周期
            return None

    # 用户主动退出
    async def exit(self, sender: CommandSender):
        await sender.send_message(Text(f"用户主动退出"))

    # 流程正常退出(在中间的流程return False/None也是正常退出)
    async def finish(self, sender: CommandSender, history: Deque[HistoryItem]):
        string = ""

        for index, item in enumerate(history, start=1):
            string += "----------\n"
            string += f"第{index}次对话\n"
            string += f"用户输入 : {item.chain.pure_text}\n"
            string += "解析出如下参数\n"

            # for argName, argValue in item.pattern:
            #     reply("{argName} {argValue}")

        await sender.send_message(Text("指令自然退出，历史成功消息如下\n"), Text(string))

    async def timeout(self, sender: CommandSender):
        await sender.send_message(Text("用户超时未回复，结束会话"))

    async def catch(self, exception: Exception, sender: CommandSender):
        await sender.send_message(
            Text("执行过程中未捕获的错误\n"),
            Text(f"{exception}"),
        )
