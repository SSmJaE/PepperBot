import inspect
import re
from argparse import ArgumentParser, _SubParsersAction
from functools import partial
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Dict,
    List,
    OrderedDict,
    Union,
    cast,
    get_args,
    get_origin,
)
from uuid import uuid4

from devtools import debug

from pepperbot.core.message.chain import MessageChain, T_SegmentInstance
from pepperbot.core.message.segment import T_SegmentClass, Text
from pepperbot.exceptions import InitializationError, PatternFormatError
from pepperbot.extensions.command.node import CommandNode
from pepperbot.extensions.command.parser import CustomArgumentParser, CustomHelpAction
from pepperbot.extensions.command.utils import merge_adjacent_text_segments
from pepperbot.store.command import (
    ARGPARSE_CALLED_METHOD,
    ARGPARSE_HELP,
    DOWNGRADE_PATTERN,
    DOWNGRADE_PATTERN_FORMAT,
    FALSE_TEXTS,
    PATTERN_ARG_TYPES,
    TRUE_TEXTS,
    ClassCommandCache,
    ClassCommandMethodCache,
    ClassCommandStatus,
    T_PatternArgClass,
    T_ValidTextTypeClass,
    T_ValidTextTypeInstance,
    TemporaryPatternArg,
    _PatternArg,
)
from pepperbot.store.event import EventMetadata
from pepperbot.store.meta import SubCommandRelation, command_arguments_cache
from pepperbot.types import T_BotProtocol
from pepperbot.utils.common import await_or_sync

if TYPE_CHECKING:
    from pepperbot.extensions.command.sender import CommandSender


# def match_by_regex(
#     text_patterns: List[Tuple[str, T_ValidTextTypeClass]], segment: Text
# ):
#     """通过正则，匹配对应的text和pattern"""
#     regex = r""
#     arg_count = len(text_patterns)

#     for index, text_pattern in enumerate(text_patterns):
#         (arg_name, arg_type) = text_pattern

#         # 拼接正则，所有文字参数，应该都是空格分格的
#         if index != arg_count - 1:
#             regex += r"(\S+)\s*"
#         else:
#             regex += r"(\S+)"

#         # logger.debug(pformat(arg_type))

#     # logger.debug(pformat(regex, segment.content))
#     match = re.search(regex, segment.content)
#     if not match:
#         raise PatternFormatError(f"pattern匹配失败-->正则失败")

#     texts = match.groups()
#     # logger.debug(pformat(texts))

#     if len(texts) != arg_count:
#         raise PatternFormatError(f"未按照格式提供参数 参数之间使用空格分隔")

#     return texts


async def downgrade_segment_to_str(
    segments: List[T_SegmentInstance], protocol: T_BotProtocol
) -> str:
    """将MessageChain中的所有Segment，downgrade为str

    1. json
    无法做到无损压缩，而且得给每一种segment重新建立一个映射关系，太麻烦了
    {
        "type": segment.__class__.__name__,
        "protocol": protocol,
        "data": json_segment,
    }

    2. pickle
    2a)
    cannot pickle 'Image' object: a class that defines __slots__ without defining __getstate__ cannot be pickled with protocol 0

    2b)
    pickle化的str，不管用什么编码，都有可能会产生空格，会导致argparse的解析问题
    所以，传递pickle str，似乎也不太方便

    result += " " + codecs.encode(pickle.dumps(segment), "base64").decode("ascii")

    3. 外部缓存
    需要及时删除，不然会占用内存

    """
    result = ""

    for segment in segments:
        if isinstance(segment, Text):
            result += segment.content

        else:
            segment_id = str(uuid4())

            command_arguments_cache[segment_id] = segment

            # 搞成这样，是为了用户意外传入了类似的格式
            # 需要手动加一个空格，不然str化的segment，会连在一起
            result += " " + DOWNGRADE_PATTERN_FORMAT.format(
                type_=segment.__class__.__name__,
                id_=segment_id,
            )

    return result


