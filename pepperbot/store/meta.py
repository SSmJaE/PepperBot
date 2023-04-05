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
    TypedDict,
    Union,
    cast,
)

from pepperbot.core.bot.api_caller import ApiCaller
from pepperbot.exceptions import InitializationError
from pepperbot.types import (
    BaseBot,
    BaseClassCommand,
    T_BotProtocol,
    T_RouteMode,
    T_RouteRelation,
    T_RouteValidator,
    T_WebProtocol,
)
from pepperbot.utils.common import deepawait_or_sync, fit_kwargs
from pydantic import BaseModel, Field
from pyrogram.client import Client
from rich import print as rich_print
from rich.tree import Tree
from typing_extensions import Annotated, NotRequired


class BotRoute(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    handlers: Optional[Iterable[object]] = None
    commands: Optional[Iterable[BaseClassCommand]] = None
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


class RouteValidatorCache(BaseModel):
    class Config:
        arbitrary_types_allowed = True


class RouteMapping(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    global_commands: Dict[T_BotProtocol, Dict[T_RouteMode, Set[str]]] = defaultdict(
        lambda: defaultdict(set)
    )
    """ 
    对所有群应用的指令，当groups="*"时注册至此
    对所有私聊消息应用的指令，当friends="*"时注册至此
    {
        "onebot" : {
            "group" : [command1, command2, ],
            "friend" : []
            "channel" : []
        }
    }
    """

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

    has_initial = False


class OnebotEventMeta(BaseModel):
    has_skip_buffered_event = False
    buffered_message_count = 0


onebot_event_meta = OnebotEventMeta()


def get_bot_id(protocol: T_BotProtocol):
    return str(route_mapping.bot_info[protocol]["bot_id"])


async def initial_bot_info():
    for protocol in api_callers:
        if protocol == "onebot":
            if not route_mapping.bot_info.get("onebot"):
                from pepperbot.adapters.onebot.api import OnebotV11Api

                bot_id = (await OnebotV11Api.get_login_info())["user_id"]
                route_mapping.bot_info["onebot"]["bot_id"] = bot_id

        elif protocol == "keaimao":
            if not route_mapping.bot_info.get("keaimao"):
                from pepperbot.adapters.keaimao.api import KeaimaoApi

                bot_id = (await KeaimaoApi.get_login_accounts())[0]["wxid"]
                route_mapping.bot_info["keaimao"]["bot_id"] = bot_id

        elif protocol == "telegram":
            if not route_mapping.bot_info.get("telegram"):
                # from pepperbot.adapters.telegram.api import TelegramApi
                client = get_telegram_caller()

                me = await client.get_me()
                bot_id = str(me.id)
                route_mapping.bot_info["telegram"]["bot_id"] = bot_id

        else:
            raise InitializationError()


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


class ApiCallerTypeMap(TypedDict):
    onebot: NotRequired[ApiCaller]
    keaimao: NotRequired[ApiCaller]
    telegram: NotRequired[Client]


# api_callers: Dict[T_BotProtocol, ApiCaller] = {}
api_callers: ApiCallerTypeMap = {}

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


def get_onebot_caller() -> ApiCaller:
    return get_api_caller("onebot")


def get_keaimao_caller() -> ApiCaller:
    return get_api_caller("keaimao")


def get_telegram_caller() -> Client:
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
    "telegram": "/telegram",
}


ALL_AVAILABLE_BOT_PROTOCOLS: Iterable[T_BotProtocol] = ["onebot", "keaimao", "telegram"]
ALL_AVAILABLE_ROUTE_MODES: Iterable[T_RouteMode] = ["group", "private", "channel"]


class EventHandlerKwarg(BaseModel):
    name: str
    type_: Any
    value: Any
    """ 
    value可以为嵌套协程，会自动await直到不可await，以获取结果 

    也可以为函数，自动call到un callable，
    
    协程嵌套同步函数再嵌套协程也没有问题
    """


T_HandlerKwargMapping = Dict[str, List[EventHandlerKwarg]]


def get_route_chinese(route_mode: T_RouteMode) -> str:
    if route_mode == "group":
        route_name = "群"
    elif route_mode == "private":
        route_name = "好友"
    else:
        route_name = "频道"

    return route_name


def output_config():

    tree = Tree("协议适配")

    for protocol, api_caller in api_callers.items():
        caller_tree = tree.add(protocol)
        if protocol != "telegram":
            api_caller = cast(ApiCaller, api_caller)

            caller_tree.add(f"[green]API调用协议").add(api_caller.protocol)
            caller_tree.add(f"[green]API ip").add(api_caller.host)
            caller_tree.add(f"[green]API端口").add(str(api_caller.port))
        # else:

    rich_print(tree)

    tree = Tree("路由")

    for protocol in ALL_AVAILABLE_BOT_PROTOCOLS:
        protocol_tree = tree.add(protocol)

        for route_mode in ALL_AVAILABLE_ROUTE_MODES:
            route_name = get_route_chinese(route_mode)

            global_commands = route_mapping.global_commands[protocol][route_mode]
            if global_commands:
                global_commands_tree = protocol_tree.add(f"全局{route_name}指令")
                for command_name in global_commands:
                    global_commands_tree.add(command_name)

            commands = route_mapping.mapping[protocol][route_mode]
            if commands:
                commands_tree = None

                for source_id, cache in commands.items():
                    if not cache["commands"]:
                        continue
                    if not commands_tree:
                        commands_tree = protocol_tree.add(f"指定来源{route_name}指令")

                    source_id_tree = commands_tree.add(source_id)
                    for command_name in cache["commands"]:
                        source_id_tree.add(command_name)

            global_handlers = route_mapping.global_handlers[protocol][route_mode]
            if global_handlers:
                global_handlers_tree = protocol_tree.add(f"全局{route_name}响应器")
                for handler_name in global_handlers:
                    global_handlers_tree.add(handler_name)

            handlers = route_mapping.mapping[protocol][route_mode]
            if handlers:
                handlers_tree = None

                for source_id, cache in handlers.items():
                    if not cache["class_handlers"]:
                        continue

                    if not handlers_tree:
                        handlers_tree = protocol_tree.add(f"指定来源{route_name}响应器")

                    source_id_tree = handlers_tree.add(source_id)
                    for handler_name in cache["class_handlers"]:
                        source_id_tree.add(handler_name)

    for route_mode in ALL_AVAILABLE_ROUTE_MODES:
        route_name = get_route_chinese(route_mode)

        validators = route_mapping.mapping["validators"][route_mode]
        if not validators:
            continue

        validator_tree = tree.add("动态判断")

        for validator_name, cache in validators.items():
            if cache["commands"] or cache["class_handlers"]:
                current_node = validator_tree.add(f"validator {validator_name}")

                for command_name in cache["commands"]:
                    current_node.add(command_name)

                for handler_name in cache["class_handlers"]:
                    current_node.add(handler_name)

    rich_print(tree)

    # DisplayTree(
    #     name=f"事件",
    #     node=[method for method in groupCache.methods.keys()],
    # )


class EventMeta(BaseModel):
    protocol: T_BotProtocol
    mode: T_RouteMode
    source_id: str
    raw_event: Dict
    raw_event_name: str
    protocol_event_name: str
