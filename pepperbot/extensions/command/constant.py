from typing import Any, Deque, Dict, Union

from pepperbot.core.message.chain import MessageChain
from pepperbot.extensions.command.sender import CommandSender
from pepperbot.store.command import HistoryItem
from pepperbot.store.event import EventHandlerKwarg
from pepperbot.types import T_StopPropagation

LIFECYCLE_WITHOUT_PATTERNS = ("exit", "timeout", "catch", "finish", "cleanup")
""" 这些生命周期不应支持pattern 

或者说，除了initial，其他的生命周期都不应该支持pattern

不允许直接return self.finish
"""


COMMAND_COMMON_KWARGS = (
    EventHandlerKwarg(name="raw_event", type_=Union[Dict, dict]),
    EventHandlerKwarg(name="chain", type_=MessageChain),
    EventHandlerKwarg(name="sender", type_=CommandSender),
    EventHandlerKwarg(name="history", type_=Deque[HistoryItem]),
    EventHandlerKwarg(name="context", type_=Union[Dict, dict]),
    EventHandlerKwarg(name="config", type_=Any),
    EventHandlerKwarg(name="stop_propagation", type_=T_StopPropagation),
    EventHandlerKwarg(name="prefix", type_=str),
    EventHandlerKwarg(name="alias", type_=str),
)

COMMAND_DEFAULT_KWARGS = {
    "initial": (*COMMAND_COMMON_KWARGS,),
    "exit": (*COMMAND_COMMON_KWARGS,),
    "timeout": (*COMMAND_COMMON_KWARGS,),
    "catch": (
        *COMMAND_COMMON_KWARGS,
        EventHandlerKwarg(name="exception", type_=Exception),
    ),
    "finish": (*COMMAND_COMMON_KWARGS,),
}
"""
用于检查用户定义的方法的参数的类型注解是否合法
也就是说，所有用户在对应方法中(比如initial)可用的参数及其类型，都应该出现在此处
这里并不需要像class_handler中一样，提供value，因为会在run_class_method中直接注入
 """
