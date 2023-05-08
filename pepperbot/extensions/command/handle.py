import pickle
import time
from collections import deque
from inspect import isawaitable
from typing import Any, Callable, Deque, Dict, Iterable, List, Set, Tuple, Union, cast

from devtools import debug

from pepperbot.adapters.onebot.event import construct_chain
from pepperbot.core.message.chain import MessageChain, chain_factory
from pepperbot.core.route.available import check_available
from pepperbot.exceptions import (
    ClassCommandDefinitionError,
    ClassCommandOnExit,
    PatternFormatError,
)
from pepperbot.extensions.command.pattern import parse_pattern
from pepperbot.extensions.command.sender import CommandSender
from pepperbot.extensions.command.utils import meet_command_exit, meet_command_prefix
from pepperbot.extensions.log import debug_log, logger
from pepperbot.store.command import ClassCommandStatus, CommandConfig, HistoryItem
from pepperbot.store.event import EventHandlerKwarg, EventMetadata
from pepperbot.store.meta import class_command_config_mapping, class_command_mapping
from pepperbot.types import T_ConversationType, T_DispatchHandler, T_StopPropagation
from pepperbot.utils.common import await_or_sync, fit_kwargs

COMMAND_LIFECYCLE_EXCEPTIONS: Dict = {
    ClassCommandOnExit.__name__: "exit",
}
""" 这些生命周期通过抛出异常触发 
finish是通过else:调用
timeout需要在定时器中单独处理
"""

LIFECYCLE_WITHOUT_PATTERNS = ("exit", "timeout", "catch", "finish", "cleanup")
""" 这些生命周期不应支持pattern 

或者说，除了initial，其他的生命周期都不应该支持pattern

不允许直接return self.finish
"""


COMMAND_COMMON_KWARGS = (
    EventHandlerKwarg(name="raw_event", type_=Union[Dict, dict]),
    EventHandlerKwarg(name="chain", type_=MessageChain),
    EventHandlerKwarg(name="sender", type_=CommandSender),
    EventHandlerKwarg(name="history", type_=Deque[HistoryItem]),
    EventHandlerKwarg(name="context", type_=Union[Dict, dict]),
    EventHandlerKwarg(name="config", type_=Any),
    EventHandlerKwarg(name="stop_propagation", type_=T_StopPropagation),
)

COMMAND_DEFAULT_KWARGS = {
    "initial": (
        *COMMAND_COMMON_KWARGS,
        EventHandlerKwarg(name="prefix", type_=str),
        EventHandlerKwarg(name="alias", type_=str),
    ),
    "exit": (*COMMAND_COMMON_KWARGS,),
    "timeout": (*COMMAND_COMMON_KWARGS,),
    "catch": (
        *COMMAND_COMMON_KWARGS,
        EventHandlerKwarg(name="exception", type_=Exception),
    ),
    "finish": (*COMMAND_COMMON_KWARGS,),
}
"""
用于检查用户定义的方法的参数的类型注解是否合法
也就是说，所有用户在对应方法中(比如initial)可用的参数及其类型，都应该出现在此处
这里并不需要像class_handler中一样，提供value，因为会在run_class_method中直接注入
 """


