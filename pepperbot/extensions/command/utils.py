import re
from typing import Any, Callable, Dict, Iterable, List, Sequence, Set, Tuple

from devtools import debug, pformat

from pepperbot.adapters.onebot.event import construct_chain
from pepperbot.core.message.chain import MessageChain
from pepperbot.core.message.segment import At, T_SegmentInstance, Text
from pepperbot.core.route.available import check_available
from pepperbot.extensions.log import debug_log, logger
from pepperbot.store.command import CommandConfig
from pepperbot.store.event import EventMetadata
from pepperbot.store.meta import (
    class_command_config_mapping,
    class_command_mapping,
    get_bot_id,
)
from pepperbot.types import T_DispatchHandler


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


# running_command_mapping: Dict[T_BotProtocol, config_id] = {}


async def has_running_command(
    event_meta: EventMetadata, class_command_config_ids: Set[str]
) -> Tuple[bool, T_DispatchHandler]:
    # TODO 直接设置正在running的指令，不需要再去数据库中查询
    # 针对per 消息来源

    from pepperbot.extensions.command.handle import get_command_status

    for class_command_config_id in class_command_config_ids:
        class_command_config_cache = class_command_config_mapping[
            class_command_config_id
        ]
        command_name = class_command_config_cache.class_command_name
        command_config = class_command_config_cache.command_config

        # 判断时，获取/新建一次status，之后run时又一次，可能导致出现两个status，一个running，一个false
        status, created = await get_command_status(
            event_meta, command_name, command_config
        )
        # if not created:

        # pointer = status.pointer
        if status.running:
            return True, (
                class_command_config_cache.command_config.propagation_group,
                class_command_config_cache.command_config.priority,
                class_command_config_cache.command_config.concurrency,
                "class_commands",
                class_command_config_id,
            )
        # if pointer != "initial":

    return False, ("", 0, False, "class_commands", "")


async def find_first_available_command(
    ordered_command_handlers: List[T_DispatchHandler],
    event_metadata: EventMetadata,
) -> Tuple[bool, T_DispatchHandler]:
    """只有没有running的指令时，才会执行这个函数"""

    from pepperbot.extensions.command.handle import construct_command_kwargs

    for (
        propagation_group,
        priority,
        concurrency,
        handler_type,
        class_command_config_id,
    ) in ordered_command_handlers:
        class_command_config_cache = class_command_config_mapping[
            class_command_config_id
        ]
        command_name = class_command_config_cache.class_command_name
        command_config = class_command_config_cache.command_config

        meet_prefix, prefix_with_alias, prefix, alias = meet_command_prefix(
            await construct_chain(event_metadata),
            command_name,
            command_config,
        )

        class_command_cache = class_command_mapping[command_name]
        command_method_mapping = class_command_cache.command_method_mapping
        command_method_cache = command_method_mapping["initial"]

        # 先判断是否满足前缀，在判断available，
        # 1.因为判断前缀性能开销比较小，失败的话，直接就不用判断available了
        # 2.checker的参数中，需要有prefix_with_alias，所以需要先判断前缀

        if not meet_prefix:
            logger.info(f"该事件不满足指令 {command_name} {class_command_config_id} 的执行条件")
            # logger.info(f"<y>{chain.pure_text}</y> 不满足指令 <lc>{command_name}</lc> 的执行条件")
            continue

        else:
            # TODO 优化一下这里的性能，不要重复构造这么多次chain、sender之类
            # 可以直接在handle_event够构造，全局使用
            # class_handle也是，现在是每个event_handler中，如果用到了chain，都会重新构造一次
            command_kwargs = await construct_command_kwargs(
                event_metadata, class_command_config_id, lambda: None, False
            )

            # TODO 现在的实现，initial会触发两次available检查
            available = await check_available(
                command_method_cache.method, command_kwargs, is_class=False
            )
            if not available:
                logger.info(
                    f"该事件不满足指令 {command_name} {class_command_config_id} 的available校验"
                )
                continue

            # TODO 应该不存在重复的config_id的可能性
            # 哪怕class相同、priority相同，只要调用了多次as_command，则config_id一定不同
            # 如果只调用了一次as_command，那只会出现一次config_id
            return True, (
                propagation_group,
                priority,
                concurrency,
                handler_type,
                class_command_config_id,
            )

    return False, ("", 0, False, "class_commands", "__does_not_exist__")