WRONG_TYPE_MESSAGE = """参数 {match_name} 类型错误，应为 {supposed_type} 类型，而你提供的是 {real_type}"""


def upgrade_str_to_segment(
    match_name: str, supposed_type: T_SegmentClass, argument: str
) -> T_SegmentInstance:
    """将str，upgrade为segment"""

    match = re.match(DOWNGRADE_PATTERN, argument)
    if not match:
        if supposed_type == Text:
            return Text(argument)

        # 应该是框架问题，用户一般不会遇到这个问题
        raise PatternFormatError(f"解析参数 {match_name} 失败，参数格式错误")

    segment_type: str = match.group(1)
    segment_id: str = match.group(2)

    segment = command_arguments_cache[segment_id]

    # TODO 定期检查，确保缓存的segment都删除了
    # 可以在删除command_status的时候，一起删
    # 或者干脆，就把这个存到command_status里面去
    del command_arguments_cache[segment_id]

    real_type = type(segment)  # segment.__class__

    if supposed_type != real_type:
        raise PatternFormatError(
            WRONG_TYPE_MESSAGE.format(
                match_name=match_name,
                supposed_type=supposed_type,
                real_type=real_type,
            )
        )

    return segment


def convert_base_type(
    match_name: str,
    supposed_type: T_ValidTextTypeClass,
    argument: str,
):
    # 有可能给这里传递segment，需要判断
    match = re.match(DOWNGRADE_PATTERN, argument)
    if match:
        segment_type: str = match.group(1)
        raise PatternFormatError(
            WRONG_TYPE_MESSAGE.format(
                match_name=match_name,
                supposed_type=supposed_type,
                real_type=segment_type,
            )
        )

    result: T_ValidTextTypeInstance

    if supposed_type == str:
        result = argument

    if supposed_type == bool:
        if not (argument in TRUE_TEXTS or argument in FALSE_TEXTS):
            raise PatternFormatError(
                WRONG_TYPE_MESSAGE.format(
                    match_name=match_name,
                    supposed_type=supposed_type,
                    real_type="不能代表 bool 的字符",
                )
            )

        else:
            if argument in TRUE_TEXTS:
                result = True
            else:
                result = False

    else:  # 解析int, float
        try:
            result = supposed_type(argument)  # type:ignore

        except Exception as e:
            raise PatternFormatError(
                WRONG_TYPE_MESSAGE.format(
                    match_name=match_name,
                    supposed_type=supposed_type,
                    real_type=f"不能转换为 {supposed_type} 的字符",
                )
            )

    return result


def convert_any(argument: str) -> Any:
    """将str，upgrade为segment"""

    match = re.match(DOWNGRADE_PATTERN, argument)
    if not match:
        return argument

    segment_type: str = match.group(1)
    segment_id: str = match.group(2)

    segment = command_arguments_cache[segment_id]
    del command_arguments_cache[segment_id]

    return segment


def type_converter_factory(
    match_name: str, element_type: T_PatternArgClass, container_type: Union[List, None]
) -> Callable:
    """optional已经处理过了，这里不要考虑Optional

    - [x] Any == str or segment
    - [x] str, int, float, bool
    - [x] MessageSegment
    - [x] List[str]
    - [ ] Union[str, segment]
    - [ ] List[Union]
    - [ ] 不允许Union[List, other(str)]
    - [ ] 支持set、tuple
    """

    if element_type in get_args(T_SegmentInstance):
        converter = partial(
            upgrade_str_to_segment,
            match_name,
            cast(T_SegmentClass, element_type),
        )

    elif element_type is Any:
        converter = convert_any

    # 无法处理的类型，之前已经检查过了，这里一定都是可以处理的
    else:
        converter = partial(
            convert_base_type,
            match_name,
            cast(T_ValidTextTypeClass, element_type),
        )

    return converter


def construct_sub_command_help_message(
    command_name: str, pattern_args: OrderedDict[str, _PatternArg]
) -> str:
    return f"Usage: {command_name} [OPTIONS] [ARGS]..."


