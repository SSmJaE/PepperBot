from __future__ import annotations
import logging

import os
import sys
from typing import Dict

from loguru import logger
from pepperbot.config import global_config


def formatter(record: Dict):
    level = record["level"].name

    # todo 显示对应的bot_protocol
    file_path: str = record["file"].path
    if "pepperbot" in file_path:
        displayed_path = "pepperbot"
    else:
        displayed_path = os.path.relpath(file_path, os.getcwd())

    if level == "DEBUG":
        return (
            "<g>{time:MM-DD HH:mm:ss}</g> | <lvl>{level}</lvl>\n"
            + f"{file_path}:{record['line']}\n"
            + "{message}\n"
        )

    else:
        return (
            "<g>{time:MM-DD HH:mm:ss}</g> | <lvl>{level:^7}</lvl> | "
            + f"{displayed_path} | "
            + "{message}"
            + "\n{exception}"
        )


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

logging.getLogger("apscheduler").setLevel(global_config.logger.level)


__all__ = ("logger",)
