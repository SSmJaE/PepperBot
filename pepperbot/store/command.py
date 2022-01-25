from collections import defaultdict
from typing import Any, Callable, Dict, List, Literal, Union
from pydantic import BaseModel

from pepperbot.types import CommandClassBase


class UserMessage(BaseModel):
    messageId: int
    # message: List[SegmentInstance_T]
    createTime: int
    groupId: int
    userId: int

    class Config:
        arbitrary_types_allowed = True


class NormalContext(BaseModel):
    """
    默认不收录消息，除非触发了指令，减少内存占用
    """

    messageQueue: List[UserMessage] = []
    commandStatus: str = "initial"
    userContext: Dict = {}


class CommandContext(BaseModel):
    """
    如果相同的一条指令，需要为某些用户跨群，某些不跨群，应该怎么操作？
    复制一份，一个全局permission，另一个提供permission方法，实现动态用户黑名单/白名单
    """

    # todo 如果未提供，使用全局设置
    # 通过as_command的kwargs指定
    maxSize: int
    timeout: int

    """
    - normal        same user same group
    - crossUser     cross user same group 
    - crossGroup    same user cross group
    - global        cross user cross group
    """
    mode: Literal["normal", "crossUser", "crossGroup", "global"] = "normal"

    # 如果是normal指令，需要为一个用户在每个群都保存一个消息队列和指令进度
    # 第一个key为QQ号，第二个key为群号
    normalContextMap: Dict[int, Dict[int, NormalContext]] = defaultdict(dict)

    # crossGroup
    crossGroupMessageQueue: List[UserMessage] = []
    # key为qq号
    # 对于当前用户，他的指令执行到哪一步了
    crossGroupCommandStatus: Dict[int, NormalContext] = defaultdict(NormalContext)

    # crossUser
    crossUserMessageQueue: List[UserMessage] = []
    # key为群号
    crossUserCommandStatus: Dict[int, NormalContext] = defaultdict(NormalContext)

    # global
    globalMessageQueue: List[UserMessage] = []
    globalCommandStatus: str = "initial"
    globalContext: Dict = {}


# todo 多个命令，一致前缀，都执行？
class Context(BaseModel):
    """
    context主要是为一个用户和各个commandClass的交互服务

    以用户或者commandClass为key都可以，不过用户的数量可能要比命令多得多

    所以以命令类为key
    """

    # todo 相同commandClass，不同permission的处理
    cache: Dict[Callable, CommandContext] = {}
    # 全局默认栈深
    maxSize: int = 9
    # 全局默认消息过期时间，单位秒
    timeout: int = 1 * 60 * 60

    class Config:
        arbitrary_types_allowed = True


# todo 提供统一的api，允许用户设置各种全局变量的默认值
globalContext = Context()


class CommandCache(BaseModel):
    instance: Union[Callable, Any]
    # key为方法名，value为实例化后的方法
    methods: Dict[str, Union[Callable, Any]] = {}
    kwargs: Dict[str, Any]
    targetMethod: str = "initial"


class_command_mapping: Dict[str, CommandClassBase] = {}
""" ClassHandler.__name__ : ClassHandlerCache """
