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

from pydantic import BaseModel, Field
from pepperbot.core.bot.api_caller import ApiCaller

# from pepperbot.store.meta import BotRoute
# from pepperbot.extensions.action import ApiCaller
# from pepperbot.initial import T_ApiCaller

from pepperbot.types import (
    CommandClassBase,
    T_BotProtocol,
    T_RouteGroups,
    T_RouteModes,
    T_RouteValidator,
    T_WebProtocol,
)


class BotRoute(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    handler: Optional[Callable] = None
    commands: Optional[Iterable[Callable]] = None
    groups: Optional[T_RouteGroups] = "*"
    friends: Optional[T_RouteGroups] = "*"


class ClassHandlerCache(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    class_instance: Any
    """ 实例化(单例)的类消息响应器 """
    event_handlers: Dict[str, List[Callable]] = defaultdict(list)
    """ 检查过合法性的事件响应器, bounded methods
    这里不需要保存handler的名字，而是直接保存handler
    因为handler适合class绑定的，class已经缓存过了 
    {
        "group_message" : [handler,],
        "add_group" : [ handler ],
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

    global_commands: Dict[T_RouteModes, Set[str]] = defaultdict(set)
    """ 对所有群应用的指令，当groups="*"时注册至此 """
    """ 对所有私聊消息应用的指令，当friends="*"时注册至此 """

    global_handlers: Dict[T_BotProtocol, Dict[T_RouteModes, Set[str]]] = defaultdict(
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
            T_RouteModes,
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
        Tuple[T_BotProtocol, Literal["group", "private"], str], Callable
    ] = Field(default_factory=dict)
    """ 为每一个消息来源构造一个bot实例的开销是完全可以接受的(即使有三四千个) """


def get_bot_instance(protocol: T_BotProtocol, mode: T_RouteModes, identifier: str):
    key = (protocol, mode, identifier)
    instances_dict = route_mapping.bot_instances

    # bot_instance: Callable
    # if key not in instances_dict:
    #     if mode == "group":
    #         bot_instance = construct_group_bot(*key)
    #     elif mode == "private":
    #         bot_instance = construct_private_bot(*key)

    #     instances_dict[key] = bot_instance

    # else:
    #     bot_instance = instances_dict[key]

    # return bot_instance


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


# def output_config():
#
# debug(classHandlers)
# # debug(globalContext)

# result = []
# for groupId, groupCacheList in classHandlers.groupCache.items():
#     buffer = []
#     for groupCache in groupCacheList:
#         buffer2 = []

#         # todo 应该反过来，根据事件，列出订阅的classHandler，也要提升至group等级
#         buffer2.append(
#             DisplayTree(
#                 name=f"事件",
#                 node=[method for method in groupCache.methods.keys()],
#             ),
#         )

#         # todo 提升至group等级，uniqueCommand
#         buffer2.append(
#             DisplayTree(
#                 name=f"指令",
#                 node=[
#                     commandClass.__name__
#                     for commandClass in groupCache.commandClasses
#                 ]
#                 or ["无"],
#             ),
#         )

#         buffer.append(
#             DisplayTree(
#                 name=f"{groupCache.instance.__class__}",
#                 node=[*buffer2],
#             ),
#         )

#     groupTree = DisplayTree(name=f"群{groupId}", node=[*buffer])
#     result.append(groupTree)

# print_tree(DisplayTree(name="PepperBot", node=result))


def onebot_caller():
    return api_callers["onebot"]


def keaimao_caller():
    return api_callers["keaimao"]


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


class AdapterBuffer(BaseModel):
    receive_protocol: T_WebProtocol
    uri: str
    request_handler: Callable