async def get_and_run_lifecycle(
    command_name,
    command_method_mapping,
    pointer,
    event_handler_name: str,
    parent_locals: dict,
):
    command_method_cache = command_method_mapping.get(event_handler_name)
    if not command_method_cache:
        logger.info(f"指令 <lc>{command_name}</lc> 未定义生命周期 <lc>{event_handler_name}</lc>")
        return

    if event_handler_name == "catch":
        logger.error(f"指令 {command_name} 的 {pointer} 方法执行出错，开始执行用户定义的异常捕获")
    else:
        logger.info(
            f"开始执行指令 <lc>{command_name}</lc> 的生命周期 <lc>{event_handler_name}</lc>"
        )

    await run_class_command_method(
        event_handler_name, command_method_cache.method, parent_locals
    )


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

    status = command_kwargs["status"]

    try:
        if running and meet_command_exit(
            command_kwargs["chain"], command_kwargs["command_config"]
        ):
            logger.info(
                f"<y>{command_kwargs['chain'].pure_text}</y> 满足指令 {command_name} 的退出条件"
            )
            raise ClassCommandOnExit()  # TODO 一并传递触发exit生命周期的exit_pattern，作为参数

        logger.info(f"开始执行指令 <lc>{command_name}</lc> 的 <lc>{pointer}</lc> 方法")

        # 当前指向的方法，或者说，当前激活的命令回调方法
        command_method_cache = command_method_mapping[pointer]

        # locals中需要
        # 如果解析出错，会直接抛出异常，所以不会修改pointer的指向
        # TODO 这里抛出FormatException，不应该触发cleanup
        returned_method_name = "has not set yet"
        target_method_name, command_kwargs["patterns"] = await parse_pattern(
            event_metadata,
            class_command_cache,
            command_method_cache,
            pointer,
            command_kwargs,
            command_name,
            status,
        )

        status.last_updated_time = time.time()
        await status.update()

        # target_method = command_method_cache.method
        target_method = command_method_mapping[target_method_name].method
        returned_method = await run_class_command_method(
            pointer, target_method, command_kwargs, running=running
        )

        # 判断是否正常退出
        returned_method_name = returned_method.__name__ if returned_method else "None"
        debug_log(
            title=f"方法 <lc>{pointer}</lc> 返回的下一步指向 <lc>{returned_method_name}</lc>",
        )
        # check_returned_method(
        #     command_name,
        #     command_method_names,
        #     returned_method_name,
        #     returned_method,
        # )

        # 设置下一次执行时要调用的方法
        await update_command_pointer(status, command_kwargs, returned_method_name)

    except PatternFormatError:
        #  PatternError，不应该被catch生命周期捕获
        # 同时，也不应触发其他生命周期，比如finish和cleanup
        pass

    except ClassCommandOnExit:
        # 当触发生命周期时，立即调用，而不是等到用户下一次交互

        try:
            # exception_name: str = exception.__class__.__qualname__  # type:ignore

            # 触发finally
            # 在调用生命周期之前调用，就相当于try、catch了一下
            returned_method_name = "None"

            await get_and_run_lifecycle(
                command_name,
                command_method_mapping,
                pointer,
                "exit",
                command_kwargs,
            )

        except Exception as exception:
            if "catch" in command_method_names:
                returned_method_name = "None"

                await get_and_run_lifecycle(
                    command_name,
                    command_method_mapping,
                    pointer,
                    "catch",
                    command_kwargs,
                )

            else:
                # finally保证cleanup一定会被调用，这里不需要手动调用
                has_unhandled_exception = True
                raise exception from exception

    except Exception as exception:
        # 调用生命周期，包括catch，自身出现的异常

        if "catch" in command_method_names:
            returned_method_name = "None"

            await get_and_run_lifecycle(
                command_name,
                command_method_mapping,
                pointer,
                "catch",
                command_kwargs,
            )

        else:
            # finally保证cleanup一定会被调用，这里不需要手动调用
            has_unhandled_exception = True
            raise exception from exception

    else:
        if returned_method_name != "None":
            return

        try:
            returned_method_name = "None"

            await get_and_run_lifecycle(
                command_name,
                command_method_mapping,
                pointer,
                "finish",
                command_kwargs,
            )
        except Exception as exception:
            if "catch" in command_method_names:
                await get_and_run_lifecycle(
                    command_name,
                    command_method_mapping,
                    pointer,
                    "catch",
                    command_kwargs,
                )

            else:
                # finally保证cleanup一定会被调用，这里不需要手动调用
                has_unhandled_exception = True
                raise exception from exception

    finally:
        # returned_method_name == "None" ，说明指令正常结束
        # has_unhandled_exception，说明指令出现了异常
        # 只有这两种情况，才需要重置指令状态
        if returned_method_name != "None" and not has_unhandled_exception:
            return

        try:
            # 存在本身，会影响has_running_command的判断
            await status.delete()
            # await update_command_pointer(
            #     status, "initial", raw_event, chain, reset=True
            # )
        except Exception as exception:
            logger.error(f"无法重置指令 <lc>{command_name}</lc> 的状态")

        await get_and_run_lifecycle(
            command_name, command_method_mapping, pointer, "cleanup", command_kwargs
        )


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

    match command_config.interactive_strategy:
        case "same_source_same_user":  # 群/channel/私聊中，仅对应的用户(自己)可以触发
            filter_kwargs.update(
                conversation_type=cast(
                    T_ConversationType, event_metadata.conversation_type
                ),
                conversation_id=event_metadata.source_id,
                user_id=event_metadata.user_id,
            )

        case "same_source_any_user":  # 群/channel/私聊中，任意用户(私聊只有一个用户)都可以触发
            filter_kwargs.update(
                conversation_type=cast(
                    T_ConversationType, event_metadata.conversation_type
                ),
                conversation_id=event_metadata.source_id,
                user_id="any",
            )

        case "any_source_same_user":  # 跨source锁定用户，不管他是通过群/channel/私聊和bot交互的
            filter_kwargs.update(
                conversation_type="any",
                conversation_id="any",
                user_id=event_metadata.user_id,
            )

        case "any_source_any_user":  # 所有消息渠道的所有用户都可以触发
            filter_kwargs.update(
                conversation_type="any",
                conversation_id="any",
                user_id="any",
            )

        case _:
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


