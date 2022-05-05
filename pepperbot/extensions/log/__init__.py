import inspect
import logging
import os
import sys
from typing import Any, Dict

from devtools.prettier import pformat
from loguru import logger
from pepperbot.config import global_config


def formatter(record: Dict):
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


def debug_log(message: Any, title: str = ""):
    frame = inspect.stack()[1]
    file_path = frame.filename
    lineno = frame.lineno

    logger.bind(title=title, file_path=file_path, lineno=lineno).debug("")

    if global_config.logger.level <= 10:  # DEBUG
        print(pformat(message, highlight=True))


logging.getLogger("apscheduler").setLevel(global_config.logger.level)

__all__ = (
    "logger",
    "debug_log",
)
