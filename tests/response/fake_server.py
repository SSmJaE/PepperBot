import inspect
from functools import wraps
from typing import Any, Callable, Dict, List, Optional, Tuple, cast

import pretty_errors
from devtools import debug
from loguru import logger
from pydantic.main import BaseModel
from pepperbot.globals import GLOBAL_CONFIG
from pepperbot.main import handle_qq_event
from pepperbot.parse import GROUP_EVENTS_T
from pepperbot.parse.cache import cache
from pepperbot.parse.figure import figure_out
from pepperbot.types import F
from pepperbot.utils.common import await_or_normal
from pepperbot.utils.mixins import ActionMixin, GroupMessageMixin

pretty_errors.configure(
    filename_display=pretty_errors.FILENAME_EXTENDED,
)


GLOBAL_CONFIG["TEST_MODE"] = True


async def test_entry(receive: Dict):

    eventName: Optional[GROUP_EVENTS_T] = None
    try:
        eventName = figure_out(receive)
    except KeyError:
        logger.debug(receive)

    if eventName:
        await handle_qq_event(receive, eventName)
    else:
        logger.warning("未注册的事件类型")
        logger.debug(receive)


async def noop():
    pass


class APIResult(BaseModel):
    action: str
    data: Dict[str, Any]


class FakeAPI(GroupMessageMixin, ActionMixin):
    def __init__(
        self,
    ):
        self.results: List[APIResult] = []

    def clear(self):
        self.results = []

    async def api(self, action: str, **kwargs):
        debug(action)
        self.results.append(APIResult(**{"action": action, "data": kwargs}))

        return noop


fakeApi = api = globalApi = FakeAPI()

hasInitial = False


async def test_run(event: Dict):
    global hasInitial

    if not hasInitial:
        cache()

        hasInitial = True

    await test_entry(event)

    return api.results


def test_handler(f: F) -> F:
    @wraps(f)
    async def wrapper(self, *args, **kwargs):

        for key, value in kwargs.items():
            if hasattr(value, "api"):
                value.api = fakeApi.api

        return await await_or_normal(f, self, *args, **kwargs)

    return cast(F, wrapper)
