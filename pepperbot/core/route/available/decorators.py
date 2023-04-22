from typing import cast

from devtools import debug

from pepperbot.extensions.log import logger
from pepperbot.store.event import EventDispatchMetadata
from pepperbot.types import T_DispatchHandler


def no_pre_activate_command(
    event_dispatch_metadata: EventDispatchMetadata, dispatch_handler: T_DispatchHandler
) -> bool:
    """如果有比当前优先级更高的命令正在运行，那么不执行当前handler"""

    # debug(event_dispatch_metadata)
    # debug(dispatch_handler)

    if (
        event_dispatch_metadata.has_running_command
        or event_dispatch_metadata.has_available_command
    ):
        command_handler = cast(
            T_DispatchHandler, event_dispatch_metadata.command_dispatch_handler
        )

        # 指令状态应该是全局的
        # if not command_handler[0] == dispatch_handler[0]:
        #     logger.info(
        #         f"运行的指令 {command_handler} 和当前handler {dispatch_handler} 不在同一个传播组，可以执行"
        #     )
        #     return True

        if command_handler[1] > dispatch_handler[1]:
            logger.info(
                f"存在比当前handler {dispatch_handler} 更高优先级的命令 {command_handler} 正在运行，不执行当前handler"
            )
            return False

    return True
