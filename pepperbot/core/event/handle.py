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
    ALL_COMMON_EVENTS,
    ALL_GROUP_EVENTS,
    ALL_KEAIMAO_EVENTS,
    ALL_META_EVENTS,
    ALL_ONEBOTV11_EVENTS,
    ALL_PRIVATE_EVENTS,
    ALL_TELEGRAM_EVENTS,
    ALL_UNIVERSAL_EVENTS,
    GROUP_COMMAND_TRIGGER_EVENTS,
    PRIVATE_COMMAND_TRIGGER_EVENTS,
    UNIVERSAL_GROUP_EVENTS,
    UNIVERSAL_PRIVATE_EVENTS,
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
    get_event_handler_kwargs,
    get_onebot_caller,
    initial_bot_info,
    onebot_event_meta,
    route_mapping,
    route_validator_mapping,
)
from pepperbot.types import BaseBot, T_BotProtocol, T_RouteMode
from pepperbot.utils.common import await_or_sync, fit_kwargs
from pyrogram.enums.chat_type import ChatType
from pyrogram.types import CallbackQuery, Message

PROTOCOL_ADAPTER_MAPPING: Dict[T_BotProtocol, Any] = {
    "onebot": OnebotV11Adapter,
    "keaimao": KeaimaoAdapter,
    "telegram": TelegramAdapter,
}


def get_adapter(protocol: T_BotProtocol) -> BaseAdapater:
    return PROTOCOL_ADAPTER_MAPPING[protocol]


def get_or_create_bot(
    protocol: T_BotProtocol,
    mode: T_RouteMode,
    identifier: str,
    universal=False,
) -> BaseBot:
    """这里只创建非universal的bot_instance"""

    instances_dict = route_mapping.bot_instances

    if universal:
        key = ("universal", mode, identifier)
    else:
        key = (protocol, mode, identifier)

    bot_instance: Optional[BaseBot] = None

    if key not in instances_dict:
        if universal:
            bot_instance = UniversalGroupBot(protocol, mode, identifier)

        else:
            bot_id = get_bot_id(protocol)

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
            raise EventHandleError(f"未能创建bot实例 {protocol} {mode} {identifier}")

        instances_dict[key] = bot_instance

    else:
        bot_instance = instances_dict[key]

    return bot_instance


def figure_telegram_route_mode(raw_event: Dict) -> T_RouteMode:

    callback_object = raw_event["callback_object"]

    debug(callback_object)

    if isinstance(callback_object, CallbackQuery):
        chat_type: ChatType = callback_object.message.chat.type

    elif isinstance(callback_object, Message):
        chat_type: ChatType = callback_object.chat.type

    else:
        chat_type: ChatType = callback_object.chat_type

    if chat_type in [ChatType.BOT, ChatType.PRIVATE]:
        mode = "private"
    elif chat_type == ChatType.GROUP:
        mode = "group"
    else:
        raise EventHandleError(f"")

    return mode


