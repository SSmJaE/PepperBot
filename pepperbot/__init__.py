from __future__ import annotations

import better_exceptions
from better_exceptions import encoding

from pepperbot.extensions.log import logger
from pepperbot.extensions.scheduler import async_scheduler
from pepperbot.store.meta import BotRoute

from .initial import PepperBot

__version__ = "0.3.4"
__all__ = (
    "__version__",
    "PepperBot",
    "logger",
    "async_scheduler",
    "BotRoute",
)

# https://github.com/Qix-/better-exceptions/issues/53
# 中文windows默认编码是gb2312，管道符号无法正常显示，手动设置为utf-8
encoding.ENCODING = "utf-8"

better_exceptions.hook()
