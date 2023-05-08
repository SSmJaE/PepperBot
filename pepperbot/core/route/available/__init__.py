import asyncio
from collections import OrderedDict
from functools import wraps
from inspect import isclass
from typing import Any, Awaitable, Callable, Dict, Set, Tuple, Union

from devtools import debug

from pepperbot.exceptions import InitializationError
from pepperbot.store.meta import CLASS_CHECKERS, T_AvailableChecker, checkers_cache
from pepperbot.types import COMMAND_CONFIG, T
from pepperbot.utils.common import await_or_sync, fit_kwargs, get_class_name_from_method
from pepperbot.extensions.log import logger

AVAILABLE_CHECKERS = "__available_checkers__"
HAS_SET_AVAILABLE_CHECKERS = "__has_set_available_checkers__"


def available(*checkers: T_AvailableChecker):
    """动态判断handler、command是否可用

    checker可以是同步函数，也可以是异步函数，返回bool即可

    只要有一个不满足，即为不可用

    忽略抛出异常的checker(忽略 == True)

    并发执行所有checkers
    """

    def decorator(obj: T) -> T:
        # 现在因为是运行时从self上获取class，所以需要三层装饰器
        # 如果能在编译时获取class，那么只需要两层装饰器
        # 还是老样子，用class name作为key，这样就不用运行时获取了
        # 运行时获取self再判断，性能可能有损耗
        # @wraps(obj)
        # async def wrapper(*args, **kwargs):
        is_class = isclass(obj)

        if not is_class:
            if not isclass(obj.__class__):
                raise InitializationError(
                    "available只能用于class handler或者class command，暂不支持function handler"
                )

            # available可以应用到method上
            # 先定义function=>应用available装饰器=>绑定到class上，也就是说，available接收不到self
            # .__self__不存在
            # 同理，此时无法通过hasattr判断是否是command
            class_name = get_class_name_from_method(obj)  # type: ignore
            # target_class = args[0].__class__
            field: str = obj.__name__  # type: ignore
        else:
            class_name = obj.__name__
            field = CLASS_CHECKERS

        # if hasattr(target_class, HAS_SET_AVAILABLE_CHECKERS):
        #     if is_class:
        #         return obj
        #     else:
        #         return await await_or_sync(obj, *args, **kwargs)

        # debug(obj)
        # debug(class_name)

        checkers_cache[class_name, field].update(checkers)

        # saved_checkers: Dict[str, Set[T_AvailableChecker]] = getattr(
        #     obj, AVAILABLE_CHECKERS, {}
        # )
        # saved_checkers.setdefault(target_field, set()).update(checkers)
        # setattr(target_class_name, AVAILABLE_CHECKERS, saved_checkers)
        # setattr(target_class_name, HAS_SET_AVAILABLE_CHECKERS, True)

        # method有可能是异步，也可能同步，这里统一用await
        # return await await_or_sync(obj, *args, **kwargs)

        return obj

    # return wrapper

    return decorator


async def concurrently_run_checkers(
    checkers: Set[T_AvailableChecker],
    **kwargs,
) -> Tuple[bool, str]:
    """并发执行所有checkers"""

    awaitable_checkers_with_name = OrderedDict()

    for checker in checkers:
        awaitable_checkers_with_name[checker.__name__] = await_or_sync(
            checker, **fit_kwargs(checker, kwargs)
        )

    # debug(awaitable_checkers_with_name)

    #  gather returns a tuple of their results in the same order
    results = await asyncio.gather(
        *awaitable_checkers_with_name.values(), return_exceptions=True
    )

    for name, result in zip(awaitable_checkers_with_name.keys(), results):
        if isinstance(result, Exception):
            continue

        if not result:
            return False, name

    return True, ""


async def check_available(obj: object, kwargs: Dict, is_class=True) -> bool:
    """检查class是否可用

    会检查class的__available_checkers__属性，如果有值，则会并发执行所有checkers

    这里传入的是instance，所以从.__class__上获取

    cache的时候，是直接.__name__
    """

    if is_class:
        class_name = obj.__class__.__name__  # type: ignore
        field = CLASS_CHECKERS
    else:
        class_name = get_class_name_from_method(obj)  # type: ignore
        field = obj.__name__  # type: ignore

    # debug(checkers_cache)

    checkers = checkers_cache[class_name, field]
    if not checkers:
        return True

    available, checker_name = await concurrently_run_checkers(checkers, **kwargs)
    if not available:
        logger.info(f"available权限校验失败: {checker_name}")
    else:
        logger.info(f"available权限校验成功")

    return available


# def is_class_command(obj: object) -> bool:
#     """运行时，如果是command，COMMAND_CONFIG属性一定存在"""

#     is_class = isclass(obj)

#     if not is_class:
#         if not isclass(obj.__class__):
#             raise InitializationError(
#                 "available只能用于class handler或者class command，暂不支持function handler"
#             )

#         target_class = obj.__class__
#     else:
#         target_class = obj

#     return hasattr(target_class, COMMAND_CONFIG)
