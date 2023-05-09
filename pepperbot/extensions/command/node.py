from typing import Dict, Iterable, List, Optional

from devtools import debug

from pepperbot.store.meta import SubCommandRelation


class CommandNode:
    def __init__(self, name: str):
        self.name = name
        self.parent: Optional["CommandNode"] = None
        self.children = []

    def __repr__(self):
        return f"<CommandNode {self.name}>"


def build_command_tree(
    relations_cache: Dict[str, SubCommandRelation], with_pattern_methods: Iterable[str]
):
    """构造出nest command的层级关系

    - a, b, c, d, e, f, g, h, i, j

    =>

    - a(initial)
        - b
            - d
            - e
        - c
            - f
            - g
    - h(非initial、非sub command，另一个根command)
        - i
        - j
    """

    node_dict: Dict[str, CommandNode] = {}

    root_command_method_names: List[str] = []

    sub_command_method_names = list(relations_cache.keys())
    for method_name in with_pattern_methods:
        if method_name not in sub_command_method_names:  # 是根command
            # node_dict["initial"] = CommandNode("initial")
            node_dict[method_name] = CommandNode(method_name)
            root_command_method_names.append(method_name)

    for method_name in relations_cache:
        node_dict[method_name] = CommandNode(method_name)

    for method_name, command_node in node_dict.items():
        if method_name in root_command_method_names:
            continue

        sub_command_relation = relations_cache[method_name]
        parent_method_name = sub_command_relation["parent_method_name"]

        if parent_method_name:
            parent_command_node = node_dict[parent_method_name]
            parent_command_node.children.append(command_node)
            command_node.parent = parent_command_node

        else:
            # 只有initial的sub command会走到这里
            # 如果是其他的根command，会在上面的if中continue
            node_dict["initial"].children.append(command_node)
            command_node.parent = node_dict["initial"]

    root_command_nodes: List[CommandNode] = []
    for root_command_name in root_command_method_names:
        root_command_node = node_dict[root_command_name]
        root_command_nodes.append(root_command_node)

    return root_command_nodes
