from textwrap import dedent
import inspect

from pydantic import validator

from pepperbot.command import as_command, pattern, with_command
from pepperbot.command.pattern import PatternResult_T
from pepperbot.exceptions import PatternFormotError
from pepperbot.main import *
from pepperbot.models.sender import Sender


def use_pattern(loc) -> Dict[str, PatternResult_T]:
    """todo 通过inspect，直接从globals CommandContext中获取context，实现0参数"""
    debug(loc)
    return loc["context"]["pattern"][
        inspect.currentframe().f_back.f_code.co_name
    ]  # type:ignore


FAQ = {
    "welearn": {
        "练习没有答案": (Text("私聊机器人，提供账号、密码、课程名称、所在单元")),
        "练习不能自动答题": (
            Text(
                dedent(
                    """\
                        有些课程只能显示答案，有的课程可以自动作答某些类型的题目
                        比较主流的课程都做了适配，至少可以显示答案
                        一些比较冷门的课程未做适配
                    """
                )
            ),
        ),
        "练习自动提交": (
            Text(
                dedent(
                    """\
                        不支持自动提交，也不打算开发此功能，因为需要给每种课程都做适配，很耗时间
                        并且做成全自动，容易被官方针对
                    """
                )
            ),
        ),
        "刷时长无效": (
            Text(
                dedent(
                    """\
                        通过左上角的设置按钮开启设置面板，开启刷时长之后保存
                        部分课程可能需要Ctrl + F5，或者重启浏览器才行
                        建议将切换间隔切换至0.2，即12秒，看一下是否正常切换
                        如果还是无法运行，检查下自己使用的是否是最新版本的chrome, temper monkey, 和本脚本
                    """
                )
            ),
        ),
        "班级测试自动答题": (Text("有空了实现"),),
        "班级测试没有答案": (
            Text(
                dedent(
                    """\
                        答案收集自大家的上传，如果没有人上传，那就没有答案
                        可以让同学先做，做完之后上传
                    """
                )
            ),
        ),
        "怎么上传班级测试答案": (
            Text(
                dedent(
                    """\
                        进入已完成的测试，点击查询即可
                        如果有多个页面，上传完当前页面，可以前往下一个页面上传
                    """
                )
            ),
        ),
    },
    "tsinghua": {
        "不显示窗口": (Text("url匹配问题，刷新一下即可"),),
        "练习自动答题": (Text("有空了实现"),),
        "练习自动提交": (Text("暂时不考虑实现"),),
    },
}

WELEARN_QUESTIONS_MAP = {
    index: question for index, question in enumerate(FAQ["welearn"].keys(), start=1)
}

WELEARN_QUESTIONS_PRESENTATION = ""
for index, question in WELEARN_QUESTIONS_MAP.items():
    WELEARN_QUESTIONS_PRESENTATION += f"{index}) {question}\n"

TSINGHUA_QUESTIONS_MAP = {
    index: question for index, question in enumerate(FAQ["tsinghua"].keys(), start=1)
}

TSINGHUA_QUESTIONS_PRESENTATION = ""
for index, question in TSINGHUA_QUESTIONS_MAP.items():
    TSINGHUA_QUESTIONS_PRESENTATION += f"{index}) {question}\n"


class DeliverOrder(BaseModel):
    order: int

    @validator("order")
    def check_order(cls, value):
        if value not in range(1, 4):
            raise PatternFormotError("请输入有效序号")


class WelearnOrder(BaseModel):
    order: int

    @validator("order")
    def check_order(cls, value):
        if value not in range(1, 8):
            raise PatternFormotError("请输入有效序号")


class TsinghuaOrder(BaseModel):
    order: int

    @validator("order")
    def check_order(cls, value):
        if value not in range(1, 4):
            raise PatternFormotError("请输入有效序号")


