from argparse import ArgumentParser
from typing import Callable, Dict, List

from devtools import debug

from pepperbot.extensions.command.handle import LIFECYCLE_WITHOUT_PATTERNS
from pepperbot.extensions.command.node import build_command_tree
from pepperbot.extensions.command.pattern import (
    build_sub_parsers_for_multi_nodes,
)
from pepperbot.store.command import (
    ClassCommandCache,
    ClassCommandConfigCache,
    ClassCommandMethodCache,
    CommandConfig,
)
from pepperbot.store.meta import (
    ClassHandlerCache,
    class_command_config_mapping,
    class_command_mapping,
    class_handler_mapping,
    command_relations_cache,
    route_validator_mapping,
)
from pepperbot.types import BaseClassCommand
from pepperbot.utils.common import get_own_methods

""" 
todo
如果未注册对应的适配器，而且类响应器中定义了事件响应
两种方法，忽略或者报错，可以设置
 """


def cache_class_handler(class_handler: object, handler_name: str):
    """在parse中，已经验证过class_handler的合法性，这里不再重复验证"""

    #  不要每次都创建实例，on/register监听器新增时建立一次保存起来即可
    class_handler_instance = class_handler()  # type: ignore

    # groupHandler可能有多个装饰器，比如register, withCommand
    # 先解析为与装饰器名称相关的缓存至groupMeta，
    # 解析完所有装饰器之后，再生成classHandlers.groupCache中的缓存
    # 生成缓存时，确保register的存在，不然报错(withCommand也可以向group中推送meta信息)
    # 这才是真正的meta，全局保存class和对应的meta，而不是绑定到class上，可能会涉及到bound和unbound的问题

    event_handlers: Dict[str, Callable] = {}

    # 初始化时，遍历生成缓存，不要每次接收到消息都去遍历
    for method in get_own_methods(class_handler_instance):
        method_name = method.__name__
        event_handlers[method_name] = method

    class_handler_mapping[handler_name] = ClassHandlerCache(
        class_instance=class_handler_instance,
        event_handlers=event_handlers,
    )
    # 是否可以只实例化一次botInstance？动态注入groupId
    # 似乎每个群一个bot，效果更好一点
    # 为每一个group，缓存一个GroupCommonBot
    # botInstance=construct_GroupCommonBot({"group_id": id}, cast(Any, None)),


def cache_class_command(class_command: BaseClassCommand, command_name: str):
    """同一个commandClass，就实例化一次"""

    class_command_instance = class_command()  # type: ignore

    command_method_mapping = {}

    with_pattern_methods = set()
    """ 可以有cli arguments的method """

    relations_cache = command_relations_cache[command_name]

    for method in get_own_methods(class_command_instance):
        method_name = method.__name__

        if method_name not in LIFECYCLE_WITHOUT_PATTERNS:
            with_pattern_methods.add(method_name)

        command_method_mapping[method_name] = ClassCommandMethodCache(method=method)

    parsers: Dict[str, ArgumentParser] = {}
    """ 这里放的是.add_subparsers.add_parser()返回的对象 """

    parser_handles = {}
    """ 这里放的是add_subparsers()返回的对象，而不是parser对象 """

    root_nodes = build_command_tree(relations_cache, with_pattern_methods)

    class_command_cache = ClassCommandCache(
        class_instance=class_command_instance,
        command_method_mapping=command_method_mapping,
    )

    build_sub_parsers_for_multi_nodes(
        root_nodes,
        parser_handles,
        parsers,
        relations_cache,
        command_name,
        class_command_cache,
        command_method_mapping,
    )

    # debug(parsers)
    # debug(parser_handles)

    class_command_mapping[command_name] = class_command_cache


def cache_class_command_config(command_name: str, command_config: CommandConfig):
    # TODO 验证一下
    # TODO 相关的文档，怎么避免意外创建多个command config
    class_command_config_mapping[command_config.config_id] = ClassCommandConfigCache(
        class_command_name=command_name,
        command_config=command_config,
    )


def cache_route_validator(validator: Callable, validator_name: str):
    route_validator_mapping[validator_name] = validator