def construct_root_command_help_message(
    command_name: str,
    root_node: CommandNode,
    command_method_mapping: Dict[str, ClassCommandMethodCache],
) -> str:
    """针对根command，帮助信息包含其所有的sub command，树形展示"""

    return f"Usage: {command_name}{':'+root_node.name if root_node.name != 'initial' else ''} [OPTIONS] [ARGS]..."


def add_arguments(parser: ArgumentParser, method: Callable):
    # signature可以获取到被装饰器装饰过的函数的真实参数签名
    signature = inspect.signature(method)

    # debug(signature.parameters)

    pattern_args: OrderedDict[str, _PatternArg] = OrderedDict()

    for arg_name, p in signature.parameters.items():
        if not isinstance(p.default, TemporaryPatternArg):
            continue

        required = False
        has_default = p.default.kwargs.get("default", None) is not None
        set_optional = False

        # is list == nargs='+'
        container_type = get_origin(p.annotation)  # None，如果没有
        element_types = get_args(p.annotation)  # 如果没有容器，则为空tuple

        # debug(element_types)
        if not element_types:
            element_type = p.annotation
        else:
            # 只支持单个元素的容器，目前不支持Union
            # 如果是Optional，None是第二个参数
            element_type = element_types[0]

        if container_type is Union and type(None) in element_types:
            set_optional = True

        # debug(container_type, element_type)
        # debug(get_origin(element_type))
        # debug(get_args(element_type))
        # debug(arg_name, p)
        # debug(p.annotation)
        # debug(p.annotation in PATTERN_ARG_TYPES)
        # debug(PATTERN_ARG_TYPES)
        if element_type not in PATTERN_ARG_TYPES:
            if element_type is Any:
                pass

            # TODO List,list Set,set
            elif get_origin(element_type) in (List, list):  # Optional[List[str]]
                container_type = list
                element_type = get_args(element_type)[0]

            else:
                raise InitializationError(f"仅支持str, bool, int, float和所有消息类型")

        # debug(container_type, element_type)

        if not set_optional and not has_default:
            required = True

        kwargs = {}

        match_names: List[str] = []
        if p.default.cls == "CLIOption":
            kwargs["dest"] = arg_name

            if set_name := p.default.kwargs.get("name"):
                match_names.append(f"--{set_name}")
            else:
                match_names.append(f"--{arg_name}")

            if short_name := p.default.kwargs.get("short_name"):
                match_names.append(f"-{short_name}")
        else:
            # ValueError: dest supplied twice for positional argument
            # https://stackoverflow.com/questions/41446760
            # add_argument(dest, ..., name=value, ...)
            # add_argument(option_string, option_string, ..., name=value, ...)

            match_names.append(arg_name)

        if container_type in (list, tuple, set):
            multiple = True
        else:
            multiple = False

        if required:
            if multiple:
                kwargs["nargs"] = "+"
            else:
                kwargs["nargs"] = 1
        else:
            if multiple:
                kwargs["nargs"] = "*"
            else:
                kwargs["nargs"] = "?"

        # debug(set_optional, required, kwargs)

        type_converter = type_converter_factory(
            match_names[0], element_type, container_type  # type: ignore
        )

        # TODO 默认值，callable
        parser.add_argument(
            *match_names,
            type=type_converter,
            **kwargs,
        )

        pattern_arg = _PatternArg(
            type_=p.annotation,
            default=p.default.kwargs.get("default", None),
            required=required,
            help_message=p.default.kwargs.get("help", None),
            is_option=p.default.cls == "CLIOption",
            name=match_names[0],
            short_name=p.default.kwargs.get("short_name", None),
            multiple=multiple,
        )

        pattern_args[arg_name] = pattern_arg

    return pattern_args


def get_command_stack(node: CommandNode):
    stack: List[str] = []

    while node:
        stack.append(node.name)
        node = node.parent  # type: ignore

    return stack[::-1]


