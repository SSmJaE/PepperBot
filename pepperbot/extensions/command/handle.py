from collections import deque
import re
from inspect import isawaitable
from typing import Any, Dict, List, Optional, Set, cast

from devtools import debug
from pepperbot.core.message.chain import MessageChain
from pepperbot.exceptions import (
    ClassCommandDefinitionError,
    ClassCommandOnExit,
    ClassCommandOnFinish,
)
from pepperbot.extensions.command.parse import (
    meet_command_exit,
    meet_command_prefix,
)
from pepperbot.store.command import (
    ClassCommandStatus,
    CommandConfig,
    T_CommandStatusKey,
    class_command_mapping,
    class_command_config_mapping,
    normal_command_context_mapping,
)
from pepperbot.types import T_BotProtocol, T_RouteMode
from pepperbot.utils.common import await_or_sync, fit_kwargs
from pepperbot.extensions.log import logger
from pprint import pformat


COMMAND_LIFECYCLE_EXCEPTIONS: Dict = {
    ClassCommandOnExit.__name__: "exit",
    ClassCommandOnFinish.__name__: "finish",
}


def get_command_status(key: T_CommandStatusKey, command_config: CommandConfig):
    # 新建status时，返回Initial

    if key not in normal_command_context_mapping:
        normal_command_context_mapping[key] = ClassCommandStatus(
            history=deque(maxlen=command_config.history_size)
        )

    return normal_command_context_mapping[key]

    # 指向哪里？initial?

    # 指令本身是跨协议、跨消息来源的吗？

    # todo 命令的优先级，
    # 命令需要优先级吗？
    # 普通的group_message也有默认优先级，所以命令可以先于group_message执行，也可以后于


def construct_command_sender():
    pass


def parse_patterns(chain: MessageChain):
    # raise EventHandleError(f"无法解析pattern")
    pass


def store_to_history_deque(key, raw_event, chain, patterns):
    # last_updated_time
    pass


async def run_command_method(method_name, method, all_locals: Dict) -> Any:
    debug(all_locals)
    injected_kwargs = dict(
        raw_event=all_locals["raw_event"],
        chain=all_locals["chain"],
        sender=all_locals["sender"],
        # context=all_locals["context"],
    )

    if method_name == "cache":
        injected_kwargs["exception"] = all_locals["exception"]

    else:
        if method_name not in COMMAND_LIFECYCLE_EXCEPTIONS.values():
            injected_kwargs = {**injected_kwargs, **all_locals["patterns"]}

    # 参数和group_message/friend_message事件参数一致
    logger.debug(f"将被注入 {method_name} 的参数\n", pformat(injected_kwargs))
    result = await await_or_sync(method, **fit_kwargs(method, injected_kwargs))
    debug(result)
    return result


def check_result(command_name: str, method_names, result_name: str, result: Any):
    if result == None:  # 流程正常退出
        raise ClassCommandOnFinish()

    else:
        if not (callable(result) or isawaitable(result)):
            raise ClassCommandDefinitionError(f"未提供指令 {command_name} 可继续执行的下一个方法")

        if not result_name in method_names:
            raise ClassCommandDefinitionError(
                f"指令 {command_name} 可继续执行的下一个方法，需要在指令中定义，不能是指令外部定义的函数"
            )


def update_command_pointer(command_name, protocol, mode, source_id, result_name):
    pass


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
        command_method_names = class_command_mapping.keys()

        command_config = class_command_config_mapping[command_name]["default"]

        key = (command_name, protocol, mode, source_id)
        status = get_command_status(key, command_config)
        pointer = status.pointer

        if pointer == "initial":
            if meet_command_prefix(chain, command_name, command_config):
                logger.info(f"{chain.pure_text} 满足指令 {command_name} 的执行条件")
            else:
                logger.info(f"{chain.pure_text} 不满足指令 {command_name} 的执行条件")
                continue

        sender = construct_command_sender()
        # patterns = parse_patterns(chain, sender)
        patterns = {}

        try:
            if meet_command_exit(chain, command_config):
                logger.info(f"满足指令 {command_name} 的退出条件")
                raise ClassCommandOnExit()

            logger.info(f"开始执行指令 {command_name} 的 {pointer} 方法")
            # 当前指向的方法，或者说，当前激活的命令回调方法
            target_method = command_method_mapping[pointer]
            result = await run_command_method(pointer, target_method, locals())

            store_to_history_deque(key, raw_event, chain, patterns)

            # 判断是否正常退出
            result_name = str(result)
            check_result(command_name, command_method_names, result_name, result)
            # 设置下一次执行时要调用的方法
            update_command_pointer(protocol, mode, source_id, command_name, result_name)

        except Exception as exception:
            exception_name: str = exception.__class__.__qualname__  # type:ignore
            if exception_name in COMMAND_LIFECYCLE_EXCEPTIONS:
                lifecycle_name = COMMAND_LIFECYCLE_EXCEPTIONS[exception_name]

                lifecycle_handler = command_method_mapping.get(lifecycle_name)
                if lifecycle_handler:
                    logger.info(f"开始执行指令 {command_name} 的 {lifecycle_name} 生命周期")
                    await run_command_method(
                        lifecycle_name, lifecycle_handler, locals()
                    )

            else:
                if "catch" in command_method_names:
                    cache_handler = command_method_mapping.get("catch")
                    if cache_handler:
                        logger.exception(
                            f"指令 {command_name} 的 {pointer} 方法执行出错，开始执行用户定义的异常捕获"
                        )
                        await run_command_method("cache", cache_handler, locals())

                else:
                    raise exception
