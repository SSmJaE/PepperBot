from __future__ import annotations

import better_exceptions
from better_exceptions import encoding

from .initial import PepperBot

__version__ = "0.3.1"
__all__ = ("PepperBot", "__version__")

# https://github.com/Qix-/better-exceptions/issues/53
# 中文windows默认编码是gb2312，管道符号无法正常显示，手动设置为utf-8
encoding.ENCODING = "utf-8"

better_exceptions.hook()
