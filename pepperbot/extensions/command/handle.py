import datetime
import pickle
import time
from collections import deque
from typing import Any, Callable, Deque, Dict, Iterable, List, Set, Tuple, Union, cast

from devtools import debug

from pepperbot.adapters.onebot.event import construct_chain
from pepperbot.core.message.chain import MessageChain, chain_factory
from pepperbot.core.route.available import check_available
from pepperbot.exceptions import ClassCommandOnExit, PatternFormatError
from pepperbot.extensions.command.constant import LIFECYCLE_WITHOUT_PATTERNS
from pepperbot.extensions.command.pattern import parse_pattern
from pepperbot.extensions.command.sender import CommandSender
from pepperbot.extensions.command.timeout import run_timeout
from pepperbot.extensions.command.utils import meet_command_exit, meet_command_prefix
from pepperbot.extensions.log import debug_log, logger
from pepperbot.extensions.scheduler import async_scheduler
from pepperbot.store.command import (
    ClassCommandMethodCache,
    ClassCommandStatus,
    CommandConfig,
    HistoryItem,
    command_timeout_jobs,
)
from pepperbot.store.event import EventHandlerKwarg, EventMetadata
from pepperbot.store.meta import class_command_config_mapping, class_command_mapping
from pepperbot.types import T_ConversationType
from pepperbot.utils.common import await_or_sync, fit_kwargs


async def run_class_command(
    event_metadata: EventMetadata,
    class_command_config_id: str,
    stop_propagation: Callable[[], None],
    running=False,
):
    """只有has_running时，或者has_available时，才会调用此函数"""

    command_kwargs = await construct_command_kwargs(
        event_metadata, class_command_config_id, stop_propagation, running
    )

    command_name = command_kwargs["command_name"]
    class_command_cache = class_command_mapping[command_name]
    command_method_mapping = class_command_cache.command_method_mapping
    command_method_names = command_method_mapping.keys()

    pointer = command_kwargs["status"].pointer

    returned_method_name = "not None"
    has_unhandled_exception = False
    unhandled_exception = Exception("should not be raised")

    status = command_kwargs["status"]

    lifecycle_kwargs = dict(
        command_name=command_name,
        command_method_mapping=command_method_mapping,
        pointer=pointer,
        command_kwargs=command_kwargs,
    )

    try:
        if running and meet_command_exit(
            command_kwargs["chain"], command_kwargs["command_config"]
        ):
            logger.info(
                f"<y>{command_kwargs['chain'].pure_text}</y> 满足指令 <lc>{command_name}</lc> 的退出条件"
            )
            raise ClassCommandOnExit()  # TODO 一并传递触发exit生命周期的exit_pattern，作为参数

        logger.info(f"开始执行指令 <lc>{command_name}</lc> 的 <lc>{pointer}</lc> 方法")

        # 当前指向的方法，或者说，当前激活的命令回调方法
        command_method_cache = command_method_mapping[pointer]

        # 这里设置为None，是为了应对指令第一次运行，直接运行initial，就抛出异常的情况
        # 如果成功运行，就直接
        returned_method_name = "__unset__"

        # 如果解析出错，会直接抛出异常，所以不会修改pointer的指向
        # 这里抛出FormatException，不应该触发cleanup
        target_method_name, command_kwargs["patterns"] = await parse_pattern(
            event_metadata,
            class_command_cache,
            command_method_cache,
            pointer,
            command_kwargs,
            command_name,
            status,
        )

        current_time = time.time()
        status.last_updated_time = current_time
        await status.update()

        next_run_time = datetime.datetime.fromtimestamp(current_time + status.timeout)

        if status.id not in command_timeout_jobs:
            job = async_scheduler.add_job(
                run_timeout,
                kwargs=dict(status=status),
                next_run_time=next_run_time,
            )
            command_timeout_jobs[status.id] = job
        else:
            # TODO status对象的缓存问题，最好的解决方案，就是remove再add
            job = command_timeout_jobs[status.id]
            job.modify(next_run_time=next_run_time)

        # target_method = command_method_cache.method
        target_method = command_method_mapping[target_method_name].method
        returned_method = await run_class_command_method(
            pointer, target_method, command_kwargs, running=running
        )

        # 判断是否正常退出
        returned_method_name = returned_method.__name__ if returned_method else "None"

        # 设置下一次执行时要调用的方法
        await update_command_pointer(status, command_kwargs, returned_method_name)

        if returned_method_name != "None":
            debug_log(
                title=f"方法 <lc>{pointer}</lc> 返回的下一步指向为 <lc>{returned_method_name}</lc>"
            )
        else:
            debug_log(title=f"方法 <lc>{pointer}</lc> 返回的下一步指向为 <lc>None</lc>，结束会话")

    except PatternFormatError as e:
        # PatternError，不应该被catch生命周期捕获
        # 同时，也不应触发其他生命周期，比如finish和cleanup
        # pointer不应该发生改变
        # debug("PatternFormatError", e)
        returned_method_name = "pattern_format_error"

    except ClassCommandOnExit:
        # 当触发生命周期时，立即调用，而不是等到用户下一次交互

        try:
            returned_method_name = "None"

            await get_and_run_lifecycle("exit", **lifecycle_kwargs)

        except Exception as exception:
            if "catch" in command_method_names:
                returned_method_name = "None"

                lifecycle_kwargs["command_kwargs"]["exception"] = exception
                await get_and_run_lifecycle("catch", **lifecycle_kwargs)

            else:
                # finally保证cleanup一定会被调用，这里不需要手动调用
                # has_unhandled_exception = True
                # unhandled_exception = exception
                raise exception from exception

    except Exception as exception:
        # 调用生命周期，包括catch，自身出现的异常

        if "catch" in command_method_names:
            returned_method_name = "None"

            lifecycle_kwargs["command_kwargs"]["exception"] = exception
            await get_and_run_lifecycle("catch", **lifecycle_kwargs)

        else:
            # finally保证cleanup一定会被调用，这里不需要手动调用
            # has_unhandled_exception = True
            # unhandled_exception = exception

            raise exception from exception

    else:
        if returned_method_name != "None":
            return

        try:
            returned_method_name = "None"

            await get_and_run_lifecycle("finish", **lifecycle_kwargs)
        except Exception as exception:
            if "catch" in command_method_names:
                lifecycle_kwargs["command_kwargs"]["exception"] = exception
                await get_and_run_lifecycle("catch", **lifecycle_kwargs)

            else:
                # finally保证cleanup一定会被调用，这里不需要手动调用
                # has_unhandled_exception = True
                # unhandled_exception = exception

                raise exception from exception

    finally:
        # returned_method_name == "None" ，说明指令正常结束
        # has_unhandled_exception，说明指令出现了异常
        # 只有这两种情况，才需要重置指令状态

        # 不能出现return，会影响re raise
        if returned_method_name == "None" or returned_method_name == "__unset__":
            try:
                await status.delete()  # 存在本身，会影响has_running_command的判断

                # 虽然在run_timeout中，判断了status是否存在——对应上方的status.delete()
                # 但是这样的效果，只是不运行run_timeout(status不存在，立即return)，job还是一直存在的，需要手动remove

                job = command_timeout_jobs[status.id]
                if async_scheduler.get_job(job.id):
                    job.remove()

                if status.id in command_timeout_jobs:
                    command_timeout_jobs.pop(status.id)

            except Exception as another_exception:
                logger.error(f"无法重置指令 <lc>{command_name}</lc> 的状态")

            await get_and_run_lifecycle("cleanup", **lifecycle_kwargs)


