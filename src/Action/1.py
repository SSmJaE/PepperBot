from functools import wraps
from typing import Any, Callable, ForwardRef, TypeVar, cast

BranchableChain = TypeVar(
    "BranchableChain",
    ForwardRef("SingleGroupAction"),
    "SingleGroupAction",
)


F = TypeVar("F", bound=Callable[..., Any])


def schedule(f: F) -> F:
    @wraps(f)
    def wrapper(self: BranchableChain, *args, **kwargs) -> BranchableChain:
        BranchableChain.test
        pass

    return cast(F, wrapper)


class SingleGroupAction:
    test: int

    @schedule
    def send_message(self):
        return self
