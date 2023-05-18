from collections import defaultdict
from inspect import isclass
from typing import (
    TYPE_CHECKING,
    Any,
    Awaitable,
    Callable,
    Dict,
    Iterable,
    List,
    Literal,
    Optional,
    Set,
    Tuple,
    Union,
    cast,
)

from pydantic import BaseModel, Field
from pyrogram.client import Client
from rich import print as rich_print
from rich.tree import Tree
from typing_extensions import NotRequired

from pepperbot.core.api.api_caller import ApiCaller
from pepperbot.exceptions import InitializationError
from pepperbot.store.command import ClassCommandCache, ClassCommandConfigCache
from pepperbot.types import (
    BOT_PROTOCOLS,
    CONVERSATION_TYPES,
    BaseBot,
    BaseClassCommand,
    T_BotProtocol,
    T_ConversationType,
    T_HandlerType,
    T_RouteRelation,
    T_RouteValidator,
)

if TYPE_CHECKING:
    from pepperbot.core.message.segment import T_SegmentInstance

import sys

if sys.version_info < (3, 11):
    from typing_extensions import TypedDict
else:
    from typing import TypedDict


class BotRoute(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    handlers: Optional[Iterable[object]] = None
    commands: Optional[Iterable[BaseClassCommand]] = None
    groups: Optional[T_RouteRelation] = None  # 默认不应该匹配所有
    friends: Optional[T_RouteRelation] = None


def register(
    *,
    handlers: Optional[Iterable[object]] = None,
    commands: Optional[Iterable[BaseClassCommand]] = None,
    # 这个可以匹配所有，因为仅建议仅有单个handler时使用，用户一般也不会做太复杂的权限控制
    groups: Optional[T_RouteRelation] = None,
    friends: Optional[T_RouteRelation] = None,
    # **kwargs, # 不允许用户传入其他参数
):
    """装饰器风格，实现注册handler和command"""

    def decorator(handler: Callable):
        if not isclass(handler):
            raise InitializationError(
                "register装饰器只能注册class handler，不能注册function handler"
            )

        # 收集register中的BotRoute，apply_routes中应用
        register_routes.append(
            # 通过BotRoute，实现参数的类型检查
            BotRoute(
                handlers=handlers,
                commands=commands,
                groups=groups,
                friends=friends,
            )
        )

        return handler

    return decorator


T_AvailableChecker = Callable[..., Union[bool, Awaitable[bool]]]


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


class ApiCallerTypeMap(TypedDict):
    onebot: NotRequired[ApiCaller]
    keaimao: NotRequired[ApiCaller]
    telegram: NotRequired[Client]


class BotInfo(BaseModel):
    """保存每个协议的bot的自身信息
    id
    是否是管理员之类
    """

    class Config:
        arbitrary_types_allowed = True

    id: int
    is_admin: bool


"""每个worker进程都需要独立进行的初始化工作"""


register_routes: List[BotRoute] = []
""" 通过register装饰器注册的class_handler """

route_mapping: Dict[
    Tuple[
        Union[T_BotProtocol, Literal["validator"]],
        T_ConversationType,
        str,
        T_HandlerType,
    ],
    Set[str],
] = defaultdict(set)
""" 路由映射

一个class_handler可能对应多个群，所以只保存class_handler的名字，而不是实例化的对象
用的时候，通过名字，从class_handler_mapping中获取实例化的对象

统一保存为str，这样不用判断是int还是str了

qq号可能和群号重复，通过conversation_type区分

这里是protocol-group，而不是group-protocol，是因为
每次接收到消息，protocol是固定的，而group、private不固定
这样的顺序符合逻辑

{
    ( "onebot", "group", "123456789", "class_handlers" ) : [ "class_handler_name" ],
    ( "onebot", "group", "123456789", "class_commands" ) : [ "class_command_name" ],
    ( "onebot", "private", "123456789", "class_handlers" ) : [ "class_handler_name" ],
    ( "onebot", "private", "123456789", "class_commands" ) : [ "class_command_name" ],
    ( "validator", "group", "__unset__", "class_handlers" ) : [ "class_handler_name" ],
    ( "validator", "group", "__unset__", "class_commands" ) : [ "class_command_name" ],
}

"""

# 下方都为缓存
class_handler_mapping: Dict[str, ClassHandlerCache] = {}
""" ClassHandler.__name__ : ClassHandlerCache """

route_validator_mapping: Dict[str, T_RouteValidator] = {}
""" ValidatorFunction.__name__ : route_validator """

class_command_mapping: Dict[str, ClassCommandCache] = {}
""" ClassCommand.__name__ : ClassHandlerCache """

class_command_config_mapping: Dict[str, ClassCommandConfigCache] = {}
""" 一个command可能有多个config，解耦class_instance和config，复用class_command_cache，不然要重复创建多次

之所以是config_id作为key，是因为在route_mapping中，直接保存的是config_id
{
    [command_config_id] : ClassCommandConfigCache(
        class_command_name = "class_command_name",
        command_config = CommandConfig,
    )
}
"""

CLASS_CHECKERS = "__class_checkers__"

checkers_cache: Dict[Tuple[str, str], Set[T_AvailableChecker]] = defaultdict(set)
""" 应用available时，无法判断是否是command，所以不放在对应的cache里，单独建一个 
{
    ("class.__name__", CLASS_CHECKERS) : set(checker),
    ("class.__name__", "method.__name__") : set(checker),
}
"""


class SubCommandRelation(TypedDict):
    parent_method_name: Optional[str]
    """ 没有父指令时的情况 """
    command_final_name: str
    """ 如何设置了alias，这里就是alias，否则就是command_name """


command_relations_cache: Dict[str, Dict[str, SubCommandRelation]] = defaultdict(dict)
""" 保存command的子指令关系，用于检查指令是否存在

{
    "command_name" : {
        "sub_command_name" : SubCommandRelation(
            parent_method_name = "parent_method_name",
            command_final_name = "command_final_name",
        ),
    },
}
 """

command_arguments_cache: Dict[str, "T_SegmentInstance"] = {}
""" 解决pickle的问题 """

api_callers: ApiCallerTypeMap = {}

bot_info: Dict[T_BotProtocol, Dict] = defaultdict(dict)
""" 保存每个协议的bot的自身信息
id
是否是管理员之类
"""


bot_instances: Dict[
    Tuple[Union[T_BotProtocol, Literal["universal"]], T_ConversationType, str],
    BaseBot,
] = {}
""" 为每一个消息来源构造一个bot实例的开销是完全可以接受的(即使有三四千个) 
{
    ("universal", "group", identifier) : bot,
    ("onebot", "private", identifier) : bot,
}
"""


class OnebotEventMeta(BaseModel):
    has_skip_buffered_event = False
    buffered_message_count = 0


onebot_event_meta = OnebotEventMeta()


LAST_ONEBOT_HEARTBEAT_TIME = "last_onebot_heartbeat_time"


def get_bot_id(protocol: T_BotProtocol):
    return str(bot_info[protocol]["bot_id"])


async def initial_bot_info():
    """数据会保存至数据库，所以所有worker中，只需要执行一次"""

    for protocol in api_callers:
        if protocol == "onebot":
            if not bot_info.get("onebot"):
                from pepperbot.adapters.onebot.api import OnebotV11API

                bot_id = (await OnebotV11API.get_login_info())["user_id"]
                bot_info["onebot"]["bot_id"] = str(bot_id)

        elif protocol == "keaimao":
            if not bot_info.get("keaimao"):
                from pepperbot.adapters.keaimao.api import KeaimaoAPI

                accounts = cast(List, await KeaimaoAPI.get_login_accounts())
                bot_id = accounts[0]["wxid"]
                bot_info["keaimao"]["bot_id"] = bot_id

        elif protocol == "telegram":
            if not bot_info.get("telegram"):
                # from pepperbot.adapters.telegram.api import TelegramApi
                client = get_telegram_caller()

                me = await client.get_me()
                bot_id = str(me.id)
                bot_info["telegram"]["bot_id"] = bot_id

        else:
            raise InitializationError(f"未知的协议: {protocol}")


def clean_bot_instances():
    """每24小时清理一次，释放内存"""
    bot_instances.clear()


# api_callers: Dict[T_BotProtocol, ApiCaller] = {}


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


def get_route_chinese(route_mode: T_ConversationType) -> str:
    if route_mode == "group":
        route_name = "群"
    elif route_mode == "private":
        route_name = "好友"
    else:
        route_name = "频道"

    return route_name


def filter_route_mapping(
    protocol: Optional[T_BotProtocol] = None,
    conversation_type: Optional[T_ConversationType] = None,
    conversation_id: Optional[str] = None,
    handler_type: Optional[T_HandlerType] = None,
):
    for p, ct, cid, ht in route_mapping.keys():
        if protocol and p != protocol:
            continue
        if conversation_type and ct != conversation_type:
            continue
        if conversation_id and cid != conversation_id:
            continue
        if handler_type and ht != handler_type:
            continue

        yield (p, ct, cid, ht)


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

    for protocol in BOT_PROTOCOLS:
        protocol_tree = tree.add(protocol)

        for conversation_type in CONVERSATION_TYPES:
            route_name = get_route_chinese(conversation_type)

            (p, ct, cid, ht) = filter_route_mapping(
                protocol=protocol,
                conversation_type=conversation_type,
                conversation_id="__global__",
                handler_type="class_commands",
            )
            if global_commands:
                global_commands_tree = protocol_tree.add(f"全局{route_name}指令")
                for command_name in global_commands:
                    global_commands_tree.add(command_name)

            commands = filter_route_mapping(
                protocol=protocol,
                conversation_type=conversation_type,
                handler_type="class_commands",
            )
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

            global_handlers = global_handlers[protocol][conversation_type]
            if global_handlers:
                global_handlers_tree = protocol_tree.add(f"全局{route_name}响应器")
                for handler_name in global_handlers:
                    global_handlers_tree.add(handler_name)

            handlers = mapping[protocol][conversation_type]
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

    for conversation_type in CONVERSATION_TYPES:
        route_name = get_route_chinese(conversation_type)

        validators = mapping["validators"][conversation_type]
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
