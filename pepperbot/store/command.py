from __future__ import annotations

import time
from collections import defaultdict, deque
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Dict,
    List,
    Literal,
    Sequence,
    Set,
    Tuple,
    Type,
    Union,
)

from devtools import debug

# if TYPE_CHECKING:
from pepperbot.core.message.segment import T_SegmentClass, T_SegmentInstance
from pepperbot.types import (
    BaseClassCommand,
    T_BotProtocol,
    T_RouteMode,
    T_RouteRelation,
)
from pydantic import BaseModel, Field
from typing_extensions import TypedDict, get_args


class CommandConfig(BaseModel):
    need_prefix: bool = False
    prefixes: Sequence[str] = ["/"]
    """ 都是正则，自动加上^ """
    aliases: Sequence[str] = Field(default_factory=list)
    """ 指令前缀别名 ，都是正则 """
    include_class_name: bool = True
    """ 类名本身是否作为指令前缀 """
    exit_patterns: Sequence[str] = ["^/exit", "^退出"]
    """ 都是正则，满足条件， """
    require_at: bool = False
    """ 是否需要@机器人 """
    timeout: int = 30
    """ 会话超时时间，单位秒, """
    history_size: int = 0
    # lock_user = False
    # """ 跨消息渠道锁定用户
    # 不管他是私聊、还是群聊、还是频道，只要是一条规则指定的用户，他们的发言都会被指令接受
    # """
    # user_mapping: List[Dict[T_BotProtocol, str]] = Field(default_factory=list)
    # """
    # 用户自己负责，是否有重复指定的情况
    # 如果重复指定了两次，那么就会执行两次
    # [
    #     {
    #         "onebot" : "123455",
    #         "keaimao" : "wxid_askjhfljdsaf",
    #     },
    #     {
    #         "onebot" : "7890784",
    #         "keaimao" : "wxid_xnvkjdhf",
    #     },
    # ]
    # """
    # lock_source = False
    # """
    # 指定消息来源，该消息来源(群、频道)内，所有用户的发言都被指令接受
    # 不要和lock_user同时使用，二选一
    # 也就是说，normal, lock_user, lock_source是三选一的关系
    # """
    # source_mapping: List[Dict[T_BotProtocol, List[str]]] = Field(default_factory=list)
    # """
    # [
    #     {
    #         "onebot" : ["123455", "2034789"],
    #         "keaimao" : ["123789@chatroom",],
    #     },
    # ]
    # """


T_PatternArg = Union[Type[str], Type[int], Type[float], Type[bool], T_SegmentClass]
T_PatternArgResult = Union[str, int, float, bool, T_SegmentInstance]


def get_runtime_pattern_arg_types():
    runtime_generic_types = []
    for type_ in get_args(T_PatternArg):

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


runtime_pattern_arg_types = get_runtime_pattern_arg_types()

# class PatternArg:
#     # pass
#     # __slots__ = ("type_",)

#     def __init__(self):
#         # self.type_ = type_

#         return 123


def PatternArg() -> Any:
    return "PatternArg"


T_CompressedPatterns = List[
    Union[List[Tuple[str, T_PatternArg]], Tuple[str, T_PatternArg]]
]


class CommandMethodCache(BaseModel):
    method: Callable
    patterns: List[Tuple[str, T_PatternArg]]
    compressed_patterns: T_CompressedPatterns
    """ cache时缓存便于正则的格式化的pattern，不用每次收到消息都解析 """


# CommandMethodCache.update_forward_refs()


class ClassCommandCache(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    class_instance: Any
    command_method_mapping: Dict[str, CommandMethodCache] = {}
    """ key为方法名，value为实例化后的方法 """
    # command_config: Dict[str, Any]
    # lock_user_context_ids: Set[str] = set()
    """ 
    允许在BotRoute中，对同一个command设置多个不同的kwargs组合
    [id1, id2, id3]

    for id in ids:
        if meet_lock_user_rule()
    """
    # lock_source_context_ids


class_command_mapping: Dict[str, ClassCommandCache] = {}
""" ClassCommand.__name__ : ClassHandlerCache """


class_command_config_mapping: Dict[str, Dict[str, CommandConfig]] = defaultdict(dict)
""" 一个command可能有多个config，share_state_command时，复用class_command_cache，
解耦class_instance和config，不然要重复创建多次
default是给BotRoute中注册的command用的
{
    [command_name] : {
        "default" : CommandConfig,
        "id1" : CommandConfig,
        "id2" : CommandConfig,
    }
}
 """

COMMAND_CONFIG = "__command_config__"


class HistoryItem(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    raw_event: Dict


class ClassCommandStatus(BaseModel):
    """也可以理解为一个session"""

    pointer: str = "initial"
    history: deque
    last_updated_time: float = Field(default_factory=time.time)
    """ 用来判断timeout """
    context: Dict = Field(default_factory=dict)
    """ 用户定义，method之间的消息传递方式 """


T_CommandStatusKey = Tuple[str, T_BotProtocol, T_RouteMode, str]

normal_command_context_mapping: Dict[T_CommandStatusKey, ClassCommandStatus] = {}
""" 
默认情况，不锁定用户，也不锁定消息来源
{
    (command_name, protocol, mode, source_id) : status
}
"""


# class LockRelation(TypedDict):
#     rule: Dict[T_BotProtocol, List[str]]
#     context: ClassCommandContext


# lock_user_context_mapping: Dict[str, LockRelation] = {}
"""
锁定用户
lock_user_mapping中的每一条规则，都应该有一个单独的context

{
    id : {
        rule : {},
        context : context
    }
}

"""
