import asyncio
from collections import defaultdict
from itertools import groupby
import json
from typing import (
    Any,
    Callable,
    DefaultDict,
    Dict,
    Iterator,
    List,
    Literal,
    Optional,
    Set,
    Type,
    Union,
    cast,
)

import arrow
from devtools import debug, pformat
from pyrogram.enums.chat_type import ChatType
from pyrogram.types import CallbackQuery, Message

from pepperbot.adapters.keaimao import KeaimaoAdapter
from pepperbot.adapters.keaimao.api import KeaimaoGroupBot, KeaimaoPrivateBot
from pepperbot.adapters.onebot import OnebotV11Adapter
from pepperbot.adapters.onebot.api import OnebotV11GroupBot, OnebotV11PrivateBot
from pepperbot.adapters.telegram import TelegramAdapter
from pepperbot.adapters.telegram.api import TelegramGroupBot, TelegramPrivateBot
from pepperbot.adapters.universal.api import UniversalGroupBot, UniversalPrivateBot
from pepperbot.core.event.base_adapter import BaseAdapter
from pepperbot.core.event.universal import (
    COMMAND_TRIGGER_EVENTS,
    UNIVERSAL_PROTOCOL_EVENT_MAPPING,
)
from pepperbot.core.event.utils import skip_current_onebot_event
from pepperbot.core.route.available import check_available
from pepperbot.exceptions import EventHandleError, StopPropagation
from pepperbot.extensions.command.handle import (
    find_first_available_command,
    has_running_command,
    run_class_command,
)
from pepperbot.extensions.log import debug_log, logger
from pepperbot.store.event import (
    EventDispatchMetadata,
    EventHandlerKwarg,
    EventMetadata,
    PropagationConfig,
)
from pepperbot.store.meta import (
    LAST_ONEBOT_HEARTBEAT_TIME,
    get_bot_id,
    get_onebot_caller,
    initial_bot_info,
    onebot_event_meta,
    route_mapping,
    class_command_config_mapping,
    class_handler_mapping,
    route_validator_mapping,
    bot_instances,
    class_command_mapping,
)
from pepperbot.store.orm import get_metadata, set_metadata
from pepperbot.types import (
    BaseBot,
    T_BotProtocol,
    T_ConversationType,
    T_DispatchHandler,
    T_HandlerType,
)
from pepperbot.utils.common import await_or_sync, deepawait_or_sync, fit_kwargs


async def handle_event(protocol: T_BotProtocol, raw_event: Dict):
    """初步根据protocol和raw_event，构造出event_meta，便于下一步进行事件调度"""

    # 有可能接收到事件时，bot还没有初始化完成，所以这里保证一下
    has_initial_bot_info = await get_metadata("has_initial_bot_info", False)
    if not has_initial_bot_info:
        await initial_bot_info()
        logger.success("成功获取bot元信息")
        await set_metadata("has_initial_bot_info", True)

    event_metadata = construct_event_metadata(protocol, raw_event)

    # 如果go-cqhttp先于bot启动，那么go-cqhttp会在bot启动时，将bot未启动之前的事件全部推送过来
    # 大部分事件的发生时间，可能过久，没有再进行处理的必要
    if protocol == "onebot":
        if not onebot_event_meta.has_skip_buffered_event:
            continue_flag = skip_current_onebot_event(
                raw_event, event_metadata.protocol_event.raw_event_name
            )
            if not continue_flag:
                return

    # debug(event_metadata)

    if not (event_metadata.conversation_type and event_metadata.source_id):
        if event_metadata.protocol_event.protocol_event_name == "onebot_heartbeat":
            # 存储心跳事件，用于health_check
            current_timestamp = arrow.now().timestamp()
            await set_metadata(LAST_ONEBOT_HEARTBEAT_TIME, current_timestamp)
            return

        logger.error(
            f"无效或尚未适配的事件"
            + f" <lc>{protocol}</lc> 的事件 <lc>{event_metadata.protocol_event.raw_event_name}</lc>"
        )
        return

    logger.info(
        f"接收到 <lc>{protocol}</lc> 的事件 <lc>{event_metadata.protocol_event.raw_event_name}</lc>，"
        + f"来自于会话 <lc>{event_metadata.conversation_type}</lc> <lc>{event_metadata.source_id}</lc>"
    )

    event_dispatch_metadata = EventDispatchMetadata()

    disordered_handlers: Set[T_DispatchHandler] = set()
    """ 
    (priority, concurrency, "class_handler", class_handler_name)
    (priority, concurrency, "class_command", class_command_config_id)
      
    """

    (
        class_command_config_ids,
        disordered_class_command_handlers,
    ) = await get_relevant_class_commands(event_metadata)

    has_running, disordered_class_command_handler = await has_running_command(
        event_metadata, class_command_config_ids
    )
    event_dispatch_metadata.has_running_command = has_running
    debug_log(has_running)
    debug_log(disordered_class_command_handler)

    if has_running:
        # 这个是全局的，不管有多少个propagation group，只要有一个指令在运行，就不会再执行其他指令
        logger.info(f"存在运行中的指令 <lc>{disordered_class_command_handler[3]}</lc>，继续执行该指令")
        disordered_handlers.add(disordered_class_command_handler)
        event_dispatch_metadata.command_dispatch_handler = (
            disordered_class_command_handler
        )

    else:
        disordered_handlers |= disordered_class_command_handlers
        ordered_command_handlers = sorted(
            list(disordered_class_command_handlers), key=lambda x: x[0], reverse=True
        )

        (
            has_available_command,
            disordered_class_command_handler,
        ) = await find_first_available_command(ordered_command_handlers, event_metadata)
        event_dispatch_metadata.has_available_command = has_available_command
        if has_available_command:
            event_dispatch_metadata.command_dispatch_handler = (
                disordered_class_command_handler
            )

    # TODO 除了validator，这个可以缓存一下
    # 原来没必要缓存，但是现在有了priority + concurrency，可以缓存一下
    disordered_handlers |= await get_relevant_class_handlers(
        event_metadata, event_dispatch_metadata
    )

    ordered_handlers: List[T_DispatchHandler] = list(disordered_handlers)
    ordered_handlers.sort(key=lambda x: x[1], reverse=True)
    grouped_ordered_handlers = groupby(ordered_handlers, key=lambda x: x[0])

    # debug_log(dict(grouped_ordered_handlers))

    groups = []
    for propagation_group, dispatch_handlers in grouped_ordered_handlers:
        groups.append(
            asyncio.create_task(
                dispatch_propagation_group(
                    event_metadata,
                    event_dispatch_metadata,
                    propagation_group,
                    list(dispatch_handlers),
                )
            )
        )

    # debug(groups)

    # TODO 确保多个event之间(同时接受)，不会阻塞
    await asyncio.gather(*groups)