def build_sub_parsers_for_single_node(
    node: CommandNode,
    parser_handles: Dict[str, _SubParsersAction],
    parsers: Dict[str, ArgumentParser],
    relations_cache: Dict[str, SubCommandRelation],
    command_name: str,
    class_command_cache: ClassCommandCache,
    command_method_mapping: Dict[str, ClassCommandMethodCache],
    root_parser: ArgumentParser,
):
    method_name = node.name

    # 判断是几级command，如果是第一级，那么就是main_parser，如果是第二级，那么就是sub_parser
    # 都需要保证，上一级的sub parser，已经存在
    if not node.parent:  # initial
        parser = root_parser
        command_final_name = method_name

    else:
        sub_command_relation = relations_cache[method_name]
        command_final_name = sub_command_relation["command_final_name"]

        parent_command_name = node.parent.name
        handle = parser_handles[parent_command_name]
        parser = handle.add_parser(command_final_name, add_help=False)

    parsers[method_name] = parser  # 用不到

    # add_parser时，用final_name，但是判断具体是要调用哪个method时，还是用method_name
    parser.set_defaults(**{f"{ARGPARSE_CALLED_METHOD}": method_name})

    # 默认都实现--help
    parser.add_argument(
        "--help",
        "-h",
        action=CustomHelpAction,
        nargs=0,
    )

    class_command_method_cache = command_method_mapping[method_name]
    method = class_command_method_cache.method

    pattern_args = add_arguments(parser, method)

    class_command_method_cache.pattern_args = pattern_args

    if not node.parent:
        help_message = construct_root_command_help_message(
            command_name, node, command_method_mapping
        )

    else:
        help_message = construct_sub_command_help_message(
            command_final_name, pattern_args
        )

    class_command_method_cache.help_message = help_message
    class_command_method_cache.command_stack = get_command_stack(node)
    class_command_method_cache.is_root = node.parent is None

    if not node.parent:
        class_command_method_cache.parser = parser

    class_command_cache.method_name_parser_mapping[method_name] = root_parser

    # 有sub_command再创建，不然，无法实现multi positional arguments，会直接尝试解析sub command
    if node.children:
        # 需要在add_subparser之前，先把所有的argument都添加进去
        # 先加参数，再加sub_command也不行，因为sub_command的本质，就是一个可选的位置参数，argparse无法解析
        handle = parser.add_subparsers(required=False)
        parser_handles[method_name] = handle

        for child in node.children:
            build_sub_parsers_for_single_node(
                child,
                parser_handles,
                parsers,
                relations_cache,
                command_name,
                class_command_cache,
                command_method_mapping,
                root_parser,
            )


def build_sub_parsers_for_multi_nodes(
    root_nodes: List[CommandNode],
    parser_handles: Dict[str, _SubParsersAction],
    parsers: Dict[str, ArgumentParser],
    relations_cache: Dict[str, SubCommandRelation],
    command_name: str,
    class_command_cache: ClassCommandCache,
    command_method_mapping: Dict[str, ClassCommandMethodCache],
):
    """
    一个指令中，允许多个top parser

    虽然实现多个top parser，但是只是为了，让非initial、非sub_command的method，也能使用命令行参数

    对于nest command，一个指令还是只建议实现一个，否则会很难维护

    """

    for root_node in root_nodes:
        root_parser = CustomArgumentParser(
            prog=f"{command_name}_{root_node.name}",
            add_help=False,
        )

        build_sub_parsers_for_single_node(
            root_node,
            parser_handles,
            parsers,
            relations_cache,
            command_name,
            class_command_cache,
            command_method_mapping,
            root_parser,
        )


# def get_pattern_results(
#     compressed_patterns: List[
#         Union[List[Tuple[str, GT_PatternArg]], Tuple[str, GT_PatternArg]]
#     ],
#     compressed_segments: List[T_SegmentInstance],
# ):
#     pattern_result: OrderedDict[str, T_PatternArgInstance] = OrderedDict()

#     for index, (segment, pattern) in enumerate(
#         zip(compressed_segments, compressed_patterns)
#     ):
#         # logger.debug(pformat(type(segment)))
#         # logger.debug(pformat(type(chunk)))

