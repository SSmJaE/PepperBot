import json
from typing import Any, Callable, Dict, List, Literal, Optional, Set, Union, cast

import arrow
from devtools import debug, pformat
from pepperbot.adapters.keaimao import KeaimaoAdapter
from pepperbot.adapters.keaimao.api import KeaimaoGroupBot, KeaimaoPrivateBot
from pepperbot.adapters.onebot import OnebotV11Adapter
from pepperbot.adapters.onebot.api import OnebotV11GroupBot, OnebotV11PrivateBot
from pepperbot.adapters.telegram import TelegramAdapter
from pepperbot.adapters.telegram.api import TelegramGroupBot, TelegramPrivateBot
from pepperbot.core.bot.universal import UniversalGroupBot, UniversalPrivateBot
from pepperbot.core.event.base_adapter import BaseAdapater
from pepperbot.core.event.kwargs import UNIVERSAL_KWARGS_MAPPING
from pepperbot.core.event.universal import (
    ALL_GROUP_EVENTS,
    ALL_META_EVENTS,
    ALL_PRIVATE_EVENTS,
    ALL_UNIVERSAL_EVENTS,
    GROUP_COMMAND_TRIGGER_EVENTS,
    PRIVATE_COMMAND_TRIGGER_EVENTS,
    UNIVERSAL_PROTOCOL_EVENT_MAPPING,
)
from pepperbot.core.event.utils import skip_current_onebot_event
from pepperbot.exceptions import EventHandleError
from pepperbot.extensions.command.handle import run_class_commands
from pepperbot.extensions.log import debug_log, logger
from pepperbot.store.meta import (
    EventHandlerKwarg,
    EventMeta,
    RouteMapping,
    T_HandlerKwargMapping,
    class_handler_mapping,
    get_bot_id,
    get_onebot_caller,
    initial_bot_info,
    onebot_event_meta,
    route_mapping,
    route_validator_mapping,
)
from pepperbot.types import BaseBot, T_BotProtocol, T_RouteMode
from pepperbot.utils.common import await_or_sync, deepawait_or_sync, fit_kwargs
from pyrogram.enums.chat_type import ChatType
from pyrogram.types import CallbackQuery, Message


async def handle_event(protocol: T_BotProtocol, raw_event: Dict):
    logger.info("-" * 50)

    if not route_mapping.has_initial:
        await initial_bot_info()
        logger.success("成功获取bot元信息")
        route_mapping.has_initial = True

    adapter = get_adapter(protocol)
    raw_event_name = adapter.get_event_name(raw_event)
    """ raw event without protocol prefix """
    protocol_event_name: str = f"{protocol}_" + raw_event_name
    """ raw event with protocol prefix """

    # go-cqhhtp will buffer outdated messages
    if protocol == "onebot":
        if not onebot_event_meta.has_skip_buffered_event:
            flag = skip_current_onebot_event(raw_event, raw_event_name)
            if not flag:
                return

    mode = adapter.get_route_mode(raw_event, raw_event_name)
    source_id = adapter.get_source_id(raw_event, mode)

    debug_log("", f"mode {mode} source_id {source_id}")

    if not (mode and source_id):
        raise EventHandleError(
            f"无效或尚未适配的事件 <lc>{protocol}</lc> 的事件 <lc>{raw_event_name}</lc>"
        )

    logger.info(
        f"接收到 <lc>{protocol}</lc> 的事件 <lc>{raw_event_name}</lc>，来自于 <lc>{mode}</lc> 模式的 <lc>{source_id}</lc>"
    )

    event_meta = EventMeta(
        protocol=protocol,
        mode=mode,
        source_id=source_id,
        raw_event=raw_event,
        raw_event_name=raw_event_name,
        protocol_event_name=protocol_event_name,
    )

    await dispatch_class_commands(event_meta)
    await dispatch_class_handlers(event_meta)


PROTOCOL_ADAPTER_MAPPING: Dict[T_BotProtocol, Any] = {
    "onebot": OnebotV11Adapter,
    "keaimao": KeaimaoAdapter,
    "telegram": TelegramAdapter,
}


