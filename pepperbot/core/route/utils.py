import json
import traceback
from typing import Iterable
from sanic import Sanic
from pepperbot.core.event.base import AdapaterBase
from pepperbot.core.event.handle import handle_event
from pepperbot.core.route.parse import parse_routes
from pepperbot.extensions.logger import logger
from pepperbot.store.meta import AdapterBuffer, BotRoute
from pepperbot.types import T_BotProtocol
from devtools import debug


def create_web_routes(app: Sanic, adapter: AdapterBuffer):
    if adapter.receive_protocol == "http":
        app.add_route(
            handler=adapter.request_handler,
            uri=adapter.uri,
            methods=["POST"],
        )

    else:
        app.add_websocket_route(
            handler=adapter.request_handler,
            uri=adapter.uri,
        )


def create_bot_routes(routes: Iterable[BotRoute]):
    parse_routes(routes)


async def http_receiver(request, protocol: T_BotProtocol, adapter: AdapaterBase):
    try:
        await handle_event(protocol, adapter, request.json)
    except Exception as e:
        logger.error(e)
        traceback.print_exc()

async def websocket_receiver(
    request, ws, protocol: T_BotProtocol, adapter: AdapaterBase
):
    while True:
        try:
            data = await ws.recv()
            raw_event = json.loads(data)

            debug(raw_event)
            await handle_event(protocol, adapter, raw_event)
        except Exception as e:
            logger.error(e)
            traceback.print_exc()