async def has_running_command(
    event_meta: EventMetadata, class_command_config_ids: Set[str]
) -> tuple[bool, T_DispatchHandler]:
    # TODO 直接设置正在running的指令，不需要再去数据库中查询

    for class_command_config_id in class_command_config_ids:
        class_command_config_cache = class_command_config_mapping[
            class_command_config_id
        ]
        command_name = class_command_config_cache.class_command_name
        command_config = class_command_config_cache.command_config

        status, created = await get_command_status(
            event_meta, command_name, command_config
        )
        # if not created:

        # pointer = status.pointer
        if status.running:
            return True, (
                class_command_config_cache.command_config.propagation_group,
                class_command_config_cache.command_config.priority,
                class_command_config_cache.command_config.concurrency,
                "class_commands",
                class_command_config_id,
            )
        # if pointer != "initial":

    return False, ("", 0, False, "class_commands", "")


async def find_first_available_command(
    ordered_command_handlers: List[T_DispatchHandler],
    event_metadata: EventMetadata,
) -> Tuple[bool, T_DispatchHandler]:
    """只有没有running的指令时，才会执行这个函数"""

    for (
        propagation_group,
        priority,
        concurrency,
        handler_type,
        class_command_config_id,
    ) in ordered_command_handlers:
        class_command_config_cache = class_command_config_mapping[
            class_command_config_id
        ]
        command_name = class_command_config_cache.class_command_name
        command_config = class_command_config_cache.command_config

        meet_prefix, prefix_with_alias, prefix, alias = meet_command_prefix(
            await construct_chain(event_metadata),
            command_name,
            command_config,
        )

        class_command_cache = class_command_mapping[command_name]
        command_method_mapping = class_command_cache.command_method_mapping
        command_method_cache = command_method_mapping["initial"]

        # 先判断是否满足前缀，在判断available，
        # 1.因为判断前缀性能开销比较小，失败的话，直接就不用判断available了
        # 2.checker的参数中，需要有prefix_with_alias，所以需要先判断前缀

        if not meet_prefix:
            logger.info(f"该事件不满足指令 {command_name} {class_command_config_id} 的执行条件")
            # logger.info(f"<y>{chain.pure_text}</y> 不满足指令 <lc>{command_name}</lc> 的执行条件")
            continue

        else:
            # TODO 优化一下这里的性能，不要重复构造这么多次chain、sender之类
            # 可以直接在handle_event够构造，全局使用
            # class_handle也是，现在是每个event_handler中，如果用到了chain，都会重新构造一次
            command_kwargs = await construct_command_kwargs(
                event_metadata, class_command_config_id, lambda: None, False
            )

            # TODO 现在的实现，initial会触发两次available检查
            available = await check_available(
                command_method_cache.method, command_kwargs, is_class=False
            )
            if not available:
                logger.info(
                    f"该事件不满足指令 {command_name} {class_command_config_id} 的available校验"
                )
                continue

            # TODO 应该不存在重复的config_id的可能性
            # 哪怕class相同、priority相同，只要调用了多次as_command，则config_id一定不同
            # 如果只调用了一次as_command，那只会出现一次config_id
            return True, (
                propagation_group,
                priority,
                concurrency,
                handler_type,
                class_command_config_id,
            )

    return False, ("", 0, False, "class_commands", "__does_not_exist__")


