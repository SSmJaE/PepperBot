import re
from functools import wraps
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    List,
    Optional,
    OrderedDict,
    Tuple,
    Union,
    cast,
)

from pepperbot.extensions.log import logger
from devtools import pformat
from pepperbot.core.message.chain import MessageChain, T_SegmentInstance
from pepperbot.core.message.segment import Text
from pepperbot.exceptions import EventHandleError, PatternFormotError
from pepperbot.store.command import (
    FALSE_TEXTS,
    TRUE_TEXTS,
    VALID_TEXT_TYPES,
    CommandMethodCache,
    T_CompressedPatterns,
    T_PatternArg,
    T_PatternArgResult,
    T_ValidTextType,
    T_ValidTextTypeInstance,
)
from copy import deepcopy

if TYPE_CHECKING:
    from pepperbot.extensions.command.handle import CommandSender


def merge_multi_text_with_space(*texts: Text):
    """
    为什么要合并字符串呢？应为接收到的消息类型，可能是分片的，也可能是连续的，
    为了保持一致，全部转换成连续的，再进行正则会方便很多
    """
    merged_string = ""
    text_count = len(texts)

    for index, text in enumerate(texts, start=1):
        merged_string += text.content

        if index != text_count:
            merged_string += " "

    return Text(merged_string)


T_CompressedSegments = List[T_SegmentInstance]


def merge_text_of_segments(segments: List[T_SegmentInstance]) -> T_CompressedSegments:
    """合并相邻的Text片段，空格分隔，方便正则"""
    logger.debug(pformat(segments))

    if len(segments) <= 1:
        return segments

    compressed_segments: T_CompressedSegments = []

    text_buffer: List[Text] = []
    last_segment_type = Text
    segments_count = len(segments)

    for index, segment in enumerate(segments, start=1):

        # True, True
        if last_segment_type == Text and isinstance(segment, Text):
            text_buffer.append(segment)

            if index == segments_count:
                compressed_segments.append(merge_multi_text_with_space(*text_buffer))

        # False, True
        elif last_segment_type != Text and isinstance(segment, Text):
            text_buffer.append(segment)

            if index == segments_count:
                compressed_segments.append(merge_multi_text_with_space(*text_buffer))

        # True, False
        elif last_segment_type == Text and not isinstance(segment, Text):
            if text_buffer:
                compressed_segments.append(merge_multi_text_with_space(*text_buffer))
                text_buffer = []

            compressed_segments.append(segment)

        # False, False
        else:
            compressed_segments.append(segment)

        last_segment_type = segment.__class__

    return compressed_segments


def merge_text_of_patterns(
    patterns: List[Tuple[str, T_PatternArg]]
) -> T_CompressedPatterns:
    """
    合并patterns中的str, int, float, bool, 即python的四种简单类型
    不管有几个连续的Textable segment，都解析为List[Tuple[str, ModelField]]

    其它类型解析为Tuple[str, ModelField]

    [
        [
            ("字符1", str),
            ("字符2", float),
            ("字符3", int),
        ],
        ("表情1", Face),
        ("图片1", Image),
        [
            ("字符4", bool),
            ("字符5", float),
        ],
    ]
    """
    if not patterns:
        return []

    # 只有一个元素的情况
    if len(patterns) == 1:
        arg_type = patterns[0][1]

        if arg_type in VALID_TEXT_TYPES:
            return [patterns]
        else:
            return patterns  # type:ignore

    compressed_patterns: T_CompressedPatterns = []

    text_buffer = []
    last_pattern_type = str
    patterns_count = len(patterns)

    for index, (arg_name, arg_type) in enumerate(patterns, start=1):

        # Text 都转换为str, 方便比较
        last_type = str if last_pattern_type in VALID_TEXT_TYPES else last_pattern_type
        current_type = str if arg_type in VALID_TEXT_TYPES else arg_type

        # True, True
        if last_type == current_type == str:
            text_buffer.append((arg_name, arg_type))

            if index == patterns_count:
                compressed_patterns.append(deepcopy(text_buffer))

        # False, True
        elif last_type != str and current_type == str:
            text_buffer.append((arg_name, arg_type))

            if index == patterns_count:
                compressed_patterns.append(deepcopy(text_buffer))

        # True, False
        elif last_type == str and current_type != str:
            if text_buffer:
                compressed_patterns.append(deepcopy(text_buffer))
                text_buffer = []

            compressed_patterns.append((arg_name, arg_type))

        # False, False
        else:
            compressed_patterns.append((arg_name, arg_type))

        last_pattern_type = arg_type

    return compressed_patterns


def match_by_regex(text_patterns: List[Tuple[str, T_ValidTextType]], segment: Text):
    """通过正则，匹配对应的text和pattern"""
    regex = r""
    arg_count = len(text_patterns)

    for index, text_pattern in enumerate(text_patterns):
        (arg_name, arg_type) = text_pattern

        # 拼接正则，所有文字参数，应该都是空格分格的
        if index != arg_count - 1:
            regex += r"(\S+)\s*"
        else:
            regex += r"(\S+)"

        # logger.debug(pformat(arg_type))

    # logger.debug(pformat(regex, segment.content))
    match = re.search(regex, segment.content)
    if not match:
        raise PatternFormotError(f"pattern匹配失败-->正则失败")

    texts = match.groups()
    # logger.debug(pformat(texts))

    if len(texts) != arg_count:
        raise PatternFormotError(f"未按照格式提供参数 参数之间使用空格分隔")

    return texts


