# from functools import wraps
# from typing import Callable, TypeVar
# from typing_extensions import ParamSpec
# from pepperbot.types import F, T_BotProtocol
# from pepperbot.store.meta import api_callers


# P = ParamSpec("P")
# R = TypeVar("R")


# def add_logging(f: Callable[P, R]) -> Callable[P, Awaitable[R]]:
#     async def inner(*args: P.args, **kwargs: P.kwargs) -> R:
#         await log_to_database()
#         return f(*args, **kwargs)

#     return inner


# def with_api_caller(protocol: T_BotProtocol):
#     api_caller = api_callers.get(protocol)

#     def has_api_caller(f: F) -> F:
#         @wraps(f)
#         def wrapper():
#             api_caller
#             pass

#         return wrapper

#     return has_api_caller


# with_onebot_api_caller = with_api_caller("onebot")
