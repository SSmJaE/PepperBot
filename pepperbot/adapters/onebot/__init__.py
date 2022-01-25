from typing import Dict, Optional

from pepperbot.core.event.base import AdapaterBase
from pepperbot.extensions import logger

# from .event.event import T_GROUP_EVENTS
# from .event.figure import figure_out
# from .handle import handle_onebotV11_event


class OnebotV11Adapter(AdapaterBase):
    # api_caller: T_api_caller

    # @staticmethod
    # def preprocess_event(raw_event: Dict):
    #     event_name: Optional[T_GROUP_EVENTS] = None
    #     try:
    #         event_name = figure_out(raw_event)
    #     except KeyError:
    #         logger.error("onebot事件解析失败")
    #         logger.debug(raw_event)

    #     return event_name

    # @staticmethod
    # async def dispatch_event_to_handler(event_name: str, raw_event: Dict):
        # await handle_onebotV11_event(raw_event, event_name)

    # def call_api(self, action: str, **kwargs):
    #     self.api_caller(action, kwargs)

    @staticmethod
    async def get_kwargs(event_name: str, raw_event: Dict):
        pass
