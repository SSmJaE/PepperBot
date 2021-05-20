from functools import wraps
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Dict,
    List,
    Literal,
    Optional,
    TypeVar,
    Union,
    cast,
)

from devtools import debug
from pydantic.main import BaseModel
from src.exceptions import EmptySelectionException


class ContextItem(BaseModel):
    action: str
    payload: Optional[Any]
    args: Optional[List[Any]]
    kwargs: Optional[Dict]


class RunnerType:
    context: List[ContextItem]
    selections: List[Any]
    selectionType: Union[Literal["group", "user"]]


END_POINTS = []

# # 之所以使用外部context，而不是挂载到class或实例上，是因为复用选择的缘故
# # 还有并发时的锁的问题
# runnerContext = {}


# if TYPE_CHECKING:
BranchableChain = TypeVar(
    "BranchableChain",
    RunnerType,
    RunnerType
    # MultiGroupAction,
    # MultiUserAction,
    # SingleGroupAction,
    # SingleUserAction,
)


# todo 装饰器，参数类型丢失

F = TypeVar("F", bound=Callable[..., Any])


def permission(f: F) -> F:
    @wraps(f)
    def wrapper(self: BranchableChain, *args, **kwargs) -> BranchableChain:

        return f(self, *args, **kwargs)

    return cast(F, wrapper)


def end_point(func: F) -> F:
    @wraps(func)
    def wrapper(self: BranchableChain, *args, **kwargs):
        END_POINTS.append(func.__name__)

        debug(func.__name__)

        context = self.context

        chainClass = self.__class__

        instance = chainClass()

        item = ContextItem(action=func.__name__, args=[*args], kwargs={**kwargs})
        instance.context = [*context, item]

        # self.clone = [*buffer]
        # self.context = deepcopy(self.context)
        return func(instance, *args, **kwargs)

    return cast(F, wrapper)


def schedule(f: F) -> F:
    @wraps(f)
    def wrapper(self: BranchableChain, *args, **kwargs) -> BranchableChain:
        debug(f.__name__)

        context = self.context

        chainClass = self.__class__

        instance = chainClass()

        item = ContextItem(action=f.__name__, args=[*args], kwargs={**kwargs})
        instance.context = [*context, item]

        # self.clone = [*buffer]
        # self.context = deepcopy(self.context)
        return f(instance, *args, **kwargs)

    return cast(F, wrapper)


def ensure_not_empty_selection(f: F) -> F:
    # todo 当当前选择的group被exclude之后，如果此时选择的group为零，raise EmptySelectException
    @wraps(f)
    def wrapper(self: BranchableChain, *args, **kwargs) -> BranchableChain:
        if not len(self.selections):
            raise EmptySelectionException

        return f(self, *args, **kwargs)

    return cast(F, wrapper)