async def dispatch_propagation_group(
    event_metadata: EventMetadata,
    event_dispatch_metadata: EventDispatchMetadata,
    propagation_group: str,
    ordered_handlers: List[T_DispatchHandler],
):
    """
    500, True, "class_handler", "class_handler_name"
    400, True, "class_command", "class_command_config_id"
    300, False, "class_handler", "class_handler_name"
    200, False, "class_command", "class_command_config_id"
    100, True, "class_handler", "class_handler_name"

    200、300这两个handler之间，priority和StopPropagation是起效的
    400、500这两个handler之间，priority有效，但是StopPropagation并不一定能起到效果
    """

    per_propagation_group = dict(
        propagation_group=propagation_group,
        stop_propagation=False,
    )

    def stop_propagation():
        per_propagation_group["stop_propagation"] = True

    ordered_handlers_count = len(ordered_handlers)
    index = 0

    # debug(propagation_group, ordered_handlers)

    tasks: list[asyncio.Task] = []
    for dispatch_handler in ordered_handlers:
        _, _, concurrency, handler_type, handler_identifier = dispatch_handler
        index += 1

        try:
            # 直到下一个阻塞性(await run)的handler调用之前，之间的handler，全都并发执行
            await asyncio.gather(*tasks)
            tasks.clear()

            if handler_type == "class_commands":
                if (
                    not event_dispatch_metadata.has_running_command
                    and not event_dispatch_metadata.has_available_command
                ):
                    continue

                if dispatch_handler != event_dispatch_metadata.command_dispatch_handler:
                    continue

                if concurrency:
                    task = asyncio.create_task(
                        run_class_command(
                            event_metadata,
                            handler_identifier,
                            stop_propagation,
                            event_dispatch_metadata.has_running_command,
                        )
                    )
                    tasks.append(task)
                else:
                    await run_class_command(
                        event_metadata,
                        handler_identifier,
                        stop_propagation,
                        event_dispatch_metadata.has_running_command,
                    )

            if handler_type == "class_handlers":
                if concurrency:
                    # 比如group_message这样的实现了统一事件的事件
                    # 如果用户同时定义了group_message和onebot_group_message，应该执行两次
                    task = asyncio.create_task(
                        run_class_handler_method(
                            event_metadata, handler_identifier, universal=True
                        )
                    )
                    tasks.append(task)

                    task = asyncio.create_task(
                        run_class_handler_method(
                            event_metadata, handler_identifier, universal=False
                        )
                    )
                    tasks.append(task)
                else:
                    await run_class_handler_method(
                        event_metadata, handler_identifier, universal=True
                    )
                    await run_class_handler_method(
                        event_metadata, handler_identifier, universal=False
                    )

            if (
                index == ordered_handlers_count
                or per_propagation_group["stop_propagation"]
            ):
                # 确保最后一个handler也能被执行
                await asyncio.gather(*tasks)
                tasks.clear()

            if per_propagation_group["stop_propagation"]:
                logger.info(f"用户抛出 StopPropagation，停止传播组 {propagation_group} 后续的事件响应")
                break

        except StopPropagation:
            logger.info(f"用户抛出 StopPropagation，停止传播组 {propagation_group} 后续事件响应")
            break

        except Exception as e:
            logger.exception(f"当前传播组 {propagation_group} 事件响应执行异常，将继续执行下一个事件响应")


