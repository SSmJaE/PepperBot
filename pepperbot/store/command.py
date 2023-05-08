from __future__ import annotations

import pickle
import re
import time
from argparse import ArgumentParser
from collections import OrderedDict, deque
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Dict,
    Generic,
    List,
    Literal,
    Optional,
    Sequence,
    Tuple,
    Type,
    TypeVar,
    Union,
    cast,
)
from uuid import uuid4

import ormar
from pydantic import BaseModel, Field
from typing_extensions import get_args

# if TYPE_CHECKING:
# field "chain" not yet prepared so type is still a ForwardRef, you might need to call HistoryItem.update_forward_refs().
# pydantic需要用到
from pepperbot.core.message.chain import MessageChain
from pepperbot.core.message.segment import (
    GT_PatternArg,
    Image,
    T_SegmentClass,
    T_SegmentInstance,
)
from pepperbot.store.orm import database, metadata
from pepperbot.types import T_BotProtocol

TRUE_TEXTS = ("True", "true", "1")
FALSE_TEXTS = ("False", "false", "0")

VALID_TEXT_TYPES = (str, int, float, bool)
T_ValidTextTypeInstance = Union[str, int, float, bool]
T_ValidTextTypeClass = Union[Type[str], Type[int], Type[float], Type[bool]]

T_PatternArgInstance = Union[T_ValidTextTypeInstance, T_SegmentInstance]
T_PatternArgClass = Union[T_ValidTextTypeClass, T_SegmentClass]


def get_runtime_pattern_arg_types():
    """获取运行时的T_PatternArg的类型，基础类型 + 所有Segment类型"""

    runtime_generic_types = []
    for type_ in get_args(T_PatternArgClass):
        if type_ is Union:  # T_SegmentClass
            runtime_generic_types.extend(get_args(type_))

        else:  # str, bool, int, float
            runtime_generic_types.append(type_)

    # debug(runtime_generic_types)
    runtime_class_types = tuple(
        map(lambda generic: get_args(generic)[0], runtime_generic_types)
    )
    # debug(runtime_class_types)
    return runtime_class_types


PATTERN_ARG_TYPES = get_runtime_pattern_arg_types()
""" 运行时的GT_PatternArg的类型，基础类型 + 所有Segment类型 """

ARGPARSE_HELP = "__help__"

ARGPARSE_CALLED_METHOD = "__called_method__"


class _PatternArg(BaseModel):
    """主要用来生成help信息"""

    type_: Any
    default: Optional[Any] = None
    required: bool = False
    """ 根据type==Optional + default判断 """
    help_message: Optional[str] = None
    is_option: bool = False
    """ 根据是CLIArgument还是CLIOption判断 """
    name: str
    """ 如果是argument，就是参数名
     
    如果是option，如果用户提供了name，就是name，不然就是参数名
    """
    short_name: Optional[str] = None
    multiple: bool = False
    """ 根据type==List判断 """


class TemporaryPatternArg:
    def __init__(
        self,
        cls: Literal["CLIArgument", "CLIOption"],
        kwargs: Dict[str, Any],
    ):
        self.cls = cls
        self.kwargs = kwargs


# T_OptionalMultiplePatternArg = Optional[Union[GT_PatternArg, List[GT_PatternArg]]]
# 不能抽出来，会失去类型推导能力？


# GT_PatternArgOrList = TypeVar("GT_PatternArgOrList", GT_PatternArg, List[GT_PatternArg])


def CLIArgument(
    default: Optional[Union[GT_PatternArg, List[GT_PatternArg]]] = None,
    help: Optional[str] = None,
) -> GT_PatternArg:
    # 这里只是为了IDE的类型提示，并不关心返回值是什么，也用不上
    # 是直接通过AST的方式，生成_PatternArg
    # 直接用AST有点麻烦，用inspect.signature
    return cast(GT_PatternArg, TemporaryPatternArg("CLIArgument", locals()))


# class CLIArgument(Generic[GT_PatternArg]):
#     def __new__(
#         cls,
#         *,
#         default: Optional[GT_PatternArg] = None,
#         help: Optional[str] = None,
#     ):
#         return cast(GT_PatternArg, _PatternArg)


