from typing import Any, Callable, Dict, Iterable, Literal, Protocol, TypeVar, Union


F = TypeVar("F", bound=Callable[..., Any])


class API_Caller_T(Protocol):
    def __call__(self, action: str, **kwargs: Any) -> Any:
        ...


class HandlerValue_T(Protocol):
    def __call__(self, event: Dict[str, Any], **kwargs: Any) -> Any:
        ...


class CommandClassBase:
    pass


T_BotProtocol = Literal["onebot", "keaimao"]
ALL_AVAILABLE_BOT_PROTOCOLS: Iterable[T_BotProtocol] = ["onebot", "keaimao"]

T_RouteModes = Literal["group", "private"]
T_RouteValidator = Callable[[str, Union[int, str]], bool]
T_WebProtocol = Literal["http", "websocket"]
T_RouteGroups = Union[
    Literal["*"],
    Dict[Literal["onebot", "keaimao"], Union[Literal["*"], Iterable[Union[int, str]]]],
    T_RouteValidator,  # 平台，群号
]