def construct_event_metadata(protocol: T_BotProtocol, raw_event: dict):
    """构造事件元信息"""

    adapter = get_adapter(protocol)
    protocol_event = adapter.get_event(raw_event)
    conversation_type = adapter.get_conversation_type(raw_event, protocol_event)
    source_id = adapter.get_source_id(raw_event, conversation_type)
    user_id = adapter.get_user_id(raw_event, conversation_type)

    event_metadata = EventMetadata(
        protocol=protocol,
        raw_event=raw_event,
        protocol_event=protocol_event,
        conversation_type=conversation_type,
        source_id=source_id,
        user_id=user_id,
    )

    return event_metadata


PROTOCOL_ADAPTER_MAPPING: Dict[T_BotProtocol, Type[BaseAdapter]] = {
    "onebot": OnebotV11Adapter,
    "keaimao": KeaimaoAdapter,
    "telegram": TelegramAdapter,
}


def get_adapter(protocol: T_BotProtocol) -> Type[BaseAdapter]:
    return PROTOCOL_ADAPTER_MAPPING[protocol]


async def get_relevant_class_commands(event_meta: EventMetadata):
    class_command_config_ids: Set[str] = set()
    """ 在global_commands、mapping、validator中重复注册的指令应该只运行一次 """

    disordered_handlers: Set[T_DispatchHandler] = set()

    mode = cast(T_ConversationType, event_meta.conversation_type)
    protocol = event_meta.protocol
    source_id = event_meta.source_id

    if event_meta.protocol_event not in COMMAND_TRIGGER_EVENTS:
        logger.info(
            f"<lc>{protocol}</lc> 的事件 "
            + f"<lc>{event_meta.protocol_event.raw_event_name}</lc> 非指令触发事件"
        )
        return class_command_config_ids, disordered_handlers

    # 单一消息来源
    class_command_config_ids |= route_mapping[
        protocol, mode, "__global__", "class_commands"
    ]
    class_command_config_ids |= route_mapping[
        protocol, mode, source_id, "class_commands"
    ]
    class_command_config_ids |= await with_validators(
        protocol, mode, source_id, "class_commands"
    )

    if not class_command_config_ids:
        logger.info(f"<lc>{mode}</lc> 模式的 <lc>{source_id}</lc> 尚未注册指令")
        return class_command_config_ids, disordered_handlers

    for class_command_config_id in class_command_config_ids:
        class_command_config_cache = class_command_config_mapping[
            class_command_config_id
        ]
        command_name = class_command_config_cache.class_command_name
        class_command_cache = class_command_mapping[command_name]
        class_command_instance = class_command_cache.class_instance
        available = await check_available(class_command_instance, {})
        if not available:
            continue

        disordered_handlers.add(
            (
                class_command_config_cache.command_config.propagation_group,
                class_command_config_cache.command_config.priority,
                class_command_config_cache.command_config.concurrency,
                "class_commands",
                class_command_config_id,
            )
        )

    return class_command_config_ids, disordered_handlers


async def get_relevant_class_handlers(
    event_meta: EventMetadata, event_dispatch_metadata: EventDispatchMetadata
):
    mode = cast(T_ConversationType, event_meta.conversation_type)
    protocol = event_meta.protocol
    source_id = event_meta.source_id

    class_handler_names: Set[str] = set()
    """ 对同一个消息来源，在处理一次事件时,同一个class_handler也只应调用一次 """

    class_handler_names |= route_mapping[protocol, mode, "__global__", "class_handlers"]
    class_handler_names |= route_mapping[protocol, mode, source_id, "class_handlers"]
    class_handler_names |= await with_validators(
        protocol, mode, source_id, "class_handlers"
    )

    debug_log(class_handler_names, "所有可用class_handler")

    if not class_handler_names:
        logger.info(
            f"<lc>{event_meta.conversation_type}</lc> 模式的 <lc>{event_meta.source_id}</lc> 尚未注册class_handler"
        )
        return set()

    disordered_handlers: Set[T_DispatchHandler] = set()

    for class_handler_name in class_handler_names:
        class_handler_cache = class_handler_mapping[class_handler_name]
        class_handler_instance = class_handler_cache.class_instance

        propagation_config: Optional[PropagationConfig] = getattr(
            class_handler_instance, "config", None
        )
        if propagation_config is None:
            propagation_config = PropagationConfig()

        dispatch_handler: T_DispatchHandler = (
            propagation_config.propagation_group,
            propagation_config.priority,
            propagation_config.concurrency,
            "class_handlers",
            class_handler_name,
        )

        available = await check_available(
            class_handler_instance,
            dict(
                event_dispatch_metadata=event_dispatch_metadata,
                dispatch_handler=dispatch_handler,
            ),
        )
        if not available:
            continue

        disordered_handlers.add(dispatch_handler)

    return disordered_handlers


