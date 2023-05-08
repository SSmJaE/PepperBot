from enum import Enum
from typing import (
    Any,
    Callable,
    Dict,
    Generic,
    Iterable,
    Literal,
    Optional,
    Protocol,
    Tuple,
    Type,
    TypeVar,
    Union,
    get_args,
)


COMMAND_CONFIG = "__command_config__"
COMMAND_RELATIONS = "__command_relations__"
""" 存储子指令和父指令的关系

{
    "sub_command_real_name": {
        "parent_command_name": "",
        "sub_command_alias": "",
    }
}

"""


class BaseClassCommand:
    __command_config__: Dict[str, Any]


class BaseBot:
    pass


T = TypeVar("T")
F = TypeVar("F", bound=Callable[..., Any])


T_WebProtocol = Literal["http", "websocket"]

T_BotProtocol = Literal["onebot", "keaimao", "telegram"]
BOT_PROTOCOLS: Iterable[T_BotProtocol] = ["onebot", "keaimao", "telegram"]

T_ConversationType = Literal["private", "group", "channel"]
CONVERSATION_TYPES: Iterable[T_ConversationType] = ["group", "private", "channel"]

T_HandlerType = Literal["class_commands", "class_handlers"]

T_RouteValidator = Callable[[str, T_ConversationType, str, T_HandlerType], bool]
""" ( protocol, conversation_type, conversation_id, handler_type ) => accept

( "onebot", "group", "123456", "class_handlers" ) => True
 """

T_RouteRelation = Union[
    Literal["*"],
    Dict[T_BotProtocol, Union[Literal["*"], Iterable[str]]],
    T_RouteValidator,  # (平台，群号)
]
""" 
groups = "*"

groups = { "onebot": "*" }

groups = { "onebot": ["123456", "654321"] }

groups = onebot_group_validator
"""


T_DispatchHandler = Tuple[str, int, bool, T_HandlerType, str]
""" (propagation_group, priority, concurrency, "class_handlers", "config_id") """

T_StopPropagation = Callable[[], None]
