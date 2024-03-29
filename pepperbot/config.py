import logging
from typing import Union

from pydantic import BaseModel, BaseSettings


class Debug(BaseModel):
    test_mode = False
    """ 单元测试用 """

    enable_proxy = False
    proxy = {
        "http://": "http://localhost:8866",
        "https://": "http://localhost:8866",
    }


class Logger(BaseModel):
    level: int = logging.INFO
    write_to_log: bool = False


class Database(BaseModel):
    url = "sqlite:///db.sqlite3"


class GlobalConfig(BaseSettings):
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        env_prefix = "p_"
        env_nested_delimiter = "__"

    debug = Debug()
    logger = Logger()
    database = Database()


global_config = GlobalConfig()
