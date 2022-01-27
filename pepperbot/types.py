from typing import Any, Callable, Dict, Iterable, Literal, Protocol, TypeVar, Union


from enum import Enum


class AutoName(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name


class HandlerValue_T(Protocol):
    def __call__(self, event: Dict[str, Any], **kwargs: Any) -> Any:
        ...


class BaseClassCommand:
    pass


class BaseBot:
    pass


F = TypeVar("F", bound=Callable[..., Any])

T_WebProtocol = Literal["http", "websocket"]
T_BotProtocol = Literal["onebot", "keaimao", "telegram"]
T_RouteMode = Literal["group", "private", "channel"]
T_RouteValidator = Callable[[str, Union[int, str]], bool]
T_RouteRelation = Union[
    Literal["*"],
    Dict[T_BotProtocol, Union[Literal["*"], Iterable[Union[int, str]]]],
    T_RouteValidator,  # (平台，群号)
]