def get_adapter(protocol: T_BotProtocol) -> BaseAdapater:
    return PROTOCOL_ADAPTER_MAPPING[protocol]


async def dispatch_class_commands(event_meta: EventMeta):
    mode = event_meta.mode
    protocol = event_meta.protocol
    source_id = event_meta.source_id

    command_trigger_events: List[str]

    if mode == "group":
        command_trigger_events = GROUP_COMMAND_TRIGGER_EVENTS
    elif mode == "private":
        command_trigger_events = PRIVATE_COMMAND_TRIGGER_EVENTS
    else:
        raise EventHandleError(f"")

    if not event_meta.protocol_event_name in command_trigger_events:
        logger.info(
            f"<lc>{protocol}</lc> 的事件 <lc>{event_meta.raw_event_name}</lc> 非指令触发事件"
        )
        return

    class_command_names: Set[str] = set()
    """ 在global_commands、mapping、validator中重复注册的指令应该只运行一次 """

    # 单一消息来源
    class_command_names |= route_mapping.global_commands[protocol][mode]
    class_command_names |= route_mapping.mapping[protocol][mode][source_id]["commands"]
    class_command_names |= await with_validators(mode, source_id, "commands")

    if not class_command_names:
        logger.info(f"<lc>{mode}</lc> 模式的 <lc>{source_id}</lc> 尚未注册指令")
        return

    logger.info(f"<lc>{mode}</lc> 模式的 <lc>{source_id}</lc> 存在注册的指令，开始执行")
    await run_class_commands(event_meta, class_command_names)

    # lock_user
    # for rule_id, rule in lock_user_mapping.items():
    #     if source_id in rule[protocol]:
    #         await run_class_command(mode="lock_user",rule_id)

    # if mode =="group" or mode =="channel":
    #     lock_source_mapping

    # lock_source


async def dispatch_class_handlers(event_meta: EventMeta):

    mode = event_meta.mode
    protocol = event_meta.protocol
    source_id = event_meta.source_id

    class_handler_names: Set[str] = set()
    """ 对同一个消息来源，在处理一次事件时,同一个class_handler也只应调用一次 """

    class_handler_names |= route_mapping.global_handlers[protocol][mode]
    class_handler_names |= route_mapping.mapping[protocol][mode][source_id][
        "class_handlers"
    ]
    class_handler_names |= await with_validators(mode, source_id, "commands")

    debug_log(class_handler_names, "所有可用class_handler")

    if not class_handler_names:
        logger.info(
            f"<lc>{event_meta.mode}</lc> 模式的 <lc>{event_meta.source_id}</lc> 尚未注册class_handler"
        )
        return

    # 比如group_message这样的实现了统一事件的事件
    # 如果用户同时定义了group_message和onebot_group_message，应该执行两次
    event_mapping = UNIVERSAL_PROTOCOL_EVENT_MAPPING.get(event_meta.raw_event_name)
    if event_mapping and event_meta.protocol_event_name in event_mapping:
        await run_class_handlers(
            event_meta,
            class_handler_names,
            universal=True,
        )

    await run_class_handlers(
        event_meta,
        class_handler_names,
    )


async def with_validators(
    mode: T_RouteMode, source_id: str, target: Literal["class_handlers", "commands"]
):
    results: Set[str] = set()

    for validator_name, validator_dict in route_mapping.mapping["validators"][
        mode
    ].items():
        validator = route_validator_mapping[validator_name]

        if await await_or_sync(validator, **{"mode": mode, "source_id": source_id}):
            results |= validator_dict[target]

    return results


