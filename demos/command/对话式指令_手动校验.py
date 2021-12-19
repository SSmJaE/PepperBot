from textwrap import dedent

from pepperbot.command import as_command, with_command
from pepperbot.main import *
from pepperbot.models.sender import Sender

HANDLER_MAP = {
    1: "handle_unipus",
    2: "handle_welearn",
    3: "handle_tsinghua",
}


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
    async def exit(self, bot: GroupCommonBot):
        await bot.group_msg(
            Text("用户主动退出\n"),
            Text("解答完成，欢迎再来😀\n"),
            Text("本机器人基于PepperBot，https://github.com/SSmJaE/PepperBot"),
        )

    async def finish(self, bot: GroupCommonBot, sender: Sender):
        await bot.group_msg(
            At(sender.user_id),
            Text("解答完成，欢迎再来😀\n"),
            Text("本机器人基于PepperBot，https://github.com/SSmJaE/PepperBot"),
        )

    async def timeout(self, bot: GroupCommonBot):
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

    # @pattern(
    #     TestModel,
    # )
    async def deliver(
        self,
        bot: GroupCommonBot,
        chain: MessageChain,
        sender: Sender,
        context: Dict,
        messageQueue: List[UserMessage],
        **kwargs,
    ):

        # patternResults: List[Dict[str, SegmentInstance_T]] = context["patternResults"]

        # buffer = []
        # for argName, segment in patternResults[-1].items():
        #     buffer.append(Text(f"\n{argName} "))
        #     buffer.append(segment)

        try:
            order_match = re.search(r"\d", chain.pure_text)

            if not order_match:
                raise Exception("请输入序号")

            order_string = order_match.group()

            order = int(order_string)

            if order not in [1, 2, 3]:
                raise Exception("请输入有效序号")

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
                        dedent(
                            """\
                            想了解welearn的？

                            1) 练习没有答案
                            2) 练习不能自动答题
                            3) 练习自动提交
                            4) 刷时长无效
                            5) 班级测试自动答题
                            6) 班级测试没有答案

                            回复序号，回复“退出”以退出
                        """
                        )
                    ),
                )

                return self.handle_welearn

            if order == 3:
                await bot.group_msg(
                    At(sender.user_id),
                    Text(
                        dedent(
                            """\
                            想了解清华社的？

                            1) 不显示窗口
                            2) 练习自动答题
                            3) 练习自动提交

                            回复序号，回复“退出”以退出
                        """
                        )
                    ),
                )

                return self.handle_tsinghua

        except Exception as e:
            await bot.group_msg(
                At(sender.user_id),
                Text(f"{e}"),
            )

            return self.deliver

    # async def handle_unipus(
    #     self,
    #     bot: GroupCommonBot,
    #     chain: MessageChain,
    #     sender: Sender,
    #     context: Dict,
    #     messageQueue: List[UserMessage],
    #     **kwargs,
    # ):
    #     await bot.group_msg(Text("u校园"))

    async def handle_welearn(
        self,
        bot: GroupCommonBot,
        chain: MessageChain,
        sender: Sender,
        context: Dict,
        messageQueue: List[UserMessage],
        **kwargs,
    ):

        try:
            order_match = re.search(r"\d", chain.pure_text)

            if not order_match:
                raise Exception("请输入序号")

            order_string = order_match.group()

            order = int(order_string)

            if order not in [1, 2, 3, 4, 5, 6]:
                raise Exception("请输入有效序号")

            if order == 1:
                await bot.group_msg(
                    At(sender.user_id),
                    Text("私聊机器人，提供账号、密码、课程名称、所在单元"),
                )

            if order == 2:
                await bot.group_msg(
                    At(sender.user_id),
                    Text(
                        dedent(
                            """\
                            有些课程只能显示答案，有的课程可以自动作答某些类型的题目
                            比较主流的课程都做了适配，至少可以显示答案
                            一些比较冷门的课程未做适配
                        """
                        )
                    ),
                )

            if order == 3:
                await bot.group_msg(
                    At(sender.user_id),
                    Text(
                        dedent(
                            """\
                            不支持自动提交，也不打算开发此功能，因为需要给每种课程都做适配，很耗时间
                            并且做成全自动，容易被官方针对
                        """
                        )
                    ),
                )

            if order == 4:
                await bot.group_msg(
                    At(sender.user_id),
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
                )

            if order == 5:
                await bot.group_msg(
                    At(sender.user_id),
                    Text(
                        dedent(
                            """\
                            有空了实现
                        """
                        )
                    ),
                )

            if order == 6:
                await bot.group_msg(
                    At(sender.user_id),
                    Text(
                        dedent(
                            """\
                            答案收集自大家的上传，如果没有人上传，那就没有答案
                            可以让同学先做，做完之后上传
                        """
                        )
                    ),
                )

            await asyncio.sleep(1)
            await bot.group_msg(
                At(sender.user_id),
                Text("回复“继续”以继续"),
            )

            return self.whether_continue

        except Exception as e:
            await bot.group_msg(
                At(sender.user_id),
                Text(f"{e}"),
            )

            return self.handle_welearn

    async def handle_tsinghua(
        self,
        bot: GroupCommonBot,
        chain: MessageChain,
        sender: Sender,
        context: Dict,
        messageQueue: List[UserMessage],
        **kwargs,
    ):
        try:
            order_match = re.search(r"\d", chain.pure_text)

            if not order_match:
                raise Exception("请输入序号")

            order_string = order_match.group()

            order = int(order_string)

            if order not in [1, 2, 3]:
                raise Exception("请输入有效序号")

            if order == 1:
                await bot.group_msg(
                    At(sender.user_id),
                    Text("url匹配问题，刷新一下即可"),
                )

            if order == 2:
                await bot.group_msg(
                    At(sender.user_id),
                    Text("有空了实现"),
                )

            if order == 3:
                await bot.group_msg(
                    At(sender.user_id),
                    Text("暂时不考虑实现"),
                )

            await asyncio.sleep(1)
            await bot.group_msg(
                At(sender.user_id),
                Text("回复“继续”以继续"),
            )

            return self.whether_continue

        except Exception as e:
            await bot.group_msg(
                At(sender.user_id),
                Text(f"{e}"),
            )

            return self.handle_tsinghua

    async def whether_continue(
        self,
        bot: GroupCommonBot,
        chain: MessageChain,
        sender: Sender,
        context: Dict,
        messageQueue: List[UserMessage],
        **kwargs,
    ):
        if chain.any("y", "Y", "继续", "是", "嗯", "对", "好"):
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
        else:
            return None


@with_command(commandClasses=[常见问题])
@register(groupId=[1041902989, 1057809143, 628421419, 793334204, 893609211])
class JustForReplyCommonQuestions:
    async def group_message(
        self, bot: GroupCommonBot, chain: MessageChain, sender: Sender
    ):
        pass
