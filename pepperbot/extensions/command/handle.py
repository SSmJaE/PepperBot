import asyncio
import re
import time
from collections import deque
from functools import partial
from inspect import isawaitable
from typing import (
    Any,
    Deque,
    Dict,
    Iterable,
    List,
    Optional,
    Sequence,
    Set,
    Tuple,
    cast,
    final,
)

from devtools import debug, pformat
from pepperbot.adapters.keaimao.api import KeaimaoApi
from pepperbot.adapters.onebot.api import OnebotV11Api
from pepperbot.adapters.telegram.api import TelegramApi

# from pepperbot.adapters.telegram.api import TelegramApi
from pepperbot.core.message.chain import MessageChain, chain_factory
from pepperbot.core.message.segment import T_SegmentInstance
from pepperbot.exceptions import (
    ClassCommandDefinitionError,
    ClassCommandOnExit,
    ClassCommandOnFinish,
    ClassCommandOnTimeout,
    EventHandleError,
)
from pepperbot.extensions.command.pattern import parse_pattern
from pepperbot.extensions.command.utils import meet_command_exit, meet_command_prefix
from pepperbot.extensions.log import debug_log, logger
from pepperbot.store.meta import EventHandlerKwarg, EventMeta, get_telegram_caller
from pepperbot.store.command import (
    ClassCommandStatus,
    CommandConfig,
    HistoryItem,
    T_CommandStatusKey,
    class_command_config_mapping,
    class_command_mapping,
    normal_command_context_mapping,
)
from pepperbot.types import T_BotProtocol, T_RouteMode
from pepperbot.utils.common import await_or_sync, fit_kwargs


class CommandSender:
    __slots__ = ("message_sender",)

    def __init__(self, protocol: T_BotProtocol, mode: T_RouteMode, source_id: str):

        if protocol == "onebot":
            if mode == "group":
                self.message_sender = partial(OnebotV11Api.group_message, source_id)
            else:
                self.message_sender = partial(OnebotV11Api.private_message, source_id)

        elif protocol == "keaimao":
            if mode == "group":
                self.message_sender = partial(KeaimaoApi.group_message, source_id)
            else:
                self.message_sender = partial(KeaimaoApi.private_message, source_id)

        elif protocol == "telegram":
            if mode == "group":
                self.message_sender = partial(TelegramApi.group_message, source_id)
            else:
                self.message_sender = partial(TelegramApi.private_message, source_id)

        else:
            raise EventHandleError(f"")

    async def send_message(self, *segments: T_SegmentInstance):
        """自动识别消息来源并发送，不需要指定协议，不需要指定是私聊还是群"""
        return await self.message_sender(*segments)

    async def reply(self, *segments: T_SegmentInstance):
        pass


# def store_to_history_deque(key, raw_event, chain, patterns):
#     # last_updated_time
#     pass

COMMAND_LIFECYCLE_EXCEPTIONS: Dict = {
    ClassCommandOnExit.__name__: "exit",
    ClassCommandOnFinish.__name__: "finish",
    ClassCommandOnTimeout.__name__: "timeout",
}
""" 这些生命周期通过抛出异常触发 """

LIFECYCLE_WITHOUT_PATTERNS = ("exit", "finish", "timeout", "catch")
""" 这些生命周期不应支持pattern """

LIFECYCLE_NO_PROGRAMMIC = ("catch", "timeout", "exit")
""" 这些生命周期不应该主动调用 """

common_kwargs = (
    EventHandlerKwarg(name="raw_event", type_=Dict),
    EventHandlerKwarg(name="chain", type_=MessageChain),
    EventHandlerKwarg(name="sender", type_=CommandSender),
    EventHandlerKwarg(name="history", type_=Deque[HistoryItem]),
)

