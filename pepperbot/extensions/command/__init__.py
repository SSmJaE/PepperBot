from inspect import isclass
from typing import Any, Callable, List, Optional, Sequence, cast
from devtools import debug

from pepperbot.store.command import COMMAND_CONFIG, CommandConfig
from pepperbot.types import BaseClassCommand


# todo command的权限管理
# todo command的黑白名单，动态黑白名单(提供函数，参数为当前发言用户)


def as_command(
    *args,
    need_prefix: bool = True,
    prefixes: Sequence[str] = None,
    aliases: Sequence[str] = None,
    include_class_name: bool = True,
    exit_patterns: Sequence[str] = None,
    require_at: bool = False,
    timeout: Optional[int] = 30,
    history_size: Optional[int] = None,
    **kwargs,
):
    """将一个class注册为指令"""

    # 自动获取所有kwargs
    command_kwargs = locals()
    del command_kwargs["args"]
    del command_kwargs["kwargs"]

    # 处理函数动态默认值复用的问题
    for config in ("prefixes", "aliases", "exit_patterns", "history_size"):
        if command_kwargs[config] == None:
            command_kwargs.pop(config)

    command_config = CommandConfig(**command_kwargs)

    def decorator(class_command: Any):
        initial_method = getattr(class_command, "initial", None)
        if not callable(initial_method):
            raise NotImplementedError(f"指令 {class_command.__name__} 需要实现initial方法作为入口")

        setattr(class_command, COMMAND_CONFIG, command_config)

        return cast(BaseClassCommand, class_command)

    return decorator


# class CommonEndMixin:
#     # 用户主动退出
#     async def exit(
#         self, bot: GroupCommonBot, chain: MessageChain, sender: Sender, **kwargs
#     ):
#         await bot.group_msg(Text("用户主动退出"))

#     # 流程正常退出(在中间的流程return None也是正常退出)
#     async def finish(
#         self, bot: GroupCommonBot, chain: MessageChain, sender: Sender, **kwargs
#     ):
#         # todo group_msg内部，自动合并相邻的Text
#         await bot.group_msg(Text(f"{sender.user_id}"), Text("命令正常执行完毕后退出"))

#     async def timeout(
#         self, bot: GroupCommonBot, chain: MessageChain, sender: Sender, **kwargs
#     ):
#         await bot.group_msg(Text("用户超时未回复，结束会话"))