#         if isinstance(segment, Text):
#             if not isinstance(pattern, list):  # 所有text都被解析为list[(arg_name, arg_type)]
#                 raise PatternFormatError("未按照格式提供参数")

#             text_patterns = cast(List[Tuple[str, T_ValidTextTypeClass]], pattern)
#             texts = match_by_regex(text_patterns, segment)

#             for index, text_without_type in enumerate(texts):
#                 arg_name, arg_type = text_patterns[index]

#                 pattern_result[arg_name] = convert_base_type(
#                     arg_name,
#                     arg_type,
#                     text_without_type,
#                 )

#         # todo 支持pydantic的Field，比如gt,lt,对输出的报错信息，转为PatternFormatError
#         # 最好能找到，pydantic中是怎么使用ModelField进行字段验证的，只是使用就好了
#         # snap: int = Field(
#         #     42,
#         #     title="The Snap",
#         #     description="this is the value of snap",
#         #     gt=30,
#         #     lt=50,
#         # )

#         # 支持pydantic的validate装饰器
#         # for arg_name, validators in command_pattern.__validators__.items():
#         #     for validator in validators:
#         #         validator.func(command_pattern.__class__, pattern_result[arg_name])

#         else:  # 检测是否是有效类型，Face，Image之类
#             pattern = cast(Tuple[str, GT_PatternArg], pattern)
#             arg_name, arg_type = pattern

#             if type(segment) != arg_type:
#                 raise PatternFormatError(f"未按照格式提供参数 {arg_name} 应为 {arg_type} 类型")

#             pattern_result[arg_name] = segment

#     return pattern_result


# def pattern_config(
#     with_format_hint: bool = True,
#     on_format_error: Optional[
#         Callable[[T_CompressedSegments, T_CompressedPatterns], str]
#     ] = None,
#     retry: int = 3,
# ):
#     """装饰器，函数粒度的config"""
#     PATTERN_CONFIG = "__pattern_config__"
#     pass


