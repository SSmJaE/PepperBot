from typing import Iterable, List

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

        command_names: List[str] = []
        for command in commands:
            command_name = command.__name__

            if not is_valid_class_command(command):
                raise InitializationError(f"路由 {route} 中的指令 {command_name} 不符合要求")

            if command_name not in class_command_mapping.keys():
                # cache_class_command(command, command_name)
                pass

            command_names.append(command_name)

        handler_name: str = ""
        # todo 多handler的情况, handlers=[]
        if route.handler:
            handler_name = route.handler.__name__

            if not is_valid_class_handler(route.handler):
                raise InitializationError(f"路由 {route} 中的消息响应器 {handler_name} 不符合要求")

            if handler_name not in class_handler_mapping.keys():
                cache_class_handler(route.handler, handler_name)
                # pass

        # pydantic会校验不合法的情况，所以不用else
        if route.groups == "*":
            for protocol in ALL_AVAILABLE_BOT_PROTOCOLS:
                for command_name in command_names:
                    route_mapping.global_commands["group"].add(command_name)

                if route.handler:
                    route_mapping.global_handlers[protocol]["group"].add(handler_name)

        elif route.groups and type(route.groups) == dict:
            for protocol, group_ids in route.groups.items():
                if group_ids == "*":
                    if route.handler:
                        route_mapping.global_handlers[protocol]["group"].add(
                            handler_name
                        )

                else:
                    for group_id in group_ids:
                        group_id = str(group_id)

                        for command_name in command_names:
                            route_mapping.mapping[protocol]["group"][group_id][
                                "commands"
                            ].add(command_name)

                        if route.handler:
                            route_mapping.mapping[protocol]["group"][group_id][
                                "class_handlers"
                            ].add(handler_name)

        elif callable(route.groups):
            validator = route.groups

            if not is_valid_route_validator(validator):
                raise InitializationError(f"路由{route}中的groups的validator不符合要求")

            validator_name = validator.__name__
            if validator_name not in route_validator_mapping.keys():
                cache_route_validator(validator, validator_name)
                # pass

            for command_name in command_names:
                route_mapping.mapping["validators"]["group"][validator_name][
                    "commands"
                ].add(command_name)

            if route.handler:
                route_mapping.mapping["validators"]["group"][validator_name][
                    "class_handlers"
                ].add(handler_name)

        if route.friends == "*":
            for protocol in ALL_AVAILABLE_BOT_PROTOCOLS:
                for command_name in command_names:
                    route_mapping.global_commands["private"].add(command_name)

                if route.handler:
                    route_mapping.global_handlers[protocol]["private"].add(handler_name)

        elif route.friends and type(route.friends) == dict:
            for protocol, private_ids in route.friends.items():
                if private_ids == "*":
                    if route.handler:
                        route_mapping.global_handlers[protocol]["private"].add(
                            handler_name
                        )

                else:
                    for private_id in private_ids:
                        private_id = str(private_id)

                        for command_name in command_names:
                            route_mapping.mapping[protocol]["private"][private_id][
                                "commands"
                            ].add(command_name)

                        if route.handler:
                            route_mapping.mapping[protocol]["private"][private_id][
                                "class_handlers"
                            ].add(handler_name)

        elif callable(route.friends):
            validator = route.friends

            if not is_valid_route_validator(validator):
                raise InitializationError(f"路由{route}中的friends的validator不符合要求")

            validator_name = validator.__name__
            if validator_name not in route_validator_mapping.keys():
                cache_route_validator(validator, validator_name)

            for command_name in command_names:
                route_mapping.mapping["validators"]["private"][validator_name][
                    "commands"
                ].add(command_name)

            if route.handler:
                route_mapping.mapping["validators"]["private"][validator_name][
                    "class_handlers"
                ].add(handler_name)