async def run_class_handlers(
    event_meta: EventMeta,
    class_handler_names: Set[str],
    universal=False,
):
    if universal:
        target_event_name = event_meta.raw_event_name
    else:
        target_event_name = event_meta.protocol_event_name

    kwargs = await get_event_handler_kwargs(event_meta, universal=universal)
    debug_log(kwargs, f"当前事件 <lc>{target_event_name}</lc> 可用的参数")

    for class_handler_name in class_handler_names:
        class_handler_cache = class_handler_mapping[class_handler_name]
        debug_log(class_handler_cache)

        event_handler = class_handler_cache.event_handlers.get(target_event_name)
        if not event_handler:
            logger.info(
                f"class_handler <lc>{class_handler_name}</lc> 未定义 <lc>{target_event_name}</lc>"
            )
            return

        logger.info(
            f"开始执行class_handler <lc>{class_handler_name}</lc> 的事件响应 <lc>{target_event_name}</lc>",
        )
        await await_or_sync(event_handler, **fit_kwargs(event_handler, kwargs))


async def get_event_handler_kwargs(
    event_meta: EventMeta,
    universal=False,
) -> Dict[str, Any]:
    """
    不包含meta event, common + group + private

    telegram的common事件，也已经识别好了mode，不需要手动判断
    """

    protocol = event_meta.protocol
    mode = event_meta.mode
    source_id = event_meta.source_id
    raw_event = event_meta.raw_event

    if universal:
        mapping = UNIVERSAL_KWARGS_MAPPING
        # universal内部会根据protocol创建对应的bot实例，并挂载
        # 比如self.onebot == OnebotV11GroupBot
        bot_instance = get_or_create_bot(protocol, mode, source_id, universal=True)

    else:
        adapter = get_adapter(protocol)

        # event_name已经在handler_event中校验过存在，不需要再校验
        # if event_meta.raw_event_name not in adapter.all_events:
        #     raise EventHandleError(
        #         f"尚未为 <lc>{protocol}</lc> 事件 <lc>{event_meta.raw_event_name}</lc> 适配参数"
        #     )

        mapping = adapter.kwargs
        bot_instance = get_or_create_bot(protocol, mode, source_id)

    injected_kwargs = dict(
        protocol=protocol,
        mode=mode,
        source_id=source_id,
        raw_event=raw_event,
        event_meta=event_meta,
        bot=bot_instance,
    )

    kwarg_list: List[EventHandlerKwarg] = mapping.get(event_meta.raw_event_name, [])
    kwargs: Dict[str, Any] = {}

    for kwarg in kwarg_list:
        kwargs[kwarg.name] = await deepawait_or_sync(
            kwarg.value,
            **fit_kwargs(kwarg.value, injected_kwargs),
        )

    return kwargs


def get_or_create_bot(
    protocol: T_BotProtocol,
    mode: T_RouteMode,
    identifier: str,
    universal=False,
) -> BaseBot:

    instances_dict = route_mapping.bot_instances

    if universal:
        key = ("universal", mode, identifier)
    else:
        key = (protocol, mode, identifier)

    bot_instance: Optional[BaseBot] = None

    if key in instances_dict:
        bot_instance = instances_dict[key]
        return bot_instance

    if universal:
        # ? todo private add_group
        bot_instance = UniversalGroupBot(protocol, mode, identifier)
        return bot_instance

    bot_id = get_bot_id(protocol)

    # 如果能用3.10的match就好了
    if mode == "group":
        if protocol == "onebot":
            bot_instance = OnebotV11GroupBot(bot_id, identifier)
        elif protocol == "keaimao":
            bot_instance = KeaimaoGroupBot(bot_id, identifier)
        elif protocol == "telegram":
            bot_instance = TelegramGroupBot(bot_id, identifier)

    elif mode == "private":
        if protocol == "onebot":
            bot_instance = OnebotV11PrivateBot(bot_id, identifier)
        elif protocol == "keaimao":
            bot_instance = KeaimaoPrivateBot(bot_id, identifier)
        elif protocol == "telegram":
            bot_instance = TelegramPrivateBot(bot_id, identifier)

    if not bot_instance:
        raise EventHandleError(
            f"未能创建bot实例 <lc>{protocol}</lc> <lc>{mode}</lc> <lc>{identifier}</lc>"
        )

    instances_dict[key] = bot_instance

    return bot_instance
