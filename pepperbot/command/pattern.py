from functools import wraps
from inspect import isclass, ismethod

from pydantic.fields import ModelField
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
    Tuple,
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

TRUE_TEXTS = ("True", "true", "1")
FALSE_TEXTS = ("False", "false", "0")

PatternResult_T = Union[str, int, float, bool, SegmentInstance_T]


def merge_multi_text(*args: Text):
    """
    为什么要合并字符串呢？应为接收到的消息类型，可能是分片的，也可能是连续的，
    为了保持一致，全部转换成连续的，再进行正则会方便很多
    """
    mergedString = ""
    for text in args:
        mergedString += text.formatted["data"]["text"] + " "

    return Text(mergedString)


def merge_text_of_chain(chain: List[SegmentInstance_T]):
    """合并相邻的Text片段"""

    compressed_chain: List[SegmentInstance_T] = []
    chainLength = len(chain)

    lastNotTextSegmentIndex = 0
    for index, segment in enumerate(chain):
        debug(segment.__class__.__name__)
        if segment.__class__.__name__ != "Text":

            if index == 0:  # 第一个segment为非Text的情况
                compressed_chain.append(segment)
                lastNotTextSegmentIndex = index + 1
                continue

            multiText: List[Any] = chain[lastNotTextSegmentIndex:index]

            compressed_chain.append(merge_multi_text(*multiText))
            compressed_chain.append(segment)
            lastNotTextSegmentIndex = index + 1

    # 倒数第二个为非Text，最后一个为Text的情况
    if chain[chainLength - 1].__class__.__name__ == "Text":
        compressed_chain.append(
            merge_multi_text(*cast(List, chain[lastNotTextSegmentIndex:chainLength]))
        )

    return compressed_chain


def merge_text_of_model(command_pattern: BaseModel):
    """
    合并pattern_model中的str, int, float, bool, 即python的四种简单类型

    不管有几个连续的Textable segment，都解析为List[Tuple[str, ModelField]]

    其它类型解析为Tuple[str, ModelField]
    """

    debug(command_pattern.__fields__)

    compressed_model: List[
        Union[List[Tuple[str, ModelField]], Tuple[str, ModelField]]
    ] = []
    buffer = list(command_pattern.__fields__.items())

    lastNotStrIndex = 0
    for index, (argName, field) in enumerate(command_pattern.__fields__.items()):
        if field.type_ not in [str, int, float, bool]:

            if index == 0:  # 第一个field为非Text的情况
                compressed_model.append((argName, field))
                lastNotStrIndex = index + 1
                continue

            multiText: List[Any] = buffer[lastNotStrIndex:index]

            compressed_model.append(multiText)
            compressed_model.append((argName, field))
            lastNotStrIndex = index + 1

    # 倒数第二个为非Text，最后一个为Text的情况
    if buffer[len(buffer) - 1][1].type_ in [str, int, float, bool]:
        compressed_model.append(buffer[lastNotStrIndex : len(buffer)])

    return compressed_model


def check_type(
    command_pattern: Any,
    compressed_chain: List[SegmentInstance_T],
    compressed_model: List[Union[List[Tuple[str, ModelField]], Tuple[str, ModelField]]],
):
    pattern_result = OrderedDict()

    for index, (segment, chunk) in enumerate(zip(compressed_chain, compressed_model)):
        # debug(type(segment))
        # debug(type(chunk))

        if isinstance(segment, Text):
            if not isinstance(chunk, list):  # 所有text都被解析为list[(name, model)]
                raise PatternFormotError("未按照格式提供参数")

            fields = chunk

            regex = r""
            arg_count = len(fields)
            for index, name_field in enumerate(fields):
                (arg_name, field) = name_field

                if index != arg_count - 1:
                    regex += r"(\S+)\s*"
                else:
                    regex += r"(\S+)"

                debug(field.type_)

            debug(regex, segment.text)
            texts = re.search(regex, segment.text).groups()  # type:ignore

            debug(texts)

            if len(texts) != arg_count:
                raise PatternFormotError(f"未按照格式提供参数 参数之间使用空格分隔")

            for index, raw_text in enumerate(texts):
                arg_name, field = fields[index]

                debug(raw_text, field.type_)

                result = None

                if field.type_ == str:
                    result = raw_text

                if field.type_ == bool:
                    if raw_text not in (*TRUE_TEXTS, *FALSE_TEXTS):
                        raise PatternFormotError(
                            f"未按照格式提供参数 {arg_name}应为{field.type_}类型"
                        )
                    else:
                        if raw_text in TRUE_TEXTS:
                            result = True
                        else:
                            result = False

                else:  # 解析int, float, bool
                    try:
                        result = field.type_(raw_text)

                    except Exception as e:
                        debug(e)
                        raise PatternFormotError(
                            f"未按照格式提供参数 {arg_name}应为{field.type_}类型"
                        )

                pattern_result[arg_name] = result

        # todo 支持pydantic的Field，比如gt,lt,对输出的报错信息，转为PatternFormotError
        # 最好能找到，pydantic中是怎么使用ModelField进行字段验证的，只是使用就好了
        # snap: int = Field(
        #     42,
        #     title="The Snap",
        #     description="this is the value of snap",
        #     gt=30,
        #     lt=50,
        # )

        else:  # 检测是否是有效类型，Face，Image之类
            chunk = cast(Tuple[str, ModelField], chunk)
            (arg_name, field) = chunk

            if type(segment) != field.type_:
                raise PatternFormotError(f"未按照格式提供参数 {arg_name}应为{field.type_}类型")

            pattern_result[arg_name] = segment

        # 支持pydantic的validate装饰器
        for arg_name, validators in command_pattern.__validators__.items():
            for validator in validators:
                validator.func(command_pattern.__class__, pattern_result[arg_name])

    return pattern_result


