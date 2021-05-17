import inspect
from inspect import isawaitable, iscoroutine
from types import FunctionType
from typing import Any, Coroutine, Union, cast

from devtools import debug


class DictNoNone(dict):
    def __setitem__(self, key, value):
        if key in self or value is not None:
            dict.__setitem__(self, key, value)


def get_current_function_name():
    return inspect.currentframe().f_back.f_code.co_name


def get_own_methods(instance: object):
    """从class上获取所有非__开头的方法"""
    for methodName in dir(instance):

        methodOrProperty = getattr(instance, methodName)

        if callable(methodOrProperty):
            if not methodName.startswith("__"):
                yield cast(FunctionType, methodOrProperty)


async def await_or_normal(
    functionOrCoroutine: Union[Any, FunctionType], *args, **kwargs
):
    """
    针对bound method，iscoroutine和isawaitable对bound method无效

    判断__func__也不行
    """
    if callable(functionOrCoroutine):
        result = functionOrCoroutine(*args, **kwargs)
        # 针对bounded mothoud
        if iscoroutine(result):
            if result.__name__ == functionOrCoroutine.__name__:
                result = await result

        return result

    return None

    # debug(functionOrCoroutine)
    # debug(dir(functionOrCoroutine))
    # debug(functionOrCoroutine.__func__)
    # debug(functionOrCoroutine.__name__)
    # debug(functionOrCoroutine.__call__)
    # debug(iscoroutine(functionOrCoroutine.__func__))
    # debug(isawaitable(functionOrCoroutine.__func__))
    # if iscoroutine(functionOrCoroutine) or isawaitable(functionOrCoroutine):
    #     result = await functionOrCoroutine(*args, **kwargs)
    # else:
    #     result = functionOrCoroutine(*args, **kwargs)
    #     debug(result.__name__)

    # return result


# async def aaa():
#     await get_current_function_name()
