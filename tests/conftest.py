import asyncio
import contextlib
import pytest

from typing import Any, Optional, cast
import pytest
from pepperbot.store.meta import onebot_event_meta
from pepperbot.store.orm import engine, metadata, database
from pepperbot.config import global_config
import os


from unittest.mock import patch

# 可以直接import tests.conftest
# base_dir = os.path.dirname(os.path.abspath(__file__))
# sys.path.append(base_dir)


@pytest.fixture(scope="session")
def event_loop():
    """Overrides pytest default function scoped event loop"""
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session", autouse=True)
async def setup_test_environment():
    # debug(global_config)

    global_config.logger.level = 10

    onebot_event_meta.has_skip_buffered_event = True

    db_path: Optional[str] = None

    if "sqlite" in global_config.database.url:
        db_path = global_config.database.url.split("///")[1]
        if os.path.exists(db_path):
            os.remove(db_path)

    else:
        if not database.is_connected:
            await database.connect()

    metadata.create_all(engine)

    yield

    if "sqlite" in global_config.database.url:
        os.remove(cast(str, db_path))

    else:
        if database.is_connected:
            await database.disconnect()


@pytest.fixture(scope="function")
async def reset_database():
    yield

    # 清空数据库
    with contextlib.closing(engine.connect()) as con:
        trans = con.begin()
        for table in reversed(metadata.sorted_tables):
            con.execute(table.delete())
        trans.commit()

    # metadata.drop_all(engine)


api_results = []


def new_caller(self, action: str, kwargs: dict[str, Any]):
    if action == "get_login_info":
        return {"user_id": "123456789", "nickname": "测试机器人"}

    else:
        api_results.append((action, kwargs))


@pytest.fixture(scope="class")
def patch_api_caller():
    with patch(
        "pepperbot.core.api.api_caller.ApiCaller.to_onebot",
        new=new_caller,
        # create=True,
    ) as patched:
        yield patched


@pytest.fixture(scope="function")
def reset_api_results():
    yield

    api_results.clear()
