import sys
from os import path

BASE_DIR = path.dirname(path.dirname(path.abspath(__file__)))
sys.path.append(BASE_DIR)


import inspect
from inspect import isawaitable, iscoroutine
from types import FunctionType
from typing import Any, Callable, Coroutine, Dict, List, Union, cast
from pydantic import BaseModel

# from pepperbot import *
# from pepperbot.utils.common import print_tree, DisplayTree

from devtools import debug


class DisplayTree(BaseModel):
    name: str
    node: List[Union["DisplayTree", str]]


DisplayTree.update_forward_refs()


def print_tree(tree: DisplayTree, indent=0, prefixes=[]):
    space = "    "
    branch = "│   "
    tee = "├───"
    lastBranch = "└───"

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


tree = DisplayTree(
    name="群123321",
    node=[
        dict(
            name="注册的指令",
            node=[
                "复读",
                dict(
                    name="注册的指令",
                    node=[
                        "复读",
                        "模拟",
                        dict(
                            name="注册的指令",
                            node=[
                                "复读",
                                dict(
                                    name="注册的指令",
                                    node=[
                                        "复读",
                                        "模拟",
                                    ],
                                ),
                                "模拟",
                            ],
                        ),
                    ],
                ),
                "模拟",
            ],
        ),
        "3",
        "4",
    ],
)

print_tree(tree)