COMMAND_DEFAULT_KWARGS = {
    "initial": (
        *common_kwargs,
        EventHandlerKwarg(name="prefix", type_=str),
        EventHandlerKwarg(name="alias", type_=str),
    ),
    "exit": (*common_kwargs,),
    "finish": (*common_kwargs,),
    "timeout": (*common_kwargs,),
    "catch": (
        *common_kwargs,
        EventHandlerKwarg(name="exception", type_=Exception),
    ),
}
"""
用于检查用户定义的方法的参数的类型注解是否合法
也就是说，所有用户在对应方法中(比如initial)可用的参数及其类型，都应该出现在此处
这里并不需要像class_handler中一样，提供value，因为会在run_class_method中直接注入
 """


async def run_class_commands(event_meta: EventMeta, class_command_names: Set[str]):

    # locals中需要存在这些参数
    chain = await chain_factory(event_meta)

    protocol = event_meta.protocol
    mode = event_meta.mode
    source_id = event_meta.source_id
    raw_event = event_meta.raw_event
    sender = CommandSender(protocol, mode, source_id)

    target_command_name: Optional[str] = None
    final_prefix = ""

    has_running, command_name = has_running_command(event_meta, class_command_names)
    if has_running:
        logger.info(f"存在运行中的指令 <lc>{command_name}</lc>，继续执行该指令")
        target_command_name = command_name
        command_config = class_command_config_mapping[target_command_name]["default"]

    else:
        # locals中需要prefix和alias，作为initial的可选参数
        command_name, prefix_with_alias, prefix, alias = find_first_available_command(
            event_meta, class_command_names, chain
        )
        if command_name:
            target_command_name = command_name
            final_prefix = prefix_with_alias

        else:
            logger.info(f"未满足任何指令的执行条件")
            return

    class_command_cache = class_command_mapping[target_command_name]
    command_method_mapping = class_command_cache.command_method_mapping
    command_method_names = command_method_mapping.keys()
    command_config = class_command_config_mapping[target_command_name]["default"]

    key = (
        target_command_name,
        event_meta.protocol,
        event_meta.mode,
        event_meta.source_id,
    )
    status = get_command_status(key, command_config)
    pointer = status.pointer

    try:
        if has_running and meet_command_exit(chain, command_config):
            logger.info(f"<y>{chain.pure_text}</y> 满足指令 {command_name} 的退出条件")
            raise ClassCommandOnExit()

        logger.info(f"开始执行指令 <lc>{target_command_name}</lc> 的 <lc>{pointer}</lc> 方法")

        # 当前指向的方法，或者说，当前激活的命令回调方法
        command_method_cache = command_method_mapping[pointer]

        # locals中需要
        patterns = await parse_pattern(
            chain,
            sender,
            pointer,
            command_method_cache,
            final_prefix,
            status.context,
        )

        target_method = command_method_cache.method
        returned_method = await run_command_method(pointer, target_method, locals())

        # 判断是否正常退出
        returned_method_name = (
            returned_method.__name__ if returned_method else "not_exist_in_names"
        )
        check_returned_method(
            command_name,
            command_method_names,
            returned_method_name,
            returned_method,
        )

        # 设置下一次执行时要调用的方法
        # store_to_history_deque(key, raw_event, chain, patterns)
        update_command_pointer(key, returned_method_name, raw_event, chain)

    except Exception as exception:
        # 当触发生命周期时，立即调用，而不是等到用户下一次交互

        try:
            exception_name: str = exception.__class__.__qualname__  # type:ignore

            if exception_name in COMMAND_LIFECYCLE_EXCEPTIONS:
                lifecycle_name = COMMAND_LIFECYCLE_EXCEPTIONS[exception_name]

                lifecycle_handler = command_method_mapping.get(lifecycle_name)
                if lifecycle_handler:
                    logger.info(
                        f"开始执行指令 <lc>{command_name}</lc> 的生命周期 <lc>{lifecycle_name}</lc>"
                    )
                    await run_command_method(
                        lifecycle_name, lifecycle_handler.method, locals()
                    )

                else:
                    logger.info(
                        f"指令 <lc>{command_name}</lc> 未定义生命周期 <lc>{lifecycle_name}</lc>"
                    )

            else:
                if "catch" in command_method_names:
                    cache_handler = command_method_mapping.get("catch")
                    if cache_handler:
                        logger.error(
                            f"指令 {command_name} 的 {pointer} 方法执行出错，开始执行用户定义的异常捕获"
                        )
                        await run_command_method(
                            "catch", cache_handler.method, locals()
                        )

                else:
                    raise exception from exception

        except Exception as unhandled_exception:
            # 调用生命周期，包括catch，自身出现的异常
            raise unhandled_exception from exception

        finally:
            update_command_pointer(key, "initial", raw_event, chain, reset=True)