def pattern(
    command_pattern: object,
    max_time: int = None,
    on_format_error: Callable[[str], str] = None,
    with_formot_hint: bool = True,
):
    """
    用于command的装饰器，对message chain进行预拦截，满足pattern放行，

    注入解析后的参数，并保存在context中，不然执行on_format_error

    Args:
        command_pattern (object): [pattern应继承自pydantic的BaseModel]
        max_time (int, optional): [同一个进度，允许尝试几次]. Defaults to None.
    """

    def decorator(f: F) -> F:
        @wraps(f)
        async def wrapper(self: BaseModel, *args, **kwargs):
            nonlocal command_pattern
            command_pattern = cast(BaseModel, command_pattern)

            chain: MessageChain = kwargs["chain"]
            bot: GroupCommonBot = kwargs["bot"]
            context: Dict = kwargs["context"]

            # todo pydantic有没有原生的功能
            # 尝试解析，解析失败，报错
            # todo List(展开), Any, Union, List[Union/Any]

            formot_hint = "请按照 "
            for argName, field in command_pattern.__fields__.items():
                formot_hint += f"<{argName} : {field.type_.__name__}> "
            formot_hint += "的格式输入\n不需要<或者>，:右侧是该参数的类型"

            command_class = self.__class__
            commandClassName = command_class.__name__
            debug(command_class)
            commandKwargs: Dict = getattr(command_class, "kwargs")
            debug(commandKwargs)

            try:

                compressed_chain = merge_text_of_chain(chain.chain)
                debug(compressed_chain)

                compressed_model = merge_text_of_model(command_pattern)
                debug(compressed_model)

                if len(compressed_chain) != len(compressed_model):
                    raise PatternFormotError(
                        f"未提供足够参数，应为{len(command_pattern.__fields__)}个，"
                        + f"获得{len(chain.chain)}个"
                    )

                # 对initial应用pattern的情况，支持prefix
                if f.__name__ == "initial":
                    if not isinstance(compressed_chain[0], Text):
                        return f

                    meetPrefix, prefix = is_meet_prefix(
                        chain, commandClassName, commandKwargs
                    )
                    if not meetPrefix:
                        return f

                    withoutPrefix = re.sub(f"^{prefix}", "", compressed_chain[0].text)
                    compressed_chain[0] = Text(withoutPrefix)

                result = check_type(command_pattern, compressed_chain, compressed_model)

                debug(result)

            except PatternFormotError as e:
                # if on_format_error:
                #     return_text = await await_or_normal(
                #         on_format_error, *args, **kwargs
                #     )
                #     if return_text:
                #         await bot.group_msg(return_text)
                # else:
                await bot.group_msg(
                    Text(f"{e}\n{formot_hint if with_formot_hint else ''}")
                )

                return f

            else:
                # todo patternResults的maxSize

                # 满足pattern时，提供解析好的字典
                context.setdefault("pattern", {})
                context["pattern"][f.__name__] = result

                return await await_or_normal(f, self, *args, **kwargs)

        return cast(F, wrapper)

    return decorator