async def get_kwargs(event_meta: EventMeta, event_name: str) -> Dict[str, Any]:
    """event_name已经校验过存在，不需要再校验"""

    protocol = event_meta.protocol
    mode = event_meta.mode
    source_id = event_meta.source_id
    raw_event = event_meta.raw_event

    mapping: T_HandlerKwargMapping
    real_event_name: str = event_name
    bot_instance: Optional[BaseBot]

    if event_name in ALL_UNIVERSAL_EVENTS:  # 不包含meta event, common + group + private
        mapping = UNIVERSAL_KWARGS_MAPPING

        if event_name in UNIVERSAL_GROUP_EVENTS:
            # universal内部会根据protocol创建对应的bot实例，并挂载
            # 比如self.onebot == OnebotV11GroupBot
            # todo 现在这个实现，handle_event到get_kwargs，有些地方还是不符合直觉，有空重构一下
            bot_instance = get_or_create_bot(
                protocol, "group", source_id, universal=True
            )
        elif event_name in UNIVERSAL_PRIVATE_EVENTS:
            bot_instance = get_or_create_bot(
                protocol, "private", source_id, universal=True
            )
        else:  # common events
            raise EventHandleError(f"尚未实现的universal事件 {real_event_name}")

    # elif event_name in ALL_ONEBOTV11_EVENTS:  # 有prefix
    elif protocol == "onebot":  # 有prefix
        mapping = OnebotV11Adapter.kwargs
        real_event_name = event_name.replace("onebot_", "")

        # 不直接mode == "group", 因为即使这样，还是要判断event_name是否在group_events中
        if real_event_name in OnebotV11Adapter.group_events:
            bot_instance = get_or_create_bot(protocol, mode, source_id)
        elif real_event_name in OnebotV11Adapter.private_events:
            bot_instance = get_or_create_bot(protocol, mode, source_id)
        else:  # common events
            raise EventHandleError(f"尚未实现的onebot事件 {real_event_name}")

    elif protocol == "keaimao":
        # elif event_name in ALL_KEAIMAO_EVENTS:
        mapping = KeaimaoAdapter.kwargs
        real_event_name = event_name.replace("keaimao_", "")

        if real_event_name in TelegramAdapter.group_events:
            bot_instance = get_or_create_bot(protocol, mode, source_id)
        elif real_event_name in TelegramAdapter.private_events:
            bot_instance = get_or_create_bot(protocol, mode, source_id)
        else:  # common events
            raise EventHandleError(f"尚未实现的keaimao事件 {real_event_name}")

    elif protocol == "telegram":
        # elif event_name in ALL_KEAIMAO_EVENTS:
        mapping = TelegramAdapter.kwargs
        real_event_name = event_name.replace("telegram_", "")

        if real_event_name in ALL_TELEGRAM_EVENTS:
            bot_instance = get_or_create_bot(protocol, mode, source_id)
        else:  # common events
            raise EventHandleError(f"尚未实现的telegram事件 {real_event_name}")
        # bot_instance = None

    else:
        raise EventHandleError(f"尚未实现的事件 {real_event_name}")

    return await get_event_handler_kwargs(
        mapping,
        real_event_name,
        protocol=protocol,
        mode=mode,
        raw_event=raw_event,
        source_id=source_id,
        bot=bot_instance,
        event_meta=event_meta,
    )


async def run_class_handlers(
    event_meta: EventMeta,
    event_name: str,
    class_handler_names: Set[str],
):
    if not class_handler_names:
        logger.info(
            f"<lc>{event_meta.mode}</lc> 模式的 <lc>{event_meta.source_id}</lc> 尚未注册class_handler"
        )
        return

    kwargs = await get_kwargs(event_meta, event_name)
    debug_log(kwargs, "当前事件可用的参数")

    for class_handler_name in class_handler_names:
        class_handler_cache = class_handler_mapping[class_handler_name]
        logger.debug(pformat(class_handler_cache))

        event_handler = class_handler_cache.event_handlers.get(event_name)
        # logger.debug(pformat(event_name, event_handler))
        if event_handler:
            logger.info(
                f"开始执行class_handler <lc>{class_handler_name}</lc> 的事件响应 <lc>{event_name}</lc>",
            )
            await await_or_sync(event_handler, **fit_kwargs(event_handler, kwargs))

        else:
            logger.info(
                f"class_handler <lc>{class_handler_name}</lc> 未定义 <lc>{event_name}</lc>"
            )


async def with_validators(mode: T_RouteMode, source_id: str):
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


def get_source_id(protocol: T_BotProtocol, mode: T_RouteMode, raw_event: Dict) -> str:
    source_id: Optional[str] = None

    if protocol == "onebot":
        if mode == "group":
            source_id = raw_event["group_id"]
        elif mode == "private":
            source_id = raw_event["sender"]["user_id"]

    elif protocol == "keaimao":
        if mode == "group":
            source_id = raw_event["from_wxid"]
            # from_wxid为群号
            # final_from_wxid为发言群员id
        elif mode == "private":
            source_id = raw_event["final_from_wxid"]

    elif protocol == "telegram":
        callback_object = raw_event["callback_object"]
        if mode == "group":
            # 注意不是from_user.id，是来源id，比如群号
            source_id = callback_object.chat.id

        elif mode == "private":
            source_id = callback_object.from_user.id

        elif mode == "channel":
            source_id = callback_object.chat.id

    if not source_id:
        raise EventHandleError(f"未能获取source_id")

    debug_log(source_id, "source_id")  # ! str化？

    return str(source_id)