# async def is_class_command_available(
#     event_metadata: EventMetadata,
#     class_command_config_id: str,
#     chain: MessageChain,
# ):
#     class_command_config_cache = class_command_config_mapping[class_command_config_id]
#     command_name = class_command_config_cache.class_command_name
#     command_config = class_command_config_cache.command_config

#     status, created = await get_command_status(
#         event_metadata, command_name, command_config
#     )

#     # 理论上来说，如果没有running，然后触发了这个判断，那么这里的pointer一定是initial
#     # 因为如果status已经存在，那就是running，如果不存在，新建的时候pointer就是initial
#     # 所以这里没必要判断
#     # pointer = status.pointer
#     # if not pointer == "initial":
#     #     return "", "", "", ""

#     meet_prefix, final_prefix, prefix, alias = meet_command_prefix(
#         chain,
#         command_name,
#         command_config,
#     )

#     if meet_prefix:
#         logger.info(f"<y>{chain.pure_text}</y> 满足指令 <lc>{command_name}</lc> 的执行条件")
#         return command_name, final_prefix, prefix, alias

#     else:
#         logger.info(f"<y>{chain.pure_text}</y> 不满足指令 <lc>{command_name}</lc> 的执行条件")

#         return "", "", "", ""


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

    # locals中需要prefix和alias，作为initial的可选参数
    # 如果一直return self.initial，那么从第二次运行开始，需要手动获取一下prefix和alias
    prefix = context.get("prefix")
    alias = context.get("alias")

    if not prefix or not alias:
        # if not running:
        # 没有正在运行中的指令，则需要找到一个可用的指令
        # 所以都需要判断一下，是否满足条件

        # locals中需要prefix和alias，作为initial的可选参数
        meet_prefix, prefix_with_alias, prefix, alias = meet_command_prefix(
            chain,
            command_name,
            command_config,
        )

        # if not meet_prefix:
        #     logger.info(f"该事件不满足指令 {command_name} {class_command_config_id} 的执行条件")
        #     # logger.info(f"<y>{chain.pure_text}</y> 不满足指令 <lc>{command_name}</lc> 的执行条件")
        #     return

        # logger.info(
        #     f"<y>{chain.pure_text}</y> 满足指令 <lc>{command_name}</lc> {class_command_config_id} 的执行条件"
        # )

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


async def run_class_command_method(
    method_name, method, all_locals: Dict, running=True
) -> Any:
    """通过running，避免刚好指令第一次触发时 + available应用到initial上，导致available被判断两次"""

    # debug_log(all_locals, title="当前可用变量")

    injected_kwargs = dict(
        raw_event=all_locals["raw_event"],
        chain=all_locals["chain"],
        sender=all_locals["sender"],
        # history=parse_obj_as(list[HistoryItem], all_locals["status"].history),
        history=all_locals["history"],
        # context=all_locals["status"].context,
        context=all_locals["context"],
        config=all_locals["command_config"].config,
        stop_propagation=all_locals["stop_propagation"],
    )

    if method_name == "catch":
        injected_kwargs["exception"] = all_locals["exception"]

    else:
        if method_name == "initial":
            injected_kwargs["alias"] = all_locals["alias"]
            injected_kwargs["prefix"] = all_locals["prefix"]

        if method_name not in LIFECYCLE_WITHOUT_PATTERNS:
            injected_kwargs = {**injected_kwargs, **all_locals["patterns"]}

    debug_log(injected_kwargs, title=f"将被注入 <lc>{method_name}</lc> 的参数")

    if running:  # not running的情况，find_first_available已经检查过了
        available = await check_available(method, injected_kwargs, is_class=False)
        debug(available)

        if not available:
            return method_name

    returned_method = await await_or_sync(method, **fit_kwargs(method, injected_kwargs))

    return returned_method