def get_command_status(key: T_CommandStatusKey, command_config: CommandConfig):
    # 新建status时，返回Initial

    if key not in normal_command_context_mapping:
        normal_command_context_mapping[key] = ClassCommandStatus(
            history=deque(maxlen=command_config.history_size),
            timeout=command_config.timeout,
        )

    return normal_command_context_mapping[key]

    # 指向哪里？initial?

    # 指令本身是跨协议、跨消息来源的吗？

    # todo 命令的优先级，
    # 命令需要优先级吗？
    # 普通的group_message也有默认优先级，所以命令可以先于group_message执行，也可以后于


def has_running_command(event_meta: EventMeta, class_command_names: Set[str]):
    for command_name in class_command_names:

        key = (command_name, event_meta.protocol, event_meta.mode, event_meta.source_id)
        command_config = class_command_config_mapping[command_name]["default"]
        status = get_command_status(key, command_config)

        pointer = status.pointer
        if pointer != "initial":
            return True, command_name

    return False, ""


def find_first_available_command(
    event_meta: EventMeta,
    class_command_names: Set[str],
    chain: MessageChain,
):
    for command_name in class_command_names:
        logger.info(f"-" * 50)

        command_config = class_command_config_mapping[command_name]["default"]
        key = (command_name, event_meta.protocol, event_meta.mode, event_meta.source_id)
        status = get_command_status(key, command_config)

        final_prefix = ""
        pointer = status.pointer
        if pointer == "initial":
            meet_prefix, final_prefix, prefix, alias = meet_command_prefix(
                chain,
                command_name,
                command_config,
            )
            if meet_prefix:
                logger.info(
                    f"<y>{chain.pure_text}</y> 满足指令 <lc>{command_name}</lc> 的执行条件"
                )
                return command_name, final_prefix, prefix, alias

            else:
                logger.info(
                    f"<y>{chain.pure_text}</y> 不满足指令 <lc>{command_name}</lc> 的执行条件"
                )
                continue

    return "", "", "", ""


async def run_command_method(method_name, method, all_locals: Dict) -> Any:
    debug_log(all_locals, title="当前可用变量")

    injected_kwargs = dict(
        raw_event=all_locals["raw_event"],
        chain=all_locals["chain"],
        sender=all_locals["sender"],
        history=all_locals["status"].history,
        # context=all_locals["context"],
    )

    if method_name == "catch":
        injected_kwargs["exception"] = all_locals["exception"]

    else:
        if method_name == "initial":
            injected_kwargs["alias"] = all_locals["alias"]
            injected_kwargs["prefix"] = all_locals["prefix"]

        if method_name not in COMMAND_LIFECYCLE_EXCEPTIONS.values():
            injected_kwargs = {**injected_kwargs, **all_locals["patterns"]}

    # 参数和group_message/friend_message事件参数一致
    debug_log(injected_kwargs, title=f"将被注入 <lc>{method_name}</lc> 的参数")

    returned_method = await await_or_sync(method, **fit_kwargs(method, injected_kwargs))

    debug_log(
        "", title=f"方法 <lc>{method_name}</lc> 返回的下一步指向 <lc>{returned_method}</lc>"
    )

    return returned_method