async def get_and_run_lifecycle(
    method_name: str,
    command_name: str,
    command_method_mapping: Dict[str, ClassCommandMethodCache],
    pointer: str,
    command_kwargs: dict,
):
    command_method_cache = command_method_mapping.get(method_name)
    if not command_method_cache:
        logger.info(f"指令 <lc>{command_name}</lc> 未定义生命周期 <lc>{method_name}</lc>")
        return

    if method_name == "catch":
        logger.error(
            f"指令 <lc>{command_name}</lc> 的 <lc>{pointer}</lc> 方法执行出错，"
            + f"开始执行用户定义的异常捕获生命周期 <lc>{method_name}</lc>"
        )
    else:
        logger.info(f"开始执行指令 <lc>{command_name}</lc> 的生命周期 <lc>{method_name}</lc>")

    await run_class_command_method(
        method_name, command_method_cache.method, command_kwargs
    )


async def run_class_command_method(
    method_name, method, command_kwargs: Dict, running=True
) -> Any:
    """通过running，避免刚好指令第一次触发时 + available应用到initial上，导致available被判断两次"""

    # debug_log(command_kwargs, title="当前可用变量")

    injected_kwargs = dict(
        alias=command_kwargs["alias"],
        prefix=command_kwargs["prefix"],
        raw_event=command_kwargs["raw_event"],
        chain=command_kwargs["chain"],
        sender=command_kwargs["sender"],
        history=command_kwargs["history"],
        context=command_kwargs["context"],
        config=command_kwargs["command_config"].config,
        stop_propagation=command_kwargs["stop_propagation"],
    )

    if method_name == "catch":
        injected_kwargs["exception"] = command_kwargs["exception"]

    if method_name not in LIFECYCLE_WITHOUT_PATTERNS:
        injected_kwargs = {**injected_kwargs, **command_kwargs["patterns"]}

    debug_log(injected_kwargs, title=f"将被注入 <lc>{method_name}</lc> 的参数")

    # not running的情况，find_first_available已经检查过了，这里一定是running的
    if running:
        available = await check_available(method, injected_kwargs, is_class=False)
        # debug(available)

        if not available:
            return method

    returned_method = await await_or_sync(method, **fit_kwargs(method, injected_kwargs))

    return returned_method