@as_command(
    needPrefix=False,
    prefix=[],
    also=[""],
    includeClassName=True,
    exitPattern=["我?退出(对话)?"],
    at=True,
    timeout=30,
)
class 常见问题:
    async def exit(self, bot: GroupCommonBot, **kwargs):
        await bot.group_msg(
            Text("用户主动退出\n"),
            Text("解答完成，欢迎再来😀\n"),
            Text("本机器人基于PepperBot，https://github.com/SSmJaE/PepperBot"),
        )

    async def finish(self, bot: GroupCommonBot, sender: Sender, **kwargs):
        await bot.group_msg(
            At(sender.user_id),
            Text("解答完成，欢迎再来😀\n"),
            Text("本机器人基于PepperBot，https://github.com/SSmJaE/PepperBot"),
        )

    async def timeout(self, bot: GroupCommonBot, **kwargs):
        await bot.group_msg(
            Text("用户超时未回复，结束会话"),
            Text("解答完成，欢迎再来😀\n"),
            Text("本机器人基于PepperBot，https://github.com/SSmJaE/PepperBot"),
        )

    async def initial(
        self, bot: GroupCommonBot, chain: MessageChain, sender: Sender, **kwargs
    ):
        await bot.group_msg(
            At(sender.user_id),
            Text(
                dedent(
                    """\
                    脚本使用文档https://ssmjae.github.io/EOC/
                    想了解哪方面的信息？

                    1) U校园
                    2) welearn
                    3) 清华社

                    回复序号，回复“退出”以退出
                """
                )
            ),
        )

        return self.deliver

    @pattern(DeliverOrder, with_formot_hint=True)
    async def deliver(
        self,
        bot: GroupCommonBot,
        sender: Sender,
        chain: MessageChain,
        context: Dict,
    ):

        order = use_pattern(locals())["order"]

        # getattr(self, HANDLER_MAP[order])(bot, chain, **kwargs)
        if order == 1:
            await bot.group_msg(
                At(sender.user_id),
                Text("被U校园官方律师函警告，已经停止维护"),
            )

            await asyncio.sleep(1)
            await bot.group_msg(
                At(sender.user_id),
                Text("回复“继续”以继续"),
            )

            return self.whether_continue

        if order == 2:
            await bot.group_msg(
                At(sender.user_id),
                Text(
                    f"""\
想了解welearn的？

{WELEARN_QUESTIONS_PRESENTATION}

回复序号，回复“退出”以退出"""
                ),
            )

            return self.handle_welearn

        if order == 3:
            await bot.group_msg(
                At(sender.user_id),
                Text(
                    """\
想了解清华社的？

{TSINGHUA_QUESTIONS_PRESENTATION}

回复序号，回复“退出”以退出"""
                ),
            )

            return self.handle_tsinghua

    @pattern(WelearnOrder)
    async def handle_welearn(
        self,
        bot: GroupCommonBot,
        sender: Sender,
        chain: MessageChain,
        context: Dict,
    ):

        order = cast(int, use_pattern(locals())["order"])

        await bot.group_msg(
            At(sender.user_id),
            *FAQ["welearn"][WELEARN_QUESTIONS_MAP[order]],
        )

        await asyncio.sleep(1)
        await bot.group_msg(
            At(sender.user_id),
            Text("回复“继续”以继续"),
        )

        return self.whether_continue

    # todo 不能自动获取chain，必须要在handler中显示指明chain，哪怕不用
    # 也许可以中转一下，__kwargs__
    # fit_kwargs不传入，但是可以静默绑定，这两个不冲突，一个面向用户，一个面向框架
    @pattern(TsinghuaOrder)
    async def handle_tsinghua(
        self,
        bot: GroupCommonBot,
        sender: Sender,
        chain: MessageChain,
        context: Dict,
    ):
        order = cast(int, use_pattern(locals())["order"])

        await bot.group_msg(
            At(sender.user_id),
            *FAQ["tsinghua"][TSINGHUA_QUESTIONS_MAP[order]],
        )

        await asyncio.sleep(1)
        await bot.group_msg(
            At(sender.user_id),
            Text("回复“继续”以继续"),
        )

        return self.whether_continue

    async def whether_continue(
        self,
        bot: GroupCommonBot,
        chain: MessageChain,
        sender: Sender,
    ):
        if chain.any("y", "Y", "继续", "是", "嗯", "对", "好"):
            await bot.group_msg(
                # todo sender.at()
                At(sender.user_id),
                Text(
                    dedent(
                        """\
                    脚本使用文档https://ssmjae.github.io/EOC/
                    想了解哪方面的信息？

                    1) U校园
                    2) welearn
                    3) 清华社

                    回复序号，回复“退出”以退出
                """
                    )
                ),
            )

            return self.deliver
        else:
            return None


@with_command(commandClasses=[常见问题])
@register(groupId=[1041902989, 1057809143, 628421419, 793334204, 893609211])
class JustForReplyCommonQuestions:
    pass


run(debug=True, port=14323)
