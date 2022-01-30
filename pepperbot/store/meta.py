from collections import defaultdict
from typing import (
    Any,
    Callable,
    Dict,
    Iterable,
    List,
    Literal,
    Optional,
    Sequence,
    Set,
    Tuple,
    Type,
    Union,
)
from typing_extensions import Annotated

from pydantic import BaseModel, Field
from pepperbot.core.bot.api_caller import ApiCaller
from pepperbot.exceptions import InitializationError
from pepperbot.utils.common import deepawait_or_sync, fit_kwargs


from pepperbot.types import (
    BaseBot,
    BaseClassCommand,
    T_BotProtocol,
    T_RouteRelation,
    T_RouteMode,
    T_RouteValidator,
    T_WebProtocol,
)


class BotRoute(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    handler: Optional[Callable] = None
    commands: Optional[Iterable[Callable]] = None
    groups: Optional[T_RouteRelation] = "*"
    friends: Optional[T_RouteRelation] = "*"


class ClassHandlerCache(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    class_instance: Any
    """ 实例化(单例)的类消息响应器 """
    event_handlers: Dict[str, Callable] = Field(default_factory=dict)
    """ 检查过合法性的事件响应器, bounded methods
    这里不需要保存handler的名字，而是直接保存handler
    因为handler适合class绑定的，class已经缓存过了 
    {
        "group_message" : bounded_handler,
        "add_group" : bounded_handler,
    }
    """


class ClassCommandCache(BaseModel):
    class Config:
        arbitrary_types_allowed = True


class RouteValidatorCache(BaseModel):
    class Config:
        arbitrary_types_allowed = True


class RouteMapping(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    global_commands: Dict[T_RouteMode, Set[str]] = defaultdict(set)
    """ 对所有群应用的指令，当groups="*"时注册至此 """
    """ 对所有私聊消息应用的指令，当friends="*"时注册至此 """

    global_handlers: Dict[T_BotProtocol, Dict[T_RouteMode, Set[str]]] = defaultdict(
        lambda: defaultdict(set)
    )
    """ 对所有群应用的消息响应器，当groups="*"或者friends="*"时注册至此 
    {
        "onebot" : {
            "group" : [handler1, handler2, ],
            "friend" : []
            "channel" : []
        }
    }
    """
    mapping: Dict[
        Union[T_BotProtocol, Literal["validators"]],
        Dict[
            T_RouteMode,
            Dict[
                str,
                Dict[Literal["class_handlers", "commands"], Set[str]],
            ],
        ],
    ] = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(set))))
    """ 
    一个群消息响应器可能对应多个群，所以只保存索引
    同意保存为str，这样不用判断是int还是str了
    qq号可能和群号重复，再套一级字典
    这里是protocol-group，而不是group-protocol，是因为
    每次接收到消息，protocol是固定的，而group、private不固定
    这样的顺序符合逻辑

    mapping可以不需要group private，减少一级嵌套，通过添加标识符，比如private123，
    减少一级嵌套，不意味不区分GroupBot和PrivateBot
    protocol还是要区分的
    之所以现在有group、private，是因为认为群号和qq号可能重复，事实上可以通过标识符避免
    比如g_123 == group 123, p_123 == private 123, c_123 == channel 123
    "group" : {
        123 : {

        }
    }
    还是
    "g_123" :{

    }
    其实真差不多，多一级的话，还有类型提示

    {
        "onebot":{
            "group" : {
                12345 : { 
                    class_handlers : [ClassHandlerCacheName],
                    commands : [CommandClassName],
                },
            },
            "private" : {
                "67890" : { 
                    class_handlers : [ClassHandlerCacheName],
                    commands : [CommandClassName],
                }
            }
        },
        "validators" : {
            "group" : {
                [validator_name] : {
                    class_handlers : [],
                    commands : [],
                },
            }
        }
    }
    """

    bot_instances: Dict[
        Tuple[Union[T_BotProtocol, Literal["universal"]], T_RouteMode, str],
        BaseBot,
    ] = Field(default_factory=dict)
    """ 为每一个消息来源构造一个bot实例的开销是完全可以接受的(即使有三四千个) 
    {
        ("universal", "group", identifier) : bot,
        ("onebot", "private", identifier) : bot,
    }
    """

    bot_info: Dict[T_BotProtocol, Dict] = defaultdict(dict)
    """ 保存每个协议的bot的自身信息
    id
    是否是管理员之类
    """


