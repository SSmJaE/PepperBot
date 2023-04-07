import re
import time
from typing import Any, Callable, Dict, Iterable, List, Sequence, Set, Tuple

from devtools import pformat
from pepperbot.core.message.chain import MessageChain
from pepperbot.core.message.segment import At
from pepperbot.store.command import CommandConfig
from pepperbot.store.meta import get_bot_id
from pepperbot.extensions.log import debug_log, logger


from devtools import debug


def meet_text_prefix(
    chain: MessageChain,
    command_name: str,
    command_config: CommandConfig,
) -> Tuple[bool, str, str, str]:

    aliases: Set[str] = set(command_config.aliases)
    if command_config.include_class_name:
        aliases.add(command_name)
    # aliases.add("")  # 保证下方循环至少执行一次

    if command_config.need_prefix:
        prefixes: Iterable[str] = set(command_config.prefixes)
    else:  # 保证下方循环至少执行一次
        prefixes = [""]

    debug_log(command_name, "指令名")
    debug_log(prefixes, "所有前缀")
    debug_log(aliases, "所有别名")

    debug_log(chain.pure_text)

    for alias in aliases:
        for prefix in prefixes:
            final_prefix = prefix + alias

            # 如果是At + Text的情况，pure_text之前会多出一个空格
            # 因为经常性，At和Text之间，会手动加一个空格，不如不去掉，就会导致判断失效
            # 必须有^，不然，当有多个指令时，某一个final_prefix是另一个final_prefix的子集时，会导致错误匹配
            # 比如，/a和/ab，当输入/a时，会匹配到/a和/ab，此时如果/a指令在前，/ab就不会被匹配到
            if re.search(f"^{final_prefix}", chain.pure_text.strip()):
                debug_log(f"^{final_prefix} 满足 {command_name} 的执行条件")

                return True, final_prefix, prefix, alias

            else:
                debug_log(f"{final_prefix} 不满足 {command_name} 的执行条件")

    return False, "", "", ""


def meet_command_prefix(
    chain: MessageChain,
    command_name: str,
    command_config: CommandConfig,
) -> Tuple[bool, str, str, str]:
    """
    通过command_kwargs和messageChain的pure_text，判断是否触发命令的initial
    """

    # 是否需要@机器人
    if command_config.require_at:
        bot_id = get_bot_id(chain.protocol)  # type:ignore

        # debug(bot_id)
        # debug(chain.has(At(bot_id)))

        if not chain.has(At(bot_id)):
            return False, "", "", ""

    meet_prefix, final_prefix, prefix, alias = meet_text_prefix(
        chain, command_name, command_config
    )
    if not meet_prefix:
        return False, "", "", ""

    return True, final_prefix, prefix, alias


def meet_command_exit(chain: MessageChain, command_config: CommandConfig):
    """退出判断"""

    debug_log(command_config.exit_patterns, "退出正则")
    for pattern in command_config.exit_patterns:
        # debug_log(re.search(pattern, chain.pure_text))
        if re.search(pattern, chain.pure_text):
            return True

    return False
