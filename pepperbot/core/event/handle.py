from typing import Callable, Dict, List, Set
import json
from pepperbot.adapters.onebot import OnebotV11Adapter
from pepperbot.core.event.base import AdapaterBase
from pepperbot.core.event.universal import ALL_GROUP_EVENTS, ALL_META_EVENTS, ALL_PRIVATE_EVENTS, GROUP_COMMAND_TRIGGER_EVENTS, PRIVATE_COMMAND_TRIGGER_EVENTS
from pepperbot.exceptions import EventHandleError

from pepperbot.extensions.logger import logger
from pepperbot.store.meta import (
    route_mapping,
    class_handler_mapping,
    route_validator_mapping,
)
from pepperbot.types import T_BotProtocol, T_RouteModes


async def get_event_handler_kwargs(event_name: str, raw_event: Dict) -> Dict:
    get_kwargs: Callable
    final_event_name: str = event_name

    if event_name in ALL_UNIVERSAL_EVENTS:
        get_kwargs = get_universal_kwargs

    elif event_name in ALL_ONEBOTV11_EVENTS:
        get_kwargs = OnebotV11Adapter.get_kwargs
        final_event_name = event_name.replace("onebot_", "")

    elif event_name in ALL_KEAIMAO_EVENTS:
        get_kwargs = KeaimaoAdapter.get_kwargs
        final_event_name = event_name.replace("keaimao_", "")

    kwargs = await get_kwargs(final_event_name, raw_event=raw_event)

    return kwargs


async def run_class_handlers(
    class_handler_names: Set[str], event_name: str, raw_event: Dict
):
    kwargs = await get_event_handler_kwargs(event_name, raw_event)
    bot_instance = get_bot_instance(protocol, mode, identifier)

    for class_handler_name in class_handler_names:
        class_handler_cache = class_handler_mapping[class_handler_name]
        event_handler = class_handler_cache.event_handlers.get(event_name)
        if event_handler:
            await await_or_sync(event_handler, **fit_kwargs(event_handler, kwargs))


async def run_class_commands():
    pass


async def with_validators(mode: T_RouteModes, source_id: str):
    handlers: Set[str] = set()
    commands: Set[str] = set()

    for validator_name, validator_dict in route_mapping.mapping["validators"][
        mode
    ].items():
        validator = route_validator_mapping[validator_name]

        if await await_or_sync(validator, **{"mode": mode, "source_id": source_id}):
            handlers |= validator_dict["class_handlers"]
            handlers |= validator_dict["commands"]

    return handlers, commands


def get_source_id(protocol: T_BotProtocol, mode: T_RouteModes, raw_event: Dict) -> str:
    source_id: str

    if protocol == "onebot":
        if mode == "group":
            source_id = raw_event["group_id"]
        elif mode == "private":
            source_id = raw_event["sender_id"]

    elif protocol == "keaimao":
        if mode == "group":
            source_id = raw_event["sender"]
        elif mode == "private":
            source_id = raw_event["sender_id"]

    if not source_id:
        raise EventHandleError(f"未能获取source_id")

    return str(source_id)





async def handle_event(protocol: T_BotProtocol, adapter: AdapaterBase, raw_event: Dict):
    event_name: str = adapter.preprocess_event(raw_event)
    # logger.info(f"{adapter.__class__.__name__}事件 {event_name}")

    if event_name in ALL_META_EVENTS:
        # print(
        #     arrow.get(receive["time"])
        #     .to("Asia/Shanghai")
        #     .format("YYYY-MM-DD HH:mm:ss"),
        #     "心跳",
        # )
        # logger.info("心跳事件")
        return

    class_handler_names: Set[str] = set()
    # 对同一个消息来源，同一个class_handler也只应调用一次
    class_command_names: Set[str] = set()
    # 对同一个消息对象，在处理一次事件时
    # 在global_commands、mapping、validator中重复注册的指令应该只运行一次
    mode: T_RouteModes
    source_id: str
    command_trigger_events: List[str]

    if event_name in ALL_GROUP_EVENTS:
        mode = "group"
        source_id = get_source_id(protocol, mode, raw_event)
        command_trigger_events = GROUP_COMMAND_TRIGGER_EVENTS

    elif event_name in ALL_PRIVATE_EVENTS:
        mode = "private"
        source_id = get_source_id(protocol, mode, raw_event)
        command_trigger_events = PRIVATE_COMMAND_TRIGGER_EVENTS

    else:
        raise EventHandleError(f"无效事件{event_name}")

    validator_handlers, validator_commands = await with_validators(mode, source_id)

    if event_name in command_trigger_events:
        class_command_names |= route_mapping.global_commands[mode]
        class_command_names |= route_mapping.mapping[protocol][mode][source_id][
            "commands"
        ]
        class_command_names |= validator_commands

        # if class_command_names:
        # await run_class_commands(protocol, mode, raw_event, class_command_names)

    class_handler_names |= route_mapping.global_handlers[protocol][mode]
    class_handler_names |= route_mapping.mapping[protocol][mode][source_id][
        "class_handlers"
    ]
    class_handler_names |= validator_handlers

    # await run_class_handlers(protocol, mode, raw_event, event_name, class_handler_names)