def check_returned_method(
    command_name: str,
    method_names: Iterable[str],
    returned_method_name: str,
    returned_method: Any,
):
    """运行时检查，和ast检查不冲突"""

    # 所有生命周期不会调用check_returned_method，所以不用排除
    if returned_method == None:  # 流程正常退出
        raise ClassCommandOnFinish()

    else:
        if not (callable(returned_method) or isawaitable(returned_method)):
            raise ClassCommandDefinitionError(
                f"指令 <lc>{command_name}</lc> 返回的 <lc>{returned_method_name}</lc> 方法不可调用"
                + "，应返回可调用的方法"
            )

        if not returned_method_name in method_names:
            raise ClassCommandDefinitionError(
                f"指令 <lc>{command_name}</lc> 返回的方法 <lc>{returned_method_name}</lc> ，"
                + "需要在指令中定义，不能是指令外部定义的函数"
            )


def update_command_pointer(
    key: T_CommandStatusKey,
    result_name: str,
    raw_event: Dict,
    chain: MessageChain,
    reset=False,
):
    """此时已经经过check_result，result_name一定有效"""

    status = normal_command_context_mapping[key]

    if not reset:
        status.pointer = result_name
        status.history.append(
            HistoryItem(
                raw_event=raw_event,
                chain=chain,
            )
        )

    else:
        status.pointer = "initial"
        status.history.clear()

    status.last_updated_time = time.time()


async def check_command_timeout():
    """应该主动进行超时判断，而不是接收到该用户消息时"""

    logger.info("检查指令是否超时……")

    timeout_status: List[T_CommandStatusKey] = []
    """ 不要在迭代字典的过程中，动态的修改字典 """

    for key, status in normal_command_context_mapping.items():
        pointer = status.pointer
        if pointer == "initial":
            continue

        last_updated_time = status.last_updated_time
        timeout = status.timeout
        current_time = time.time()

        # 超时判断，与上一条消息的createTime判断
        if current_time >= last_updated_time + timeout:

            command_name, protocol, mode, source_id = key
            logger.info(
                f"<lc>{protocol}</lc> <lc>{mode}</lc> 模式中的 <lc>{source_id}</lc> 指令 <lc>{command_name}</lc> 已超时"
            )

            if not len(status.history):
                logger.error(f"如果要执行timeout生命周期，history_size至少为1")
                timeout_status.append(key)
                continue

            class_command_cache = class_command_mapping[command_name]
            command_method_mapping = class_command_cache.command_method_mapping
            command_method_names = command_method_mapping.keys()

            pointer = "timeout"

            lifecycle_handler = command_method_mapping.get(pointer)
            if not lifecycle_handler:
                logger.info(
                    f"指令 <lc>{command_name}</lc> 未定义生命周期 <lc>{pointer}</lc>，直接结束指令"
                )
                timeout_status.append(key)
                continue

            logger.info(f"开始执行指令 <lc>{command_name}</lc> 的生命周期 <lc>{pointer}</lc>")

            history_item = status.history[-1]
            raw_event = history_item.raw_event
            chain = history_item.chain
            sender = CommandSender(protocol, mode, source_id)

            try:

                command_method_cache = command_method_mapping[pointer]
                target_method = command_method_cache.method
                # await run_command_method(pointer, target_method, locals())
                task = asyncio.create_task(
                    run_command_method(pointer, target_method, locals())
                )
                # await task

            except Exception as exception:
                if "catch" in command_method_names:
                    cache_handler = command_method_mapping.get("catch")
                    if cache_handler:
                        logger.exception(
                            f"指令 {command_name} 的 {pointer} 方法执行出错，开始执行用户定义的异常捕获"
                        )
                        await run_command_method("catch", cache_handler, locals())

                else:
                    raise exception from exception

            finally:
                timeout_status.append(key)

    for key in timeout_status:
        normal_command_context_mapping.pop(key)

        command_name, protocol, mode, source_id = key
        logger.info(
            f"协议 <lc>{protocol}</lc> <lc>{mode}</lc> 模式中 <lc>{source_id}</lc> 的指令 <lc>{command_name}</lc> 已timeout"
        )