def check_returned_method(
    command_name: str,
    method_names: Iterable[str],
    returned_method_name: str,
    returned_method: Any,
):
    """运行时检查，和ast检查不冲突

    TODO 这个函数没有存在的必要，我一开始是担心eval之类的问题，但是这个完全可以在ast检查的时候就检查出来
    """

    # 所有生命周期不会调用check_returned_method，所以不用排除
    if returned_method == None:  # 流程正常退出，应该触发else段
        # raise ClassCommandOnFinish()
        return

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


async def check_command_timeout():
    """应该主动进行超时判断，而不是接收到该用户消息时"""

    logger.info("检查指令是否超时……")

    timeout_status: List[int] = []
    """ 不要在迭代字典的过程中，动态的修改字典 """

    for status in await ClassCommandStatus.objects.all():
        # initial的也要删啊
        # pointer = status.pointer
        # if pointer == "initial":
        #     continue

        if not status.running:
            await status.delete()
            continue

        last_updated_time = status.last_updated_time
        timeout = status.timeout
        current_time = time.time()

        # 超时判断，与上一条消息的createTime判断
        if current_time < last_updated_time + timeout:
            continue

        logger.info(
            f"<lc>{status.protocol}</lc> <lc>{status.conversation_type}</lc> 模式中的"
            + f"<lc>{status.conversation_id}</lc> 指令 <lc>{status.command_name}</lc> 已超时"
        )

        history: List[HistoryItem] = pickle.loads(status.history)
        context = pickle.loads(status.context)

        def stop_propagation():
            context["stop_propagation"] = True

        if not len(history):
            logger.error(f"如果要执行timeout生命周期，history_size至少为1")
            timeout_status.append(status.id)
            continue

        history_item = history[-1]

        # 考虑到重启后，指令cache会丢失，而数据库中还存在的情况
        class_command_config_cache = class_command_config_mapping.get(status.config_id)
        if not class_command_config_cache:
            logger.error(
                f"指令 <lc>{status.command_name}</lc> {status.config_id} 的cache已被删除，可能是重启worker导致的"
            )
            timeout_status.append(status.id)
            continue

        command_config = class_command_config_cache.command_config  # locals中需要
        command_name = class_command_config_cache.class_command_name
        class_command_cache = class_command_mapping[command_name]
        command_method_mapping = class_command_cache.command_method_mapping
        command_method_names = command_method_mapping.keys()

        # locals中需要
        raw_event = history_item.raw_event
        chain = history_item.chain
        from pepperbot.core.event.handle import construct_event_metadata

        event_metadata = construct_event_metadata(status.protocol, raw_event)
        # chain = await chain_factory(event_metadata)
        sender = CommandSender(event_metadata)

        pointer = "timeout"

        try:
            lifecycle_handler = command_method_mapping.get(pointer)
            if not lifecycle_handler:
                logger.info(
                    f"指令 <lc>{command_name}</lc> 未定义生命周期 <lc>{pointer}</lc>，直接结束指令"
                )
                timeout_status.append(status.id)
                continue

            logger.info(f"开始执行指令 <lc>{command_name}</lc> 的生命周期 <lc>{pointer}</lc>")

            command_method_cache = command_method_mapping[pointer]
            target_method = command_method_cache.method

            # 不阻塞事件响应
            await run_class_command_method(pointer, target_method, locals())

        except Exception as exception:
            if "catch" in command_method_names:
                await get_and_run_lifecycle(
                    command_name, command_method_mapping, pointer, "catch", locals()
                )

            else:
                raise exception from exception

        else:
            # 只需要执行一次timeout lifecycle，不需要考虑pointer的问题
            await get_and_run_lifecycle(
                command_name, command_method_mapping, pointer, "finish", locals()
            )

        finally:
            try:
                timeout_status.append(status.id)
                await status.delete()
                # await update_command_pointer(
                #     status, "initial", raw_event, chain, reset=True
                # )
            except Exception as exception:
                logger.error(f"无法重置指令 <lc>{command_name}</lc> 的状态")

            await get_and_run_lifecycle(
                command_name, command_method_mapping, pointer, "cleanup", locals()
            )

    for status_id in timeout_status:
        await ClassCommandStatus.objects.filter(id=status_id).delete()


# async def run_command_method_with_lifecycle():