def get_bot_info(protocol: T_BotProtocol):
    raise InitializationError(f"未能获取{protocol}的bot自身信息")
    return {}


def get_bot_id(protocol: T_BotProtocol):
    return route_mapping.bot_info[protocol]["bot_id"]


def clean_bot_instances():
    """每24小时清理一次，释放内存"""
    route_mapping.bot_instances.clear()


class LifecycleHandler(BaseModel):
    """函数形式的生命周期响应器"""

    pass


lifecycle_handlers = defaultdict(list)


class_handler_mapping: Dict[str, ClassHandlerCache] = {}
""" ClassHandler.__name__ : ClassHandlerCache """

route_validator_mapping: Dict[str, T_RouteValidator] = {}

route_mapping = RouteMapping()

api_callers: Dict[T_BotProtocol, ApiCaller] = {}

register_routes: List[BotRoute] = []
""" 通过register装饰器注册的class_handler """


class BotMetaState(BaseModel):
    router = {}
    class_handlers = {}
    function_handlers = {}
    commands = {}


bot_meta_state = BotMetaState()


def cache_command_class(command_class: object):
    if command_class not in bot_meta_state.commands:
        bot_meta_state.commands[command_class.__class__] = command_class


def get_api_caller(protocol: T_BotProtocol):
    api_caller = api_callers.get(protocol)
    
    assert api_caller, f"无法获取 {protocol} 对应的api_caller，请确保你注册了对应的adapter"

    return api_caller

def get_onebot_caller():
    return get_api_caller("onebot")


def get_keaimao_caller():
    return get_api_caller("keaimao")


def get_telegram_caller():
    return get_api_caller("telegram")


cached_group_ids = []


# def split_cached_mapping_for_performance():
#     for key, item in route_mapping.mapping.items():
#         if key in handler_validator_mapping.keys():
#             pass
#         elif key.startswith("private"):
#             pass
#         else:
#             pass


def has_class_handler(source_id: Union[int, str]):
    return source_id in cached_group_ids


def has_commands(source_id: Union[int, str]):
    pass


def has_validator():
    pass


DEFAULT_URI = {
    "onebot": "/onebot",
    "keaimao": "/keaimao",
}


ALL_AVAILABLE_BOT_PROTOCOLS: Iterable[T_BotProtocol] = ["onebot", "keaimao"]


class EventHandlerKwarg(BaseModel):
    name: str
    type_: Any
    value: Any
    """ 
    value可以为嵌套协程，会自动await直到不可await，以获取结果 
    也可以为函数，自动call到un callable，
    协程嵌套同步函数再嵌套协程也没有问题
    """


async def get_event_handler_kwargs(
    mapping: Dict[str, List[EventHandlerKwarg]],
    event_name: str,
    *,
    default_kwargs: List[EventHandlerKwarg] = None,
    **injected_kwargs: Annotated[Any, "必须提供bot和raw_event"],
):
    kwarg_list: List[EventHandlerKwarg] = mapping.get(event_name, default_kwargs or [])

    kwargs: Dict[str, Any] = {}
    for kwarg in kwarg_list:
        kwargs[kwarg.name] = await deepawait_or_sync(
            kwarg.value,
            **fit_kwargs(kwarg.value, injected_kwargs),
        )

    return kwargs


T_HandlerKwargMapping = Dict[str, List[EventHandlerKwarg]]
