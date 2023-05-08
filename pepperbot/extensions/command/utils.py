import re
from typing import Any, Callable, Dict, Iterable, List, Sequence, Set, Tuple

from devtools import debug, pformat

from pepperbot.core.message.chain import MessageChain
from pepperbot.core.message.segment import At, T_SegmentInstance, Text
from pepperbot.extensions.log import debug_log, logger
from pepperbot.store.command import CommandConfig
from pepperbot.store.meta import get_bot_id


def merge_text_by_space(*texts: Text) -> Text:
    """
    为什么要合并字符串呢？因为接收到的消息类型，可能是分片的，也可能是连续的，
    为了保持一致，全部转换成连续的，再进行正则会方便很多
    """
    # merged_string = ""
    # text_count = len(texts)

    # for index, text in enumerate(texts, start=1):
    #     merged_string += text.content

    #     if index != text_count:
    #         merged_string += " "

    return Text(" ".join([text.content for text in texts]))


def merge_adjacent_text_segments(
    segments: List[T_SegmentInstance],
) -> List[T_SegmentInstance]:
    """合并相邻的Text片段，空格分隔，方便正则"""
    debug_log(segments)

    if len(segments) <= 1:
        return segments

    compressed_segments: List[T_SegmentInstance] = []

    text_buffer: List[Text] = []
    last_segment_type = Text
    segments_count = len(segments)

    for index, segment in enumerate(segments, start=1):
        # True, True
        if last_segment_type == Text and isinstance(segment, Text):
            text_buffer.append(segment)

            if index == segments_count:
                compressed_segments.append(merge_text_by_space(*text_buffer))

        # False, True
        elif last_segment_type != Text and isinstance(segment, Text):
            text_buffer.append(segment)

            if index == segments_count:
                compressed_segments.append(merge_text_by_space(*text_buffer))

        # True, False
        elif last_segment_type == Text and not isinstance(segment, Text):
            if text_buffer:
                compressed_segments.append(merge_text_by_space(*text_buffer))
                text_buffer = []

            compressed_segments.append(segment)

        # False, False
        else:
            compressed_segments.append(segment)

        last_segment_type = segment.__class__

    return compressed_segments


# def merge_text_of_patterns(
#     patterns: List[Tuple[str, T_PatternArgClass]]
# ) -> T_CompressedPatterns:
#     """
#     合并patterns中的str, int, float, bool, 即python的四种简单类型
#     不管有几个连续的Textable segment，都解析为List[Tuple[str, ModelField]]

#     其它类型解析为Tuple[str, ModelField]

#     [
#         [
#             ("字符1", str),
#             ("字符2", float),
#             ("字符3", int),
#         ],
#         ("表情1", Face),
#         ("图片1", Image),
#         [
#             ("字符4", bool),
#             ("字符5", float),
#         ],
#     ]
#     """
#     if not patterns:
#         return []

#     # 只有一个元素的情况
#     if len(patterns) == 1:
#         arg_type = patterns[0][1]

#         if arg_type in VALID_TEXT_TYPES:
#             return [patterns]
#         else:
#             return patterns  # type:ignore

#     compressed_patterns: T_CompressedPatterns = []

#     text_buffer = []
#     last_pattern_type = str
#     patterns_count = len(patterns)

#     for index, (arg_name, arg_type) in enumerate(patterns, start=1):
#         # Text 都转换为str, 方便比较
#         last_type = str if last_pattern_type in VALID_TEXT_TYPES else last_pattern_type
#         current_type = str if arg_type in VALID_TEXT_TYPES else arg_type

#         # True, True
#         if last_type == current_type == str:
#             text_buffer.append((arg_name, arg_type))

#             if index == patterns_count:
#                 compressed_patterns.append(deepcopy(text_buffer))

#         # False, True
#         elif last_type != str and current_type == str:
#             text_buffer.append((arg_name, arg_type))

#             if index == patterns_count:
#                 compressed_patterns.append(deepcopy(text_buffer))

#         # True, False
#         elif last_type == str and current_type != str:
#             if text_buffer:
#                 compressed_patterns.append(deepcopy(text_buffer))
#                 text_buffer = []

#             compressed_patterns.append((arg_name, arg_type))

#         # False, False
#         else:
#             compressed_patterns.append((arg_name, arg_type))

#         last_pattern_type = arg_type

#     return compressed_patterns


def meet_text_prefix(
    chain: MessageChain,
    command_name: str,
    command_config: CommandConfig,
) -> Tuple[bool, str, str, str]:
    aliases: Set[str] = set(command_config.aliases)
    if command_config.include_class_name:
        aliases.add(command_name)
    # aliases.add("")  # 保证下方循环至少执行一次

    if command_config.need_prefix:
        prefixes: Iterable[str] = set(command_config.prefixes)
    else:  # 保证下方循环至少执行一次
        prefixes = [""]

    debug_log(command_name, "指令名")
    debug_log(prefixes, "所有前缀")
    debug_log(aliases, "所有别名")
    debug_log(chain.pure_text, "纯文本")

    for alias in aliases:
        for prefix in prefixes:
            prefix_with_alias = prefix + alias

            # 如果是At + Text的情况，pure_text之前会多出一个空格
            # 因为经常性，At和Text之间，会手动加一个空格，不如不去掉，就会导致判断失效

            without_side_space = chain.pure_text.strip()
            splitted = without_side_space.split(" ")
            supposed_prefix_with_alias = splitted[0]

            # 必须全等，不然，当有多个指令时，某一个final_prefix是另一个final_prefix的子集时，会导致错误匹配
            # 比如，/a和/ab，当输入/a时，会匹配到/a和/ab，此时如果/a指令在前，/ab就不会被匹配到
            # /gpt 和 /gpt-manage的情况
            # 需要考虑到，仅/gpt，后面不接任何文字的情况，通过/gpt后有无空格来判断——这个是因为没有判全等，才会有这个问题，判全等就行了
            if prefix_with_alias != supposed_prefix_with_alias:
                debug_log(f"{prefix_with_alias} 不满足 {command_name} 的执行条件")
                continue

            debug_log(f"^{prefix_with_alias} 满足 {command_name} 的执行条件")

            return True, prefix_with_alias, prefix, alias

    return False, "", "", ""


def meet_command_prefix(
    chain: MessageChain,
    command_name: str,
    command_config: CommandConfig,
) -> Tuple[bool, str, str, str]:
    """
    通过command_kwargs和messageChain的pure_text，判断是否触发命令的initial
    """

    # 是否需要@机器人
    if command_config.require_at:
        bot_id = get_bot_id(chain.protocol)  # type:ignore

        # debug(bot_id)
        # debug(chain.has(At(bot_id)))

        if not chain.has(At(bot_id)):
            return False, "", "", ""

    meet_prefix, final_prefix, prefix, alias = meet_text_prefix(
        chain, command_name, command_config
    )
    if not meet_prefix:
        return False, "", "", ""

    return True, final_prefix, prefix, alias


def meet_command_exit(chain: MessageChain, command_config: CommandConfig):
    """退出判断"""

    debug_log(command_config.exit_patterns, "退出正则")
    for pattern in command_config.exit_patterns:
        # debug_log(re.search(pattern, chain.pure_text))
        if re.search(pattern, chain.pure_text):
            return True

    return False