# 这两种方式(用函数，或者__new__)基本都一样，用函数的开销小一点，虽然都可以忽略不计
# 唯一区别是，不提供default时，如果是class的形式，如果GT_PatternArg设置了default(TypeVar)，如果参数的类型和default不一致，会报错
# 而如果是函数的形式，则可以自动根据参数的类型推断default的类型，所以不会报错，也不用设置TypeVar中的default
# https://peps.python.org/pep-0696/
# 3.12才支持给TypeVar设置default

# a: str = CLIArgument(default=Image(""))
# a: Image = CLIArgument(default=Image(""))
# a: int = CLIArgument()  # 无默认值时，泛型如何处理


def CLIOption(
    *,
    default: Optional[Union[GT_PatternArg, List[GT_PatternArg]]] = None,
    help: Optional[str] = None,
    name: Optional[str] = None,
    short_name: Optional[str] = None,
):
    return cast(GT_PatternArg, TemporaryPatternArg("CLIOption", locals()))


def uuid_str() -> str:
    return str(uuid4())


T_InteractiveStrategy = Literal[
    "same_source_same_user",
    "same_source_any_user",
    "any_source_same_user",
    "any_source_any_user",
]


class CommandConfig(BaseModel):
    """pydantic可以自动处理动态默认值的问题

    动态默认值问题是指，如果默认值是[]、{}，则会被复用，导致多个指令共享同一个默认值对象(因为是同一个对象)
    也就是说，修改会在多个指令间同步
    """

    config_id: str = Field(default_factory=uuid_str)

    need_prefix: bool = False
    prefixes: Sequence[str] = ["/"]
    aliases: Sequence[str] = Field(default_factory=list)
    include_class_name: bool = True
    exit_patterns: Sequence[str] = ["^/exit", "^退出"]
    require_at: bool = False
    timeout: int = 60
    history_size: int = 1
    interactive_strategy: T_InteractiveStrategy = "any_source_same_user"
    config: Any = None
    concurrency: bool = True
    priority: int = 0
    propagation_group: str = "default"


T_CompressedPatterns = List[
    Union[List[Tuple[str, GT_PatternArg]], Tuple[str, GT_PatternArg]]
]


class ClassCommandMethodCache(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    method: Callable
    pattern_args: OrderedDict[str, _PatternArg] = OrderedDict()
    help_message: Optional[str] = None
    """ sub command的help message """
    command_stack: List[str] = []
    """ 对于nest command来说，就是从initial => sub command => sub sub command的顺序，
    用于处理argparse的解析结果 """


class ClassCommandCache(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    class_instance: Any
    command_method_mapping: Dict[str, ClassCommandMethodCache] = {}
    """ key为方法名，value为实例化后的方法 """
    parser: ArgumentParser
    help_message: Optional[str] = None
    """ 存储help message，此处为总览"""


DOWNGRADE_PATTERN_FORMAT = "__{type_}:{id_}__"
DOWNGRADE_PATTERN = re.compile(r"__(\w+):(.*)__")


class ClassCommandConfigCache(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    class_command_name: str
    command_config: CommandConfig


class HistoryItem(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    raw_event: Dict
    chain: MessageChain


# MessageChain = ForwardRef('MessageChain')
# MessageChain.update_forward_refs()


class ClassCommandStatus(ormar.Model):
    """保存指令状态，跨进程"""

    class Meta:
        tablename = "class_command_status"
        database = database
        metadata = metadata

    id: int = cast(int, ormar.Integer(primary_key=True))

    command_name = cast(str, ormar.String(max_length=50))
    config_id: str = cast(str, ormar.String(max_length=50))
    protocol: T_BotProtocol = cast(T_BotProtocol, ormar.String(max_length=50))
    conversation_type: str = cast(str, ormar.String(max_length=50))
    conversation_id: str = cast(str, ormar.String(max_length=50))
    user_id: str = cast(str, ormar.String(max_length=50))

    pointer: str = cast(str, ormar.String(max_length=50, default="initial"))
    running: bool = ormar.Boolean(default=False)

    # 通过pickle序列化后的数据
    history: bytes = ormar.LargeBinary(
        max_length=100000, default=pickle.dumps(deque(maxlen=1))
    )
    context: bytes = ormar.LargeBinary(max_length=100000, default=pickle.dumps({}))

    """ 用户定义，method之间的消息传递方式 """
    last_updated_time: float = cast(float, ormar.Float(default=time.time))
    """ 用来判断timeout """
    timeout: int = cast(int, ormar.Integer())
