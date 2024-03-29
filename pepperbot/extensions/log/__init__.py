import inspect
import logging
import os
import sys
from typing import Any, Dict, Optional

from devtools.prettier import pformat
from loguru import logger
from pepperbot.config import global_config


__all__ = (
    "logger",
    "debug_log",
)


def formatter(record: Dict):
    # TODO 带进程id，因为现在sanic自带worker manager了

    level = record["level"].name

    file_path: str = record["extra"].get("file_path") or record["file"].path
    if "pepperbot" in file_path:
        displayed_path = "pepperbot"
    else:
        displayed_path = os.path.relpath(file_path, os.getcwd())

    lineno = record["extra"].get("lineno") or record["line"]

    if level == "DEBUG":
        return (
            "<g>{time:MM-DD HH:mm:ss}</g> | <lvl>{level:^7}</lvl> | "
            + f"{record['extra']['title']}\n"
            + f"{file_path}:{lineno}\n"
            # + "{message}\n"
        )

    else:
        return (
            "<g>{time:MM-DD HH:mm:ss}</g> | <lvl>{level:^7}</lvl> | "
            # + f"{displayed_path} | "
            + "{message}\n"
            + "{exception}"
        )


logger.configure(extra={"title": "", "message": ""})
logger.remove()
logger.add(
    sys.stdout,  # type:ignore
    level=global_config.logger.level,
    colorize=True,
    backtrace=True,
    diagnose=True,
    # enqueue=True, # 需要阻塞式的日志输出
    format=formatter,  # type:ignore
)
logger = logger.opt(colors=True)


def debug_log(message: Optional[Any] = None, title: str = ""):
    # 获取frame就很“昂贵”，所以只有在debug模式下才会获取
    if global_config.logger.level <= 10:  # DEBUG
        frame = inspect.stack()[1]
        file_path = frame.filename
        lineno = frame.lineno

        logger.bind(title=title, file_path=file_path, lineno=lineno).debug("")

        if message:
            print(pformat(message, highlight=True))


# TODO 整合sanic的日志
# TODO 统一logging为loguru
logging.getLogger("apscheduler").setLevel(global_config.logger.level)
