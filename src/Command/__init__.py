from functools import wraps
from inspect import ismethod
from typing import Any, Callable, Dict, List, TypeVar, Union, cast

from pydantic import BaseModel
from src.main import *

F = TypeVar("F", bound=Callable[..., Any])


class PatternModel:
    pass


# todo 多个group handler，相同command的处理(解析所有指令和groupId，重新生成缓存)

# todo command的权限管理
# todo command的黑白名单，动态黑白名单(提供函数，参数为当前发言用户)


def with_command(commandClasses: List[CommandClassBase] = [], *args, **kwargs):
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
            print("应为class")

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
    mode: Literal["normal", "crossUser", "crossGroup", "global"] = "normal",
    **kwargs,
):
    """将一个class注册为指令类，并收集关键字参数"""

    def decorator(commandClass: object):
        initialMethod = getattr(commandClass, "initial")
        if not callable(initialMethod):
            raise NotImplementedError("命令类需要实现initial方法作为入口")

        setattr(
            commandClass,
            "kwargs",
            # todo 使用annanotion自动获取所有kwargs
            {
                "needPrefix": needPrefix,
                "prefix": prefix,
                "also": also,
                "includeClassName": includeClassName,
                "exitPattern": exitPattern,
                "at": at,
                "timeout": timeout,
                "mode": mode,
            },
        )

        return cast(CommandClassBase, commandClass)

    return decorator


class CommandClassNecessary:
    async def initial(self):
        raise NotImplementedError()


def pattern(
    commandPattern: Union[str, PatternModel] = None,
    onFormatError=None,
    # 同一个进度，允许尝试几次
    maxTime=None,
):
    """对message chain进行预拦截，满足pattern放行，不然执行onFormatError"""

    def decorator(f: F) -> F:
        @wraps(f)
        def wrapper(self: object, *args, **kwargs):

            # todo 满足pattern时，提供解析好的字典

            return f(self, *args, **kwargs)

        return cast(F, wrapper)

    return decorator


class CommonEndMixin:
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
        # todo group_msg内部，自动合并相邻的Text
        await bot.group_msg(Text(f"{sender.user_id}"), Text("命令正常执行完毕后退出"))

    async def timeout(
        self, bot: GroupMessageBot, chain: MessageChain, sender: Sender, **kwargs
    ):
        await bot.group_msg(Text("用户超时未回复，结束会话"))
