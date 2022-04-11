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
)

from devtools import debug, pformat
from pepperbot.adapters.keaimao.api import KeaimaoApi
from pepperbot.adapters.onebot.api import OnebotV11Api
from pepperbot.core.message.chain import MessageChain
from pepperbot.core.message.segment import T_SegmentInstance
from pepperbot.exceptions import (
    ClassCommandDefinitionError,
    ClassCommandOnExit,
    ClassCommandOnFinish,
    ClassCommandOnTimeout,
)
from pepperbot.extensions.command.pattern import parse_pattern
from pepperbot.extensions.command.utils import meet_command_exit, meet_command_prefix
from pepperbot.extensions.log import logger
from pepperbot.store.meta import EventHandlerKwarg
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

        else:
            if mode == "group":
                self.message_sender = partial(KeaimaoApi.group_message, source_id)
            else:
                self.message_sender = partial(KeaimaoApi.private_message, source_id)

    async def send_message(self, *segments: T_SegmentInstance):
        """自动识别消息来源并发送，不需要指定协议，不需要指定是私聊还是群"""
        return await self.message_sender(*segments)

    async def reply(self, *segments: T_SegmentInstance):
        pass


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


# def store_to_history_deque(key, raw_event, chain, patterns):
#     # last_updated_time
#     pass

COMMAND_LIFECYCLE_EXCEPTIONS: Dict = {
    ClassCommandOnExit.__name__: "exit",
    ClassCommandOnFinish.__name__: "finish",
    ClassCommandOnTimeout.__name__: "timeout",
}

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
    "initial": (*common_kwargs,),
    "exit": (*common_kwargs,),
    "finish": (*common_kwargs,),
    "timeout": (*common_kwargs,),
    "catch": (
        *common_kwargs,
        EventHandlerKwarg(name="exception", type_=Exception),
    ),
}


async def run_command_method(method_name, method, all_locals: Dict) -> Any:
    logger.debug(pformat(all_locals))
    injected_kwargs = dict(
        raw_event=all_locals["raw_event"],
        chain=all_locals["chain"],
        sender=all_locals["sender"],
        history=all_locals["status"].history,
        # context=all_locals["context"],
    )

    if method_name == "cache":
        injected_kwargs["exception"] = all_locals["exception"]

    else:
        if method_name not in COMMAND_LIFECYCLE_EXCEPTIONS.values():
            injected_kwargs = {**injected_kwargs, **all_locals["patterns"]}

    # 参数和group_message/friend_message事件参数一致
    logger.debug(f"将被注入 {method_name} 的参数\n{pformat(injected_kwargs)}")
    result = await await_or_sync(method, **fit_kwargs(method, injected_kwargs))
    logger.debug(pformat(result))
    return result


def check_result(
    command_name: str, method_names: Iterable[str], result_name: str, result: Any
):
    """运行时检查，和ast检查不冲突"""

    if result == None:  # 流程正常退出
        raise ClassCommandOnFinish()

    else:
        if not (callable(result) or isawaitable(result)):
            raise ClassCommandDefinitionError(f"未提供指令 {command_name} 可继续执行的下一个方法")

        if not result_name in method_names:
            raise ClassCommandDefinitionError(
                f"指令 {command_name} 可继续执行的下一个方法，需要在指令中定义，不能是指令外部定义的函数"
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
    """超时判断应该每次心跳都判断，而不是接收到该用户消息时"""

    logger.info("检查指令是否超时……")

    timeouted_status: List[T_CommandStatusKey] = []
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
            logger.info(f"{protocol} {mode} 中的用户 {source_id} 指令 {command_name} 已超时")

            if not len(status.history):
                logger.error(f"如果要执行timeout生命周期，history_size至少为1")
                timeouted_status.append(key)
                continue

            class_command_cache = class_command_mapping[command_name]
            command_method_mapping = class_command_cache.command_method_mapping
            command_method_names = command_method_mapping.keys()

            pointer = "timeout"

            lifecycle_handler = command_method_mapping.get(pointer)
            if not lifecycle_handler:
                logger.error(f"未定义timeout生命周期，直接结束指令")
                timeouted_status.append(key)
                continue

            logger.info(f"开始执行指令 {command_name} 的生命周期 {pointer}")

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
                timeouted_status.append(key)

    for key in timeouted_status:
        normal_command_context_mapping.pop(key)


async def run_class_commands(
    protocol: T_BotProtocol,
    mode: T_RouteMode,
    source_id: str,
    raw_event: Dict,
    class_command_names: Set[str],
):
    # todo kwargs pydantic化

    logger.info(f"开始执行指令")
    chain = MessageChain(protocol, mode, raw_event, source_id)

    for command_name in class_command_names:
        logger.info(f"-" * 50)

        class_command_cache = class_command_mapping[command_name]
        command_method_mapping = class_command_cache.command_method_mapping
        command_method_names = command_method_mapping.keys()

        command_config = class_command_config_mapping[command_name]["default"]

        key = (command_name, protocol, mode, source_id)
        status = get_command_status(key, command_config)
        pointer = status.pointer

        final_prefix = ""
        if pointer == "initial":
            meet_prefix, final_prefix = meet_command_prefix(
                chain, command_name, command_config
            )
            if meet_prefix:
                logger.info(f"{chain.pure_text} 满足指令 {command_name} 的执行条件")
            else:
                logger.info(f"{chain.pure_text} 不满足指令 {command_name} 的执行条件")
                continue

        sender = CommandSender(protocol, mode, source_id)

        try:
            if meet_command_exit(chain, command_config):
                logger.info(f"满足指令 {command_name} 的退出条件")
                raise ClassCommandOnExit()

            logger.info(f"开始执行指令 {command_name} 的 {pointer} 方法")

            # 当前指向的方法，或者说，当前激活的命令回调方法
            command_method_cache = command_method_mapping[pointer]

            patterns = await parse_pattern(
                chain,
                sender,
                pointer,
                command_method_cache,
                final_prefix,
                status.context,
            )

            target_method = command_method_cache.method
            result = await run_command_method(pointer, target_method, locals())

            # 判断是否正常退出
            result_name = result.__name__ if result else "not_exist_in_names"
            check_result(command_name, command_method_names, result_name, result)
            # 设置下一次执行时要调用的方法
            # store_to_history_deque(key, raw_event, chain, patterns)
            update_command_pointer(key, result_name, raw_event, chain)

        except Exception as exception:
            exception_name: str = exception.__class__.__qualname__  # type:ignore
            if exception_name in COMMAND_LIFECYCLE_EXCEPTIONS:
                lifecycle_name = COMMAND_LIFECYCLE_EXCEPTIONS[exception_name]

                lifecycle_handler = command_method_mapping.get(lifecycle_name)
                if lifecycle_handler:
                    logger.info(f"开始执行指令 {command_name} 的生命周期 {lifecycle_name}")
                    await run_command_method(
                        lifecycle_name, lifecycle_handler.method, locals()
                    )
                    update_command_pointer(key, "initial", raw_event, chain, reset=True)

                else:
                    logger.info(f"指令 {command_name} 的生命周期 {lifecycle_name} 无对应hook")

            else:
                if "catch" in command_method_names:
                    cache_handler = command_method_mapping.get("catch")
                    if cache_handler:
                        logger.exception(
                            f"指令 {command_name} 的 {pointer} 方法执行出错，开始执行用户定义的异常捕获"
                        )
                        await run_command_method(
                            "catch", cache_handler.method, locals()
                        )
                        update_command_pointer(
                            key, "initial", raw_event, chain, reset=True
                        )

                else:
                    raise exception from exception
