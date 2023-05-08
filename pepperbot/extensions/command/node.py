from typing import Dict, Optional

from pepperbot.store.meta import SubCommandRelation


class CommandNode:
    def __init__(self, name: str):
        self.name = name
        self.parent: Optional["CommandNode"] = None
        self.children = []


def build_command_tree(relations_cache: Dict[str, SubCommandRelation]):
    """构造出nest command的层级关系

    - a, b, c, d, e, f, g

    =>

    - a
        - b
            - d
            - e
        - c
            - f
            - g
    """

    node_dict: Dict[str, CommandNode] = {}

    node_dict["initial"] = CommandNode("initial")

    for method_name in relations_cache:
        node_dict[method_name] = CommandNode(method_name)

    for method_name, command_node in node_dict.items():
        if method_name == "initial":
            continue

        sub_command_relation = relations_cache[method_name]
        parent_method_name = sub_command_relation["parent_method_name"]

        if parent_method_name:
            parent_command_node = node_dict[parent_method_name]
            parent_command_node.children.append(command_node)
            command_node.parent = parent_command_node

        else:
            node_dict["initial"].children.append(command_node)
            command_node.parent = node_dict["initial"]

    return node_dict["initial"]