async def with_validators(
    protocol: T_BotProtocol,
    conversation_type: T_ConversationType,
    source_id: str,
    handler_type: T_HandlerType,
):
    handler_names: Set[str] = set()

    for validator_name in route_mapping[
        "validator",
        conversation_type,
        "__unset__",
        handler_type,
    ]:
        validator = route_validator_mapping[validator_name]

        try:
            # ( protocol, conversation_type, conversation_id, handler_type ) => accept
            accept = await await_or_sync(
                validator,
                **dict(
                    protocol=protocol,
                    conversation_type=conversation_type,
                    source_id=source_id,
                    handler_type=handler_type,
                ),
            )

            if accept:
                handler_names.add(validator_name)

        except Exception as e:
            logger.exception(e)

    return handler_names


async def run_class_handler_method(
    event_meta: EventMetadata,
    class_handler_name: str,
    universal=False,
):
    if universal:
        target_event_name = event_meta.protocol_event.raw_event_name
    else:
        target_event_name = cast(str, event_meta.protocol_event.protocol_event_name)

    kwargs = await get_event_handler_kwargs(event_meta, universal=universal)
    debug_log(kwargs, f"当前事件 <lc>{target_event_name}</lc> 可用的参数")

    class_handler_cache = class_handler_mapping[class_handler_name]
    debug_log(class_handler_cache)

    event_handler = class_handler_cache.event_handlers.get(target_event_name)
    if not event_handler:
        return

    available = await check_available(event_handler, kwargs, is_class=False)
    if not available:
        return

    logger.info(
        f"开始执行class_handler <lc>{class_handler_name}</lc> 的event_handler <lc>{target_event_name}</lc>",
    )

    await await_or_sync(event_handler, **fit_kwargs(event_handler, kwargs))


async def get_event_handler_kwargs(
    event_meta: EventMetadata,
    universal=False,
) -> Dict[str, Any]:
    """
    不包含meta event, common + group + private

    telegram的common事件，也已经识别好了mode，不需要手动判断
    """

    protocol = event_meta.protocol
    mode = cast(T_ConversationType, event_meta.conversation_type)
    source_id = event_meta.source_id
    raw_event = event_meta.raw_event

    if universal:
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

        bot_instance = get_or_create_bot(protocol, mode, source_id)

    injected_kwargs = dict(
        protocol=protocol,
        mode=mode,
        source_id=source_id,
        raw_event=raw_event,
        event_meta=event_meta,
        bot=bot_instance,
    )

    kwargs: Dict[str, Any] = {}

    for keyword_argument in event_meta.protocol_event.keyword_arguments:
        kwargs[keyword_argument.name] = await deepawait_or_sync(
            keyword_argument.value,
            **fit_kwargs(cast(Any, keyword_argument.value), injected_kwargs),
        )

    return kwargs


def get_or_create_bot(
    protocol: T_BotProtocol,
    mode: T_ConversationType,
    identifier: str,
    universal=False,
) -> BaseBot:
    """获取bot实例，如果不存在则创建"""
    instances_dict = bot_instances

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

    if mode == "group":
        if protocol == "onebot":
            bot_instance = OnebotV11GroupBot(bot_id, identifier)
        if protocol == "keaimao":
            bot_instance = KeaimaoGroupBot(bot_id, identifier)
        if protocol == "telegram":
            bot_instance = TelegramGroupBot(bot_id, identifier)

    elif mode == "private":
        if protocol == "onebot":
            bot_instance = OnebotV11PrivateBot(bot_id, identifier)
        if protocol == "keaimao":
            bot_instance = KeaimaoPrivateBot(bot_id, identifier)
        if protocol == "telegram":
            bot_instance = TelegramPrivateBot(bot_id, identifier)

    if not bot_instance:
        raise EventHandleError(
            f"未能创建bot实例 <lc>{protocol}</lc> <lc>{mode}</lc> <lc>{identifier}</lc>"
        )

    instances_dict[key] = bot_instance

    return bot_instance
