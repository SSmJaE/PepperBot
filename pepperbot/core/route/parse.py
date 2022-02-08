from typing import Iterable, List, Set

from devtools import debug
from pepperbot.core.route.cache import (
    cache_class_command,
    cache_class_handler,
    cache_route_validator,
)
from pepperbot.core.route.validate import (
    is_valid_class_command,
    is_valid_class_handler,
    is_valid_route_validator,
)
from pepperbot.exceptions import InitializationError
from pepperbot.store.command import class_command_mapping
from pepperbot.store.meta import (
    ALL_AVAILABLE_BOT_PROTOCOLS,
    BotRoute,
    class_handler_mapping,
    route_mapping,
    route_validator_mapping,
)


def parse_routes(routes: Iterable[BotRoute]):
    for route in routes:

        commands = []
        if route.commands:
            commands = route.commands

        command_names: Set[str] = set()
        for command in commands:
            command_name = command.__name__

            if not is_valid_class_command(command):
                raise InitializationError(f"路由 {route} 中的指令 {command_name} 不符合要求")

            if command_name not in class_command_mapping.keys():
                # cache_class_command(command, command_name)
                pass

            command_names.add(command_name)

        handler_names: Set[str] = set()
        if route.handlers:
            for handler in route.handlers:
                handler_name = handler.__name__

                if not is_valid_class_handler(handler):
                    raise InitializationError(
                        f"路由 {route} 中的消息响应器 {handler_name} 不符合要求"
                    )

                if handler_name not in class_handler_mapping.keys():
                    cache_class_handler(handler, handler_name)

                handler_names.add(handler_name)

        # -------------------------------------------------------------------------------

        # pydantic会校验不合法的情况，所以不用else
        if route.groups == "*":
            for protocol in ALL_AVAILABLE_BOT_PROTOCOLS:
                route_mapping.global_commands[protocol]["group"] |= command_names
                route_mapping.global_handlers[protocol]["group"] |= handler_names

        elif route.groups and type(route.groups) == dict:
            for protocol, group_ids in route.groups.items():
                if group_ids == "*":
                    route_mapping.global_handlers[protocol]["group"] |= handler_names

                else:
                    for group_id in group_ids:
                        group_id = str(group_id)

                        route_mapping.mapping[protocol]["group"][group_id][
                            "commands"
                        ] |= command_names

                        route_mapping.mapping[protocol]["group"][group_id][
                            "class_handlers"
                        ] |= handler_names

        elif callable(route.groups):
            validator = route.groups

            if not is_valid_route_validator(validator):
                raise InitializationError(f"路由{route}中的groups的validator不符合要求")

            validator_name = validator.__name__
            if validator_name not in route_validator_mapping.keys():
                cache_route_validator(validator, validator_name)

            route_mapping.mapping["validators"]["group"][validator_name][
                "commands"
            ] |= command_names

            route_mapping.mapping["validators"]["group"][validator_name][
                "class_handlers"
            ] |= handler_names

        # -------------------------------------------------------------------------------

        if route.friends == "*":
            for protocol in ALL_AVAILABLE_BOT_PROTOCOLS:
                route_mapping.global_commands[protocol]["private"] |= command_names
                route_mapping.global_handlers[protocol]["private"] |= handler_names

        elif route.friends and type(route.friends) == dict:
            for protocol, private_ids in route.friends.items():
                if private_ids == "*":
                    route_mapping.global_handlers[protocol]["private"] |= handler_names

                else:
                    for private_id in private_ids:
                        private_id = str(private_id)

                        route_mapping.mapping[protocol]["private"][private_id][
                            "commands"
                        ] |= command_names

                        route_mapping.mapping[protocol]["private"][private_id][
                            "class_handlers"
                        ] |= handler_names

        elif callable(route.friends):
            validator = route.friends

            if not is_valid_route_validator(validator):
                raise InitializationError(f"路由{route}中的friends的validator不符合要求")

            validator_name = validator.__name__
            if validator_name not in route_validator_mapping.keys():
                cache_route_validator(validator, validator_name)

            route_mapping.mapping["validators"]["private"][validator_name][
                "commands"
            ] |= command_names

            route_mapping.mapping["validators"]["private"][validator_name][
                "class_handlers"
            ] |= handler_names