def try_convert_type(arg_name: str, arg_type: T_ValidTextType, text_without_type: str):
    # logger.debug(pformat(text_without_type, arg_type))

    result: T_ValidTextTypeInstance

    if arg_type == str:
        result = text_without_type

    if arg_type == bool:
        if not (text_without_type in TRUE_TEXTS or text_without_type in FALSE_TEXTS):
            raise PatternFormotError(f"未按照格式提供参数 {arg_name} 应为bool类型")

        else:
            if text_without_type in TRUE_TEXTS:
                result = True
            else:
                result = False

    else:  # 解析int, float
        try:
            result = arg_type(text_without_type)  # type:ignore

        except Exception as e:
            raise PatternFormotError(f"未按照格式提供参数 {arg_name}应为{arg_type}类型")

    return result


def get_pattern_results(
    compressed_patterns: List[
        Union[List[Tuple[str, T_PatternArg]], Tuple[str, T_PatternArg]]
    ],
    compressed_segments: List[T_SegmentInstance],
):
    pattern_result: OrderedDict[str, T_PatternArgResult] = OrderedDict()

    for index, (segment, pattern) in enumerate(
        zip(compressed_segments, compressed_patterns)
    ):
        # logger.debug(pformat(type(segment)))
        # logger.debug(pformat(type(chunk)))

        if isinstance(segment, Text):
            if not isinstance(pattern, list):  # 所有text都被解析为list[(arg_name, arg_type)]
                raise PatternFormotError("未按照格式提供参数")

            text_patterns = cast(List[Tuple[str, T_ValidTextType]], pattern)
            texts = match_by_regex(text_patterns, segment)

            for index, text_without_type in enumerate(texts):
                arg_name, arg_type = text_patterns[index]

                pattern_result[arg_name] = try_convert_type(
                    arg_name,
                    arg_type,
                    text_without_type,
                )

        # todo 支持pydantic的Field，比如gt,lt,对输出的报错信息，转为PatternFormotError
        # 最好能找到，pydantic中是怎么使用ModelField进行字段验证的，只是使用就好了
        # snap: int = Field(
        #     42,
        #     title="The Snap",
        #     description="this is the value of snap",
        #     gt=30,
        #     lt=50,
        # )

        # 支持pydantic的validate装饰器
        # for arg_name, validators in command_pattern.__validators__.items():
        #     for validator in validators:
        #         validator.func(command_pattern.__class__, pattern_result[arg_name])

        else:  # 检测是否是有效类型，Face，Image之类
            pattern = cast(Tuple[str, T_PatternArg], pattern)
            arg_name, arg_type = pattern

            if type(segment) != arg_type:
                raise PatternFormotError(f"未按照格式提供参数 {arg_name} 应为 {arg_type} 类型")

            pattern_result[arg_name] = segment

    return pattern_result


def pattern_config(
    with_formot_hint: bool = True,
    on_format_error: Optional[
        Callable[[T_CompressedSegments, T_CompressedPatterns], str]
    ] = None,
    retry: int = 3,
):
    """装饰器，函数粒度的config"""
    PATTERN_CONFIG = "__pattern_config__"
    pass


async def parse_pattern(
    chain: MessageChain,
    sender: "CommandSender",
    method_name,
    cache: CommandMethodCache,
    prefix: str,
    context,
):
    """
    根据签名中的PatternArg，自动解析参数，并转换为对应类型，自动注入函数调用中

    满足pattern放行，如果不满足，会对方法调用进行拦截，
    """

    if not cache.compressed_patterns:
        return {}

    compressed_patterns = cache.compressed_patterns

    # todo pydantic有没有原生的功能
    # 尝试解析，解析失败，报错
    # todo List(展开), Any, Union, List[Union/Any]

    formot_hint = "请按照 "
    for arg_name, arg_type in cache.patterns:
        formot_hint += f"<{arg_name} : {arg_type.__name__}> "
    formot_hint += "的格式输入\n不需要输入<或者>，:右侧是该参数的类型"

    # formot_hint添加prefix
    # if method_name == "initial":

    results = {}

    try:

        compressed_segments = merge_text_of_segments(chain.segments)
        logger.debug(pformat(compressed_segments))

        if len(compressed_segments) != len(compressed_patterns):
            raise PatternFormotError(
                f"未提供足够参数，应为{len(cache.patterns)}个，" + f"获得{len(chain.segments)}个"
            )

        # 对initial应用pattern的情况，支持prefix
        # 目前仅支持文字prefix
        if method_name == "initial":
            if not isinstance(compressed_segments[0], Text):
                return PatternFormotError("目前仅支持文字前缀")

            with_prefix = compressed_segments[0].content
            without_prefix = re.sub(f"^{prefix}", "", with_prefix)
            compressed_segments[0].content = without_prefix

        results = get_pattern_results(compressed_patterns, compressed_segments)

    except PatternFormotError as e:
        # if on_format_error:
        #     return_text = await await_or_normal(
        #         on_format_error, *args, **kwargs
        #     )
        #     if return_text:
        #         await bot.group_msg(return_text)
        # else:
        await sender.send_message(
            # Text(f"{e}\n{formot_hint if with_formot_hint else ''}")
            Text(f"{e}\n{formot_hint}")
        )

        logger.error("指令解析失败")
        raise e  # 需要中断指令的执行

    else:
        # todo patternResults的maxSize

        logger.debug(pformat(results))
        return results

    # finally:
    # # 满足pattern时，提供解析好的字典
    # context.setdefault("pattern", {})
    # context["pattern"][f.__name__] = result

    # return await await_or_normal(f, self, *args, **kwargs)
