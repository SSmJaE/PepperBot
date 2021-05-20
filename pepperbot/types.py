from typing import Any, Callable, Dict, Protocol, TypeVar


F = TypeVar("F", bound=Callable[..., Any])


class API_Caller_T(Protocol):
    def __call__(self, action: str, **kwargs: Any) -> Any:
        ...


class HandlerValue_T(Protocol):
    def __call__(self, event: Dict[str, Any], **kwargs: Any) -> Any:
        ...


class CommandClassBase:
    pass