async def parse_pattern(
    event_metadata: EventMetadata,
    class_command_cache: ClassCommandCache,
    cache: ClassCommandMethodCache,
    method_name: str,
    command_kwargs: Dict[str, Any],
    command_name: str,
    status: ClassCommandStatus,
):
    """
    根据签名中的PatternArg，自动解析参数，并转换为对应类型，自动注入函数调用中

    满足pattern放行，如果不满足，会对方法调用进行拦截，拦截的意思就是，不update pointer
    应该通过抛出异常，来立即结束执行，这个不应该被catch生命周期捕获

    如果存在sub command，会直接调用该sub command对应的method

    - 先使用argparse，解析纯str形式的参数
    - 再将segment还原为对应的类型，并检查类型是否一致
    """

    chain: MessageChain = command_kwargs["chain"]
    sender: "CommandSender" = command_kwargs["sender"]
    prefix: str = command_kwargs["prefix"]
    alias: str = command_kwargs["alias"]
    context: Dict = command_kwargs["context"]

    # TODO 性能优化
    # if not cache.compressed_patterns:
    #     return method_name,{}

    # 需要根据当前的method_name，判断用哪个parser来解析
    parser = class_command_cache.method_name_parser_mapping[method_name]

    # message_chain转为str(json.dumps，不带空格)，去掉prefix
    prefix_with_alias = prefix + alias
    # compressed_segments = merge_adjacent_text_segments(chain.segments)
    chain_str = await downgrade_segment_to_str(chain.segments, event_metadata.protocol)
    without_prefix = chain_str.replace(prefix_with_alias, "", 1).strip()

    # debug(chain_str)
    # debug(without_prefix)

    splitted_args = without_prefix.split()

    try:
        # args = parser.parse_args(splitted_args)
        args, unknown_args = parser.parse_known_args(splitted_args)

        args_dict = vars(args)

        # debug(args_dict)

        # 考虑到alias(command_final_name)的问题
        target_method = args_dict[ARGPARSE_CALLED_METHOD]

        # 即使只有单个结果，只要设置了nargs，返回的也是list，需要处理一下
        # optional(nargs=?)时，返回的不是list

        # 对于sub sub command来说，每一级command的参数都需要处理
        class_method_cache = class_command_cache.command_method_mapping[target_method]
        for stack_name in class_method_cache.command_stack:
            stack_cache = class_command_cache.command_method_mapping[stack_name]

            for arg_name, pattern_arg_info in stack_cache.pattern_args.items():
                # debug(pattern_arg_info)

                # argparse会将optional的参数，设置为None
                if arg_name in args_dict and args_dict[arg_name] is not None:
                    if not pattern_arg_info.multiple:
                        if isinstance(args_dict[arg_name], list):
                            args_dict[arg_name] = args_dict[arg_name][0]

                if arg_name not in args_dict or args_dict[arg_name] is None:
                    if pattern_arg_info.default:
                        try:
                            if callable(pattern_arg_info.default):
                                args_dict[arg_name] = await await_or_sync(
                                    pattern_arg_info.default
                                )
                            else:
                                # TODO 动态默认值复用的问题
                                args_dict[arg_name] = pattern_arg_info.default

                        except Exception as e:
                            raise PatternFormatError(f"无法设置参数 {arg_name} 的默认值，{e}")

        # debug(args_dict)
        context["cli_arguments"] = {**args_dict}
        # debug(context)

        return target_method, args_dict

    except PatternFormatError as exception:
        if ARGPARSE_HELP == exception.args[0]:
            # -h不应该使命令进入running
            # 这个可以直接in 判断，因为不需要知道是不是子任务的，只需要知道有没有-h
            status.running = False
            await status.update()

            # 根据target_method，获取对应的help message
            # debug(exception.args)
            kwargs = exception.args[1]
            namespace = kwargs["namespace"]
            target_method = getattr(namespace, ARGPARSE_CALLED_METHOD)

            class_method_cache = class_command_cache.command_method_mapping[
                target_method
            ]
            help_message = class_method_cache.help_message or ""

            await sender.send_message(Text(f"{help_message}"))

        else:
            # 参数不足 /gpt
            # the following arguments are required: test

            # 参数过多 /gpt 123 456
            # unrecognized arguments: 456

            # 参数过多 + sub_parsers /gpt 123 456
            # invalid choice: '456' (choose from )

            # error似乎没法获取到__call_command__

            class_method_cache = class_command_cache.command_method_mapping["initial"]
            help_message = class_method_cache.help_message or ""

            await sender.send_message(Text(f"参数解析失败: {exception}\n" + help_message))

        raise exception

    # try:
    #     compressed_segments = merge_text_of_segments(chain.segments)
    #     debug_log(compressed_segments)

    #     if len(compressed_segments) != len(compressed_patterns):
    #         raise PatternFormatError(
    #             f"未提供足够参数，应为{len(cache.patterns)}个，" + f"获得{len(chain.segments)}个"
    #         )

    #     # 对initial应用pattern的情况，支持prefix
    #     # 目前仅支持文字prefix
    #     if method_name == "initial":
    #         if not isinstance(compressed_segments[0], Text):
    #             return PatternFormatError("目前仅支持文字前缀")

    #         with_prefix = compressed_segments[0].content
    #         without_prefix = re.sub(f"^{prefix}", "", with_prefix)
    #         compressed_segments[0].content = without_prefix

    #     results = get_pattern_results(compressed_patterns, compressed_segments)

    # except PatternFormatError as e:
    #     # if on_format_error:
    #     #     return_text = await await_or_normal(
    #     #         on_format_error, *args, **kwargs
    #     #     )
    #     #     if return_text:
    #     #         await bot.group_msg(return_text)
    #     # else:
    #     await sender.send_message(
    #         # Text(f"{e}\n{formot_hint if with_formot_hint else ''}")
    #         Text(f"{e}\n{format_hint}")
    #     )

    #     logger.error("指令解析失败")
    #     raise e  # 需要中断指令的执行
