import asyncio
import inspect
from inspect import iscoroutine
from types import FunctionType
from typing import Any, Callable, Coroutine, Dict, List, Union, cast

from devtools import debug
from pydantic import BaseModel


class DictNoNone(dict):
    def __setitem__(self, key, value):
        if key in self or value is not None:
            dict.__setitem__(self, key, value)


def get_current_function_name():
    return inspect.currentframe().f_back.f_code.co_name  # type:ignore


def get_own_methods(instance: object):
    """从class上获取所有非__开头的方法"""
    for methodName in dir(instance):
        methodOrProperty = getattr(instance, methodName)

        if callable(methodOrProperty):
            if not methodName.startswith("__"):
                yield cast(FunctionType, methodOrProperty)


def get_own_attributes(instance: object):
    """从class上获取所有非__开头的属性"""

    for property in dir(instance):
        if not property.startswith("__"):
            yield property


def get_class_name_from_method(method: Callable) -> str:
    """从method上获取class name"""

    # debug(method.__qualname__)

    return method.__qualname__.split(".")[0]


async def await_or_sync(obj: Union[Any, FunctionType], *args, **kwargs) -> Any:
    """
    针对bound method，iscoroutine和isawaitable对bound method无效

    判断__func__也不行
    """

    # while isinstance(obj, functools.partial):
    #     obj = obj.func

    if (
        asyncio.iscoroutinefunction(obj)
        or (callable(obj) and asyncio.iscoroutinefunction(obj.__call__))
        # or iscoroutine(obj)
        # or isawaitable(obj)
    ):
        # debug("coroutine")
        result = await obj(*args, **kwargs)  # type: ignore
        return result
    else:
        if callable(obj):
            # debug("sync")
            result = await asyncio.to_thread(obj, *args, **kwargs)
            # loop = asyncio.get_event_loop()
            # with_kwargs = functools.partial(functionOrCoroutine, *args, **kwargs)

            # result = await loop.run_in_executor(None, with_kwargs)
            return result
        else:
            return None

    # if callable(functionOrCoroutine):
    #     result = functionOrCoroutine(*args, **kwargs)
    #     # 针对bounded mothoud
    #     if iscoroutine(result):
    #         if result.__name__ == functionOrCoroutine.__name__:
    #             result = await result

    #     return result

    # return None

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


async def deepawait_or_sync(
    value_or_function_or_coroutine: Union[
        Any,
        FunctionType,
        Coroutine,
    ],
    *args,
    **kwargs,
) -> Any:
    """双重await，lambda"""
    if callable(value_or_function_or_coroutine):
        # 第一次调用一个协程，会返回一个awaitable
        # awaitable不可调用
        result = value_or_function_or_coroutine(*args, **kwargs)

        while iscoroutine(result) or callable(result):
            if callable(result):
                result = result()
            else:
                result = await result

        return result

    return value_or_function_or_coroutine


def fit_kwargs(method: Callable, kwargs: Dict[str, Any]):
    """
    刨除没有在函数中定义的，但是提供了的额外参数

    可以是lambda函数

    定义时是位置参数或者关键字参数都可以，因为位置参数也可以通过关键词参数的形式赋值
    """
    # validKwargNames = method.__annotations__.keys()
    # provided_arg_names = inspect.getargs(method.__code__)[0]
    provided_arg_names = inspect.signature(method).parameters

    fitted_args = {}

    for arg_name in kwargs.keys():
        if arg_name in provided_arg_names:
            fitted_args[arg_name] = kwargs[arg_name]

    return fitted_args


class DisplayTree(BaseModel):
    name: str
    node: List[Union["DisplayTree", str]]


DisplayTree.update_forward_refs()


def print_tree(tree: DisplayTree, indent=0, prefixes=[]):
    space = "    "
    tee = "├── "
    branch = "│   "
    lastBranch = "└── "

    if indent == 0:
        print(tree.name)

    treeLength = len(tree.node)
    for index, node in enumerate(tree.node):
        newPrefixes = [*prefixes]

        if index == treeLength - 1:
            if isinstance(node, DisplayTree):
                print("".join([*prefixes, lastBranch]), node.name)

                newPrefixes.append(space)
            else:
                newPrefixes.append(lastBranch)

        else:
            if isinstance(node, DisplayTree):
                print("".join([*prefixes, tee]), node.name)

                newPrefixes.append(branch)
            else:
                newPrefixes.append(tee)

        if isinstance(node, DisplayTree):
            print_tree(node, indent + 1, newPrefixes)
        else:
            print("".join(newPrefixes), node)
