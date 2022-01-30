from typing import Any, Dict, Tuple

from pepperbot.types import T_BotProtocol


class BaseMessageSegment:
    identifier: Any
    """ 用来判断两个segment是否一致 """
    universal: Tuple[T_BotProtocol, ...]

    onebot: Dict[str, Any]
    keaimao: Any

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
