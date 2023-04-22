from __future__ import annotations
from collections import deque
import pickle

import time
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
    for type_ in get_args(GT_PatternArg):
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


# TODO 带默认值的pattern
def PatternArg(default: Optional[GT_PatternArg] = None) -> GT_PatternArg:
    return cast(GT_PatternArg, "PatternArg")
    # return cast(GT_PatternArg, default)


# a: Image = PatternArg()


# class PatternArg(Generic[GT_PatternArg]):
#     """ """

#     __slots__ = (
#         "type_",
#         "default",
#     )

#     def __init__(
#         self, type_: Type[GT_PatternArg], default: Optional[GT_PatternArg] = None
#     ):
#         self.type_ = type_
#         self.default = default


# a = PatternArg(Image, Image(""))


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
    patterns: List[Tuple[str, T_PatternArgInstance]]
    compressed_patterns: T_CompressedPatterns
    """ cache时缓存便于正则的格式化的pattern，不用每次收到消息都解析 """


class ClassCommandCache(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    class_instance: Any
    command_method_mapping: Dict[str, ClassCommandMethodCache] = {}
    """ key为方法名，value为实例化后的方法 """


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