async def get_command_status(
    event_metadata: EventMetadata, command_name: str, command_config: CommandConfig
):
    """根据不同的交互策略，从数据库中获取对应的状态"""

    # TODO 跨protocol锁定用户
    # TODO 跨protocol锁定群/channel

    filter_kwargs = dict(
        command_name=command_name,
        config_id=command_config.config_id,
        protocol=event_metadata.protocol,
    )

    # 群/channel/私聊中，仅对应的用户(自己)可以触发
    if command_config.interactive_strategy == "same_source_same_user":
        filter_kwargs.update(
            conversation_type=cast(
                T_ConversationType, event_metadata.conversation_type
            ),
            conversation_id=event_metadata.source_id,
            user_id=event_metadata.user_id,
        )

    # 群/channel/私聊中，任意用户(私聊只有一个用户)都可以触发
    elif command_config.interactive_strategy == "same_source_any_user":
        filter_kwargs.update(
            conversation_type=cast(
                T_ConversationType, event_metadata.conversation_type
            ),
            conversation_id=event_metadata.source_id,
            user_id="any",
        )

    # 跨source锁定用户，不管他是通过群/channel/私聊和bot交互的
    elif command_config.interactive_strategy == "any_source_same_user":
        filter_kwargs.update(
            conversation_type="any",
            conversation_id="any",
            user_id=event_metadata.user_id,
        )

    # 所有消息渠道的所有用户都可以触发
    elif command_config.interactive_strategy == "any_source_any_user":
        filter_kwargs.update(
            conversation_type="any",
            conversation_id="any",
            user_id="any",
        )

    else:
        raise ValueError(f"不支持的交互策略 <lc>{command_config.interactive_strategy}</lc>")

    debug_log(filter_kwargs, title="获取指令状态的过滤条件")

    # 需要pepperbot启动时，立即清理一次无效的指令状态，不然会干扰这里的判断
    # TODO 同一个用户，极短时间内，连续满足指令的匹配(/并发测试)，导致存在多个status的情况
    class_command_status, created = await ClassCommandStatus.objects.get_or_create(
        **filter_kwargs,
        _defaults=dict(
            **filter_kwargs,
            timeout=command_config.timeout,
        ),
    )

    return class_command_status, created


async def update_command_pointer(
    status: ClassCommandStatus,
    command_kwargs: Dict,
    result_name: str,
):
    """此时已经经过check_result，result_name一定有效"""

    status.pointer = result_name
    history = command_kwargs["history"]

    history.append(
        HistoryItem(
            raw_event=command_kwargs["raw_event"],
            chain=command_kwargs["chain"],
        )
    )
    status.history = pickle.dumps(history)
    status.context = pickle.dumps(command_kwargs["context"])

    status.last_updated_time = time.time()

    await status.update()


async def construct_command_kwargs(
    event_metadata: EventMetadata,
    class_command_config_id: str,
    stop_propagation: Callable[[], None],
    running=False,
):
    """
    # 所有生命周期都有
    - raw_event
    - chain
    - sender
    - status
    - history
    - context
    - config(通过as_command传入的custom_config)
    - prefix 触发了当前指令的前缀
    - alias 触发了当前指令的别名

    # 仅catch有
    - exception

    # 所有生命周期都没有
    - patterns

    # 仅timeout没有
    - stop_propagation

    - exit_pattern 最终满足匹配的pattern
    """

    raw_event = event_metadata.raw_event
    chain = await chain_factory(event_metadata)
    sender = CommandSender(event_metadata)

    class_command_config_cache = class_command_config_mapping[class_command_config_id]

    command_name = class_command_config_cache.class_command_name
    command_config = class_command_config_cache.command_config

    status, created = await get_command_status(
        event_metadata, command_name, command_config
    )
    if not running:
        history: Deque[HistoryItem] = deque(maxlen=command_config.history_size)
    else:
        history: Deque[HistoryItem] = pickle.loads(status.history)

    context: Dict = pickle.loads(status.context)

    # locals中需要prefix和alias，作为可选参数
    # 如果一直return self.initial，那么从第二次运行开始，需要手动获取一下prefix和alias
    prefix = context.get("prefix")
    alias = context.get("alias")

    if not prefix or not alias:
        meet_prefix, prefix_with_alias, prefix, alias = meet_command_prefix(
            chain,
            command_name,
            command_config,
        )

        context.update(dict(prefix=prefix, alias=alias))
        status.context = pickle.dumps(context)
        status.running = True
        await status.update()

    class_command_cache = class_command_mapping[command_name]
    command_method_mapping = class_command_cache.command_method_mapping
    command_method_names = command_method_mapping.keys()

    return dict(
        raw_event=raw_event,
        chain=chain,
        sender=sender,
        status=status,
        history=history,
        context=context,
        config=command_config.config,
        prefix=prefix,
        alias=alias,
        patterns=command_method_names,
        stop_propagation=stop_propagation,
        # 中间变量
        command_name=command_name,
        command_config=command_config,
    )
