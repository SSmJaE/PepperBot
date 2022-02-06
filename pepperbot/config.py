from typing import Union
from pydantic import BaseSettings


class Debug(BaseSettings):
    test_mode = False
    """ 单元测试用 """

    enable_proxy = False
    proxy = {
        "http://": "http://localhost:8866",
        "https://": "http://localhost:8866",
    }


class Logger(BaseSettings):
    level: Union[str, int] = "DEBUG"
    write_to_log: bool = False


class Sqlite(BaseSettings):
    path = "./{id}.sqlite3"


class GlobalConfig(BaseSettings):
    debug = Debug()
    logger = Logger()
    sqlite = Sqlite()


global_config = GlobalConfig()
