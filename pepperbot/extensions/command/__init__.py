from inspect import isclass
from typing import Callable, List, Optional, Sequence, cast

from pepperbot.command.pattern import pattern
from pepperbot.exceptions import EventHandlerDefineError
from pepperbot.globals import *
from pepperbot.message.chain import MessageChain
from pepperbot.message.segment import Text
from pepperbot.models.sender import Sender
from pepperbot.parse.bots import GroupCommonBot
from pepperbot.types import BaseClassCommand


class PatternModel:
    pass


# todo command的权限管理
# todo command的黑白名单，动态黑白名单(提供函数，参数为当前发言用户)


def with_command(commandClasses: List[BaseClassCommand] = [], *args, **kwargs):
    """为group_message事件响应注入命令类，并不直接可用，需要__cache解析"""

    def decorator(handler: object):
        if isclass(handler):
            decoratorMeta = GroupDecorator(
                **{
                    "args": [*args],
                    "kwargs": {**kwargs, "commandClasses": commandClasses},
                }
            )

            classHandlers.groupMeta[cast(Callable, handler)].decorators[
                "with_command"
            ] = decoratorMeta

            # debug(commandClasses[0].kwargs)
        else:
            raise EventHandlerDefineError("只允许使用with_command装饰器注册class")

        return handler

    return decorator


def as_command(
    *args,
    needPrefix: bool = False,
    # 都是正则，自动加上^
    prefix: Sequence[str] = ["/"],
    # 都是正则
    also: Sequence[str] = [],
    # 类名本身不作为指令
    includeClassName: bool = True,
    # 都是正则
    exitPattern: Sequence[str] = ["^/exit", "^退出"],
    # 是否需要at机器人
    at: bool = False,
    # 会话超时时间，单位秒,
    timeout: Optional[int] = 30,
    maxSize: Optional[int] = None,
    mode: Literal["normal", "crossUser", "crossGroup", "global"] = "normal",
    **kwargs,
):
    """将一个class注册为指令类，并收集关键字参数"""

    # 使用annanotion自动获取所有kwargs
    commandKwargs = locals()
    del commandKwargs["args"]
    del commandKwargs["kwargs"]

    def decorator(commandClass: object):
        initialMethod = getattr(commandClass, "initial")
        if not callable(initialMethod):
            raise NotImplementedError("命令类需要实现initial方法作为入口")

        setattr(
            commandClass,
            "kwargs",
            {**commandKwargs},
        )

        return cast(BaseClassCommand, commandClass)

    return decorator


class CommandClassNecessary:
    async def initial(self):
        raise NotImplementedError()


class CommonEndMixin:
    # 用户主动退出
    async def exit(
        self, bot: GroupCommonBot, chain: MessageChain, sender: Sender, **kwargs
    ):
        await bot.group_msg(Text("用户主动退出"))

    # 流程正常退出(在中间的流程return False/None也是正常退出)
    async def finish(
        self, bot: GroupCommonBot, chain: MessageChain, sender: Sender, **kwargs
    ):
        # todo group_msg内部，自动合并相邻的Text
        await bot.group_msg(Text(f"{sender.user_id}"), Text("命令正常执行完毕后退出"))

    async def timeout(
        self, bot: GroupCommonBot, chain: MessageChain, sender: Sender, **kwargs
    ):
        await bot.group_msg(Text("用户超时未回复，结束会话"))
