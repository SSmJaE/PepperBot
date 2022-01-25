from pydantic import BaseModel


class GlobalConfig(BaseModel):
    class Debug:
        test_mode = False
        """ 单元测试用 """

        enable_proxy = False
        proxy = {
            "http://": "http://localhost:8866",
            "https://": "http://localhost:8866",
        }

    class Logger:
        level = "debug"
        write_to_log: bool = False

    class Sqlite:
        path = "./{id}.sqlite3"


# todo BaseModel的子类，比如上方的Logger，是否也能runtime检测
global_config = GlobalConfig()