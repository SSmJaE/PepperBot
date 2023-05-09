import asyncio
import contextlib
import pytest

from typing import Any
from devtools import debug
import pytest
from pytest_mock import MockerFixture
from capabilities.pepperbot_gpt_example.src.config import GPTExampleConfig
from capabilities.pepperbot_gpt_example.src.main import GPTExample, GPTManage
from pepperbot.core.api.api_caller import ApiCaller
from pepperbot.core.event.handle import handle_event
from pepperbot.core.message.segment import Image
from pepperbot.extensions.command import as_command
from pepperbot.initial import PepperBot
from pepperbot.store.meta import BotRoute, get_onebot_caller, onebot_event_meta
from pepperbot.store.orm import engine, metadata, set_metadata
from pepperbot.config import global_config
import os
import sys

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
    global_config.logger.level = 10
    # debug(global_config)

    onebot_event_meta.has_skip_buffered_event = True

    db_path = global_config.database.url.split("///")[1]
    if os.path.exists(db_path):
        os.remove(db_path)

    metadata.create_all(engine)

    yield

    os.remove(db_path)


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


results = []


def new_caller(self, action: str, kwargs: dict[str, Any]):
    if action == "get_login_info":
        return {"user_id": "123456789", "nickname": "测试机器人"}

    else:
        results.append((action, kwargs))


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

    results.clear()
