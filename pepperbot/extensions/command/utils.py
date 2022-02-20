import re
import time
from typing import Any, Callable, Dict, List, Set, Tuple

from devtools import pformat
from pepperbot.core.message.chain import MessageChain
from pepperbot.core.message.segment import At
from pepperbot.store.command import CommandConfig
from pepperbot.store.meta import get_bot_id
from pepperbot.extensions.log import logger


def meet_text_prefix(
    chain: MessageChain,
    command_name: str,
    command_config: CommandConfig,
) -> Tuple[bool, str]:

    aliases: Set[str] = set(command_config.aliases)
    prefixes: Set[str] = set(command_config.prefixes)

    logger.debug(pformat(command_name))
    logger.debug(pformat(prefixes))
    logger.debug(pformat(aliases))

    if command_config.include_class_name:
        aliases.add(command_name)

    for alias in aliases:
        final_prefixes = prefixes if command_config.need_prefix else []
        for prefix in final_prefixes:
            final_prefix = prefix + alias
            logger.debug(pformat(final_prefix))
            if re.search(f"^{final_prefix}", chain.pure_text):
                return True, final_prefix

    return False, ""


def meet_command_prefix(
    chain: MessageChain,
    command_name: str,
    command_config: CommandConfig,
) -> Tuple[bool, str]:
    """
    通过command_kwargs和messageChain的pure_text，判断是否触发命令的initial
    """

    # 是否需要@机器人
    if command_config.require_at:
        bot_id = get_bot_id(chain.protocol)  # type:ignore

        if not chain.has(At(bot_id)):
            return False, ""

    meet_prefix, prefix = meet_text_prefix(chain, command_name, command_config)
    if not meet_prefix:
        return False, ""

    return True, prefix


def meet_command_exit(chain: MessageChain, command_config: CommandConfig):
    """退出判断"""

    logger.debug(pformat(command_config.exit_patterns))
    for pattern in command_config.exit_patterns:
        logger.debug(pformat(re.search(pattern, chain.pure_text)))
        if re.search(pattern, chain.pure_text):
            return True

    return False
