import inspect
from inspect import isawaitable, iscoroutine
from types import FunctionType
from typing import Any, Callable, Coroutine, Dict, List, Union, cast
from pydantic import BaseModel

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


async def deepawait_or_normal(
    functionOrCoroutineOrValue: Union[Any, Coroutine, FunctionType], *args, **kwargs
):
    """
    pepperbot.parse.kwargs.get_member_info

    双重await，lambda
    """
    if callable(functionOrCoroutineOrValue):
        result = functionOrCoroutineOrValue(*args, **kwargs)

        while iscoroutine(result):
            result = await result

        return result

    return functionOrCoroutineOrValue


def fit_kwargs(method: Callable, kwargs: Dict[str, Any]):
    validKwargNames = method.__annotations__.keys()

    finalKwargs = {}

    for argName in kwargs.keys():
        if argName in validKwargNames:
            finalKwargs[argName] = kwargs[argName]

    return finalKwargs


class DisplayTree(BaseModel):
    name: str
    node: List[Union["DisplayTree", str]]


DisplayTree.update_forward_refs()


def print_tree(tree: DisplayTree, indent=0, prefixes=[]):
    space = "    "
    branch = "│   "
    tee = "├── "
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
