import asyncio
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
from pepperbot.types import (
    T_BotProtocol,
    T_ConversationType,
    T_DispatchHandler,
    T_StopPropagation,
)
from pepperbot.utils.common import await_or_sync, fit_kwargs


async def run_timeout(status: ClassCommandStatus):
    """这里只负责运行timeout生命周期，调用这个方法，则已经判断过是否超时了，只有超时会调用这个方法"""

    from pepperbot.core.event.handle import construct_event_metadata
    from pepperbot.extensions.command.handle import (
        construct_command_kwargs,
        get_and_run_lifecycle,
        run_class_command_method,
    )

    common_prefix = (
        f"<lc>{status.protocol}</lc> <lc>{status.conversation_type}</lc> 模式中 "
        + f"<lc>{status.conversation_id}</lc> 的指令 <lc>{status.command_name}</lc> "
    )

    if status.id not in command_timeout_jobs:
        # 或是该指令从未被匹配过，也就是通过check_command_timeout()判断出来的超时
        # 从未匹配过=》该指令从未running过，所以也就没有command_timeout_jobs[status.id]，所以不需要处理
        await status.delete()

        logger.info(common_prefix + "的生命周期 <lc>timeout</lc> 已被处理")
        return

    logger.info(common_prefix + "已超时，开始处理生命周期 <lc>timeout</lc>")

    history: List[HistoryItem] = pickle.loads(status.history)

    if not len(history):
        logger.error(common_prefix + "如果要执行生命周期 <lc>timeout</lc>，history_size 至少为1")
        return

    # 考虑到重启后，指令cache会丢失(uuid会重新生成)，而数据库中还存在的情况
    class_command_config_cache = class_command_config_mapping.get(status.config_id)
    if not class_command_config_cache:
        logger.error(common_prefix + f"{status.config_id} 的cache已被删除，可能是重启worker导致的")
        return

    command_config = class_command_config_cache.command_config  # locals中需要
    command_name = class_command_config_cache.class_command_name
    class_command_cache = class_command_mapping[command_name]
    command_method_mapping = class_command_cache.command_method_mapping
    command_method_names = command_method_mapping.keys()

    history_item = history[-1]
    raw_event = history_item.raw_event
    event_metadata = construct_event_metadata(status.protocol, raw_event)

    context = pickle.loads(status.context)

    def stop_propagation():
        context["stop_propagation"] = True

    command_kwargs = await construct_command_kwargs(
        event_metadata=event_metadata,
        class_command_config_id=command_config.config_id,
        stop_propagation=stop_propagation,
        running=True,
    )

    pointer = "timeout"

    lifecycle_kwargs: Dict[str, Any] = dict(
        command_name=command_name,
        command_method_mapping=command_method_mapping,
        pointer=pointer,
        command_kwargs=command_kwargs,
    )

    try:
        lifecycle_handler = command_method_mapping.get(pointer)
        if not lifecycle_handler:
            logger.info(f"指令 <lc>{command_name}</lc> 未定义生命周期 <lc>{pointer}</lc>，直接结束指令")
            return

        logger.info(f"开始执行指令 <lc>{command_name}</lc> 的生命周期 <lc>{pointer}</lc>")

        command_method_cache = command_method_mapping[pointer]
        target_method = command_method_cache.method

        # 不阻塞事件响应
        await run_class_command_method(pointer, target_method, command_kwargs)

    except Exception as exception:
        if "catch" in command_method_names:
            lifecycle_kwargs["command_kwargs"]["exception"] = exception
            await get_and_run_lifecycle("catch", **lifecycle_kwargs)

        else:
            raise exception from exception

    finally:
        try:
            # 这里和run_class_command中的finally是对应的
            # 因为生命周期，要么走timeout，要么就是exit、catch、finish那些，只有这两个地方处理
            await status.delete()

            # 虽然对于仅运行一次的任务，apscheduler可能会自动删除，但是还是手动删除一下吧
            job = command_timeout_jobs[status.id]
            if async_scheduler.get_job(job.id):
                job.remove()

            if status.id in command_timeout_jobs:
                command_timeout_jobs.pop(status.id)

        except Exception as exception:
            logger.error(f"无法重置指令 <lc>{command_name}</lc> 的状态: {exception}")

        await get_and_run_lifecycle("cleanup", **lifecycle_kwargs)


async def check_command_timeout():
    """应该主动进行超时判断，而不是接收到该用户消息时

    以防scheduler体系没有清除干净，手动校验还是需要的，只是不需要那么频繁了

    比如，同一个用户，定义了多个交互策略，对一个事件，可能创建两个status，但是只有一个status会是running，另一个永远不会被处理
    """

    useless_status_ids: List[int] = []
    """ 不要在迭代字典的过程中，动态的修改字典 """

    timeout_tasks: List[asyncio.Task] = []

    for status in await ClassCommandStatus.objects.all():
        if not status.running:
            useless_status_ids.append(status.id)
            continue

        # 考虑到重启后，指令cache会丢失，而数据库中还存在的情况
        class_command_config_cache = class_command_config_mapping.get(status.config_id)
        if not class_command_config_cache:
            logger.error(
                f"指令 <lc>{status.command_name}</lc> {status.config_id} 的cache已被删除，可能是重启worker导致的"
            )
            useless_status_ids.append(status.id)
            continue

        last_updated_time = status.last_updated_time
        timeout = status.timeout
        current_time = time.time()

        # 超时判断，与上一条消息的createTime判断
        # +5 ，是为了给apscheduler一点调度的时间，防止刚好同时触发
        # 同时，因为这个函数的间隔是10,5 < 10，所以不会导致相邻两次调用都认为超时——每10秒调用一次这个主动超时判断函数
        if current_time > last_updated_time + timeout + 5:
            # run_timeout中会主动删除status.id，这里没必要append到useless_status_ids里了
            task = asyncio.create_task(run_timeout(status))
            timeout_tasks.append(task)
            continue

    for status_id in useless_status_ids:
        try:
            await ClassCommandStatus.objects.filter(id=status_id).delete()

        except:
            logger.error(f"无法删除指令状态 {status_id}")

    await asyncio.gather(*timeout_tasks)
