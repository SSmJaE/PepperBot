from typing import Any, Iterable, List, Literal, Set, Type, TypeVar

from devtools import debug

from pepperbot.core.route.cache import (
    cache_class_command,
    cache_class_command_config,
    cache_class_handler,
    cache_route_validator,
)
from pepperbot.core.route.validate import (
    is_valid_class_command,
    is_valid_class_handler,
    is_valid_route_validator,
)
from pepperbot.exceptions import InitializationError
from pepperbot.store.command import ClassCommandConfigCache, CommandConfig
from pepperbot.store.meta import (
    BotRoute,
    class_command_config_mapping,
    class_command_mapping,
    class_handler_mapping,
    route_mapping,
    route_validator_mapping,
)
from pepperbot.types import (
    BOT_PROTOCOLS,
    COMMAND_CONFIG,
    BaseClassCommand,
    T_ConversationType,
)


def parse_routes(routes: Iterable[BotRoute]):
    for route in routes:
        commands: Iterable[BaseClassCommand] = []
        if route.commands:
            commands = route.commands

        command_config_ids: Set[str] = set()
        """ 需要知道config_id和command_name的对应关系 
        
        (command_name, config_id)
        """

        for command in commands:
            # 直接.__name__，不要.__class__.__name__，因为后者会返回type
            command_name = command.__name__  # type: ignore

            if not is_valid_class_command(command):
                raise InitializationError(f"路由 {route} 中的指令 {command_name} 不符合要求")

            # class command的class本身，和command对应的config，解耦了，需要分别缓存
            # command config后续通过map_by_conversation_type进行缓存
            # class command直接在这里缓存，只需要缓存一次
            if command_name not in class_command_mapping.keys():
                cache_class_command(command, command_name)

            # 上方已经验证该字段一定存在
            command_config_dict: dict[str, CommandConfig] = getattr(
                command, COMMAND_CONFIG
            )

            for command_config_id, command_config in command_config_dict.items():
                if command_config_id not in class_command_config_mapping.keys():
                    cache_class_command_config(command_name, command_config)

                command_config_ids.add(command_config_id)

        handler_names: Set[str] = set()
        if route.handlers:
            for handler in route.handlers:
                # 目前都是class handler，后续可能支持function handler
                handler_name = handler.__name__  # type: ignore

                if not is_valid_class_handler(handler):
                    raise InitializationError(
                        f"路由 {route} 中的消息响应器 {handler_name} 不符合要求"
                    )

                if handler_name not in class_handler_mapping.keys():
                    cache_class_handler(handler, handler_name)

                handler_names.add(handler_name)

        map_by_conversation_type(
            route, "group", route.groups, command_config_ids, handler_names
        )
        map_by_conversation_type(
            route, "private", route.friends, command_config_ids, handler_names
        )


def map_by_conversation_type(
    route: BotRoute,
    conversation_type: T_ConversationType,
    conversation_definition: Any,
    command_config_ids: Set[str],
    handler_names: Set[str],
):
    if conversation_definition == "*":
        for protocol in BOT_PROTOCOLS:
            route_mapping[
                (
                    protocol,
                    conversation_type,
                    "__global__",
                    "class_commands",
                )
            ] |= command_config_ids
            route_mapping[
                (
                    protocol,
                    conversation_type,
                    "__global__",
                    "class_handlers",
                )
            ] |= handler_names

    elif conversation_definition and type(conversation_definition) == dict:
        for protocol, conversation_keys in conversation_definition.items():
            if conversation_keys == "*":
                route_mapping[
                    (
                        protocol,
                        conversation_type,
                        "__global__",
                        "class_commands",
                    )
                ] |= command_config_ids
                route_mapping[
                    (
                        protocol,
                        conversation_type,
                        "__global__",
                        "class_handlers",
                    )
                ] |= handler_names

            else:
                for conversation_key in conversation_keys:
                    conversation_key = str(conversation_key)

                    route_mapping[
                        (
                            protocol,
                            conversation_type,
                            conversation_key,
                            "class_commands",
                        )
                    ] |= command_config_ids
                    route_mapping[
                        (
                            protocol,
                            conversation_type,
                            conversation_key,
                            "class_handlers",
                        )
                    ] |= handler_names

    elif callable(conversation_definition):
        validator = conversation_definition

        if not is_valid_route_validator(validator):
            raise InitializationError(f"路由{route}中的{conversation_type}的validator不符合要求")

        validator_name = validator.__name__
        if validator_name not in route_validator_mapping.keys():
            cache_route_validator(validator, validator_name)

        route_mapping[
            (
                "validator",
                conversation_type,
                "__unset__",
                "class_commands",
            )
        ] |= command_config_ids
        route_mapping[
            (
                "validator",
                conversation_type,
                "__unset__",
                "class_handlers",
            )
        ] |= handler_names