async def handle_event(protocol: T_BotProtocol, raw_event: Dict):
    logger.info("-" * 50)

    if not route_mapping.has_initial:
        await initial_bot_info()
        logger.success("成功获取bot元信息")
        route_mapping.has_initial = True

    adapter = get_adapter(protocol)
    raw_event_name = adapter.get_event_name(raw_event)
    protocol_event_name: str = f"{protocol}_" + raw_event_name

    if protocol == "onebot":
        if not onebot_event_meta.has_skip_buffered_event:
            flag = skip_current_onebot_event(raw_event, raw_event_name)
            if not flag:
                return

        logger.info("onebot 心跳")

    class_handler_names: Set[str] = set()
    # 对同一个消息来源，同一个class_handler也只应调用一次
    class_command_names: Set[str] = set()
    # 对同一个消息对象，在处理一次事件时
    # 在global_commands、mapping、validator中重复注册的指令应该只运行一次
    mode: T_RouteMode
    source_id: str
    command_trigger_events: List[str]

    if protocol_event_name in ALL_GROUP_EVENTS:
        mode = "group"
        source_id = get_source_id(protocol, mode, raw_event)

    elif protocol_event_name in ALL_PRIVATE_EVENTS:
        mode = "private"
        source_id = get_source_id(protocol, mode, raw_event)

    elif protocol == "telegram":
        mode = figure_telegram_route_mode(raw_event)
        source_id = get_source_id(protocol, mode, raw_event)

    else:
        raise EventHandleError(f"无效或尚未适配的事件 <lc>{protocol_event_name}</lc>")

    logger.opt(colors=True).info(
        f"接收到 <lc>{protocol}</lc> 的事件 <lc>{raw_event_name}</lc>，来自于 <lc>{mode}</lc> 模式的 <lc>{source_id}</lc>"
    )

    if mode == "group":
        command_trigger_events = GROUP_COMMAND_TRIGGER_EVENTS
    elif mode == "private":
        command_trigger_events = PRIVATE_COMMAND_TRIGGER_EVENTS
    else:
        raise EventHandleError(f"")

    event_meta = EventMeta(
        protocol=protocol,
        mode=mode,
        source_id=source_id,
        raw_event=raw_event,
    )

    validator_handlers, validator_commands = await with_validators(mode, source_id)

    if protocol_event_name in command_trigger_events:
        # normal
        class_command_names |= route_mapping.global_commands[protocol][mode]
        class_command_names |= route_mapping.mapping[protocol][mode][source_id][
            "commands"
        ]
        class_command_names |= validator_commands

        if class_command_names:
            logger.info(f"<lc>{mode}</lc> 模式的 <lc>{source_id}</lc> 存在注册的指令，开始执行")
            await run_class_commands(event_meta, class_command_names)

        # lock_user
        # for rule_id, rule in lock_user_mapping.items():
        #     if source_id in rule[protocol]:
        #         await run_class_command(mode="lock_user",rule_id)

        # if mode =="group" or mode =="channel":
        #     lock_source_mapping

        # lock_source
    else:
        logger.info(f"<lc>{mode}</lc> 模式的 <lc>{source_id}</lc> 尚未注册指令")

    class_handler_names |= route_mapping.global_handlers[protocol][mode]
    class_handler_names |= route_mapping.mapping[protocol][mode][source_id][
        "class_handlers"
    ]
    class_handler_names |= validator_handlers

    debug_log(class_handler_names, "所有可用class_handler")

    # 比如group_message这样的实现了统一事件的事件
    # 如果用户同时定义了group_message和onebot_group_message，应该执行两次
    event_mapping = UNIVERSAL_PROTOCOL_EVENT_MAPPING.get(raw_event_name)
    if event_mapping and protocol_event_name in event_mapping:
        await run_class_handlers(event_meta, raw_event_name, class_handler_names)

    await run_class_handlers(event_meta, protocol_event_name, class_handler_names)
