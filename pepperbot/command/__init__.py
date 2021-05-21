from functools import wraps
from inspect import isclass, ismethod
from pepperbot.command.parse import is_meet_prefix
from pepperbot.utils.common import await_or_normal
from pepperbot.exceptions import EventHandlerDefineError, PatternFormotError
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Optional,
    OrderedDict,
    Sequence,
    TypeVar,
    Union,
    cast,
)
import re

from devtools import debug
from pydantic import BaseModel
from pepperbot.globals import *
from pepperbot.message.chain import MessageChain
from pepperbot.message.segment import Text
from pepperbot.models.sender import Sender
from pepperbot.parse.bots import GroupCommonBot
from pepperbot.types import CommandClassBase, F


class PatternModel:
    pass


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

        return cast(CommandClassBase, commandClass)

    return decorator


class CommandClassNecessary:
    async def initial(self):
        raise NotImplementedError()


def merge_multi_text(*args: Text):
    mergedString = ""
    for text in args:
        mergedString += text.formatted["data"]["text"]

    return Text(mergedString)


def merge_text_of_chain(chain: List[SegmentInstance_T]):
    compressedChain = []
    chainLength = len(chain)

    lastNotTextSegmentIndex = 0
    for index, segment in enumerate(chain):
        debug(segment.__class__.__name__)
        if segment.__class__.__name__ != "Text":
            multiText: List[Any] = chain[lastNotTextSegmentIndex:index]

            compressedChain.append(merge_multi_text(*multiText))
            compressedChain.append(segment)
            lastNotTextSegmentIndex = index + 1

    if chain[chainLength - 1].__class__.__name__ == "Text":
        compressedChain.append(
            merge_multi_text(*cast(List, chain[lastNotTextSegmentIndex:chainLength]))
        )

    return compressedChain


def merge_MessageChain(chain: MessageChain):
    chain.chain = merge_text_of_chain(chain.chain)


def pattern(
    commandPattern: object,
    # 同一个进度，允许尝试几次
    maxTime=None,
):
    """对message chain进行预拦截，满足pattern放行，注入解析后的参数，并保存在context中，不然执行onFormatError"""

    def decorator(f: F) -> F:
        @wraps(f)
        async def wrapper(self: object, *args, **kwargs):
            nonlocal commandPattern

            chain: MessageChain = kwargs["chain"]
            bot: GroupCommonBot = kwargs["bot"]
            context: Dict = kwargs["context"]

            commandPattern = cast(BaseModel, commandPattern)

            # todo 检测是否是有效类型，Face，Image之类
            # todo pydantic有没有原生的功能
            # todo 解析str为int, float, bool
            # 尝试解析，解析失败，报错
            # todo List(展开), Any, Union, List[Union/Any]

            formotHint = "请按照 "
            for argName, field in commandPattern.__fields__.items():
                formotHint += f"<{argName} : {field.type_.__name__}> "
            formotHint += "的格式输入\n不需要<或者>，:右侧是该参数的类型"

            commandClass = self.__class__
            commandClassName = commandClass.__name__
            debug(commandClass)
            commandKwargs: Dict = getattr(commandClass, "kwargs")
            debug(commandKwargs)

            result = OrderedDict()
            try:

                compressedChain = merge_text_of_chain(chain.chain)

                debug(compressedChain)

                debug(commandPattern.__fields__)

                compressedChunk = []

                buffer = list(commandPattern.__fields__.items())

                lastNotStrIndex = 0
                for index, (argName, field) in enumerate(
                    commandPattern.__fields__.items()
                ):
                    if field.type_ != str:
                        multiText: List[Any] = buffer[lastNotStrIndex:index]

                        compressedChunk.append(multiText)
                        compressedChunk.append((argName, field))
                        lastNotStrIndex = index + 1

                if buffer[len(buffer) - 1][1].type_ == str:
                    compressedChunk.append(buffer[lastNotStrIndex : len(buffer)])

                debug(compressedChunk)

                if len(compressedChain) < len(compressedChunk):
                    raise PatternFormotError("未提供足够参数")

                # 对initial应用pattern的情况，支持prefix
                if f.__name__ == "initial":
                    if not isinstance(compressedChain[0], Text):
                        return f
                    else:
                        meetPrefix, prefix = is_meet_prefix(
                            chain, commandClassName, commandKwargs
                        )
                        if meetPrefix:
                            withoutPrefix = re.sub(
                                f"^{prefix}", "", compressedChain[0].content
                            )
                            compressedChain[0] = Text(withoutPrefix)
                        else:
                            return f

                for index, (segment, chunk) in enumerate(
                    zip(compressedChain, compressedChunk)
                ):
                    # debug(type(segment))
                    # debug(type(chunk))

                    if isinstance(segment, Text):
                        if not isinstance(chunk, list):
                            raise PatternFormotError("未按照格式提供参数")
                        else:

                            regex = r""
                            argLength = len(chunk)
                            for index, arg in enumerate(chunk):
                                (argName, field) = arg

                                if index != argLength - 1:
                                    regex += r"(\S+)\s*"
                                else:
                                    regex += r"(\S+)"

                            debug(regex, segment.content)
                            texts = re.search(regex, segment.content).groups()

                            debug(texts)

                            if len(texts) < argLength:
                                raise PatternFormotError(f"未按照格式提供参数 参数之间使用空格分隔")

                            for index, text in enumerate(texts):
                                result[chunk[index][0]] = Text(text)

                    else:
                        (argName, field) = chunk

                        if type(segment) != field.type_:
                            raise PatternFormotError(
                                f"未按照格式提供参数 {argName}应为{field.type_}类型"
                            )

                        result[argName] = segment

                debug(result)

            except PatternFormotError as e:
                await bot.group_msg(Text(f"{e}\n{formotHint}"))

                return f

            else:

                # todo patternResults的maxSize
                # 满足pattern时，提供解析好的字典
                if not context.get("patternResults"):
                    context["patternResults"] = []

                context["patternResults"].append(result)

                return await await_or_normal(f, self, *args, **kwargs)

        return cast(F, wrapper)

    return decorator


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
