from typing import Any, Dict, Tuple

from pepperbot.types import T_BotProtocol
from pepperbot.extensions.log import logger


class BaseMessageSegment:
    identifier: Any
    """ 用来判断两个segment是否一致 """

    def __init__(self, identifier: Any):
        self.identifier = identifier

    def __str__(self) -> str:
        return f"Segment[{self.__class__.__name__}, {self.identifier}]"

    def __repr__(self) -> str:
        return f"Segment[{self.__class__.__name__}, {self.identifier}]"

    def __eq__(self, other: "BaseMessageSegment") -> bool:
        if type(self) == type(other):
            if self.identifier == other.identifier:
                return True
        return False

    async def onebot(self):
        raise NotImplementedError

    async def keaimao(self):
        raise NotImplementedError

    async def telegram(self):
        raise NotImplementedError
