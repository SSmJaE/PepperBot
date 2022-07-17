from ast import Call
import ast
import inspect
import re
from typing import Any, Callable, Dict, List, Sequence, Union, get_args, get_origin

from devtools import debug
from pepperbot.adapters.keaimao.event.kwargs import KEAIMAO_KWARGS_MAPPING
from pepperbot.adapters.onebot.event.kwargs import ONEBOTV11_KWARGS_MAPPING
from pepperbot.adapters.telegram.event.kwargs import TELEGRAM_KWARGS_MAPPING
from pepperbot.core.event.kwargs import UNIVERSAL_KWARGS_MAPPING
from pepperbot.core.event.universal import (
    ALL_COMMON_EVENTS,
    ALL_GROUP_EVENTS,
    ALL_META_EVENTS,
    ALL_PRIVATE_EVENTS,
)
from pepperbot.exceptions import InitializationError
from pepperbot.extensions.command.handle import (
    COMMAND_DEFAULT_KWARGS,
    LIFECYCLE_NO_PROGRAMMIC,
    LIFECYCLE_WITHOUT_PATTERNS,
    common_kwargs,
)
from pepperbot.store.command import runtime_pattern_arg_types
from pepperbot.store.meta import EventHandlerKwarg
from pepperbot.utils.common import get_own_methods


def is_valid_class_handler(class_handler: object):
    for method in get_own_methods(class_handler):
        method_name = method.__name__

        is_handler_method_name_valid(method_name)
        is_handler_method_args_valid(class_handler, method, method_name)

    return True


def is_handler_method_name_valid(method_name: str):
    if not (
        method_name in ALL_META_EVENTS
        or method_name in ALL_COMMON_EVENTS
        or method_name in ALL_GROUP_EVENTS
        or method_name in ALL_PRIVATE_EVENTS
    ):
        raise InitializationError(f"无效的事件名 {method_name}")


def gen_usable_kwargs_hint(method_name_kwargs_mapping: Dict, method_name: str):

    kwarg_list: List[EventHandlerKwarg] = method_name_kwargs_mapping.get(
        method_name, common_kwargs
    )

    kwarg_name_type_mapping = {}
    for kwarg in kwarg_list:
        kwarg_name_type_mapping[kwarg.name] = kwarg.type_

    usable_kwargs_hint = "\n可用的参数及类型有\n"
    kwargs_count = len(kwarg_name_type_mapping)

    for index, (kwargName, kwargType) in enumerate(
        kwarg_name_type_mapping.items(), start=1
    ):
        usable_kwargs_hint += f"{kwargName} : {kwargType}"

        if index != kwargs_count:
            usable_kwargs_hint += ",\n"

    return kwarg_name_type_mapping, usable_kwargs_hint


def is_kwarg_annotation_correct(
    parameter_name: str,
    parameter_type: Any,
    supposed_type: Any,
    common_prefix: str = "",
):
    wrong_type_flag = True

    if get_origin(supposed_type) is Union:
        for type_ in get_args(supposed_type):
            if type_ == parameter_type:
                wrong_type_flag = False

    else:
        if type(supposed_type) == str:  # 避免循环导入，有时会使用字符串形式的类型
            # <class 'pepperbot.core.message.chain.MessageChain'>
            pattern = re.search(r"<class '(.*)'>", str(parameter_type))
            if not pattern:
                raise InitializationError(common_prefix + f"无法确认参数{parameter_name}的类型")

            str_parameter_type = pattern.groups()[0].split(".")[-1]
            if supposed_type == str_parameter_type:
                wrong_type_flag = False

        else:
            if supposed_type == parameter_type:
                wrong_type_flag = False

    if wrong_type_flag:
        raise InitializationError(
            common_prefix
            + f"的参数{parameter_name}的类型应该为{supposed_type}，而不是{parameter_type}"
        )


def is_handler_method_args_valid(
    class_handler: Any, method: Callable, method_name: str
):

    if "onebot" in method_name:
        mapping = ONEBOTV11_KWARGS_MAPPING
        event_name = method_name.replace("onebot_", "")

    elif "keaimao" in method_name:
        mapping = KEAIMAO_KWARGS_MAPPING
        event_name = method_name.replace("keaimao_", "")

    elif "telegram" in method_name:
        mapping = TELEGRAM_KWARGS_MAPPING
        event_name = method_name.replace("telegram_", "")

    else:
        mapping = UNIVERSAL_KWARGS_MAPPING
        event_name = method_name

    kwarg_name_type_mapping, usable_kwargs_hint = gen_usable_kwargs_hint(
        mapping, event_name
    )
    usable_kwarg_names = kwarg_name_type_mapping.keys()

    source_file_name = inspect.getsourcefile(class_handler)
    class_handler_name = class_handler.__name__

    common_prefix = (
        f"\n{source_file_name}文件中的类响应器{class_handler_name}的" + f"{method_name}事件"
    )

    all_args, var_args, var_kwargs = inspect.getargs(method.__code__)

    if var_args or var_kwargs:
        raise InitializationError(
            common_prefix
            + "不需要提供*或者**参数，PepperBot会自动根据声明的参数以及类型注入"
            + usable_kwargs_hint
        )

    for arg_name in all_args[1:]:  # 第一个是self
        if arg_name not in usable_kwarg_names:
            raise InitializationError(
                common_prefix + f"上不存在参数{arg_name}" + usable_kwargs_hint
            )

        if arg_name not in method.__annotations__.keys():
            raise InitializationError(
                common_prefix
                + f"的参数{arg_name}未提供类型注解，其类型为{kwarg_name_type_mapping[arg_name]}"
                + usable_kwargs_hint
            )

    # 经过上两步验证，此时的参数，一定是有效的，而且有类型注解
    for arg_name, arg_type in method.__annotations__.items():

        supposed_arg_type = kwarg_name_type_mapping[arg_name]

        is_kwarg_annotation_correct(
            arg_name, arg_type, supposed_arg_type, common_prefix
        )


def is_valid_class_command(class_command: Any):
    source_file_name = inspect.getsourcefile(class_command)
    class_command_name = class_command.__name__

    common_prefix = f"\n{source_file_name} 文件中的指令 {class_command_name} 的"

    methods = list(get_own_methods(class_command))
    method_names = [method.__name__ for method in methods]

    if not "initial" in method_names:
        raise InitializationError("指令必须定义initial方法作为入口")

    for method in methods:
        method_name = method.__name__

        is_command_method_args_valid(method, method_name, common_prefix)
        is_command_method_return_valid(method, method_name, method_names, common_prefix)

    return True


def is_command_method_args_valid(
    method: Callable, method_name: str, common_prefix: str
):

    common_prefix += f"{method_name}方法"

    signature = inspect.signature(method)

    for arg_name, p in signature.parameters.items():

        # self
        if arg_name == "self":
            continue

        # no *, **
        if p.kind == p.VAR_POSITIONAL or p.kind == p.VAR_KEYWORD:
            raise InitializationError(
                common_prefix + "不需要提供*或者**参数，PepperBot会自动根据声明的参数以及类型注入"
            )

        ## has type hint
        kwarg_name_type_mapping, usable_kwargs_hint = gen_usable_kwargs_hint(
            COMMAND_DEFAULT_KWARGS, method_name
        )

        if p.annotation == p.empty:
            raise InitializationError(
                common_prefix
                + f"指令的方法 {method_name} 的参数 {arg_name} 未提供类型注解"
                + usable_kwargs_hint
                if arg_name in kwarg_name_type_mapping.keys()
                else ""
            )

        else:
            # kwargs == no default value
            if p.default != p.empty and p.default != "PatternArg":
                raise InitializationError(
                    common_prefix + f"不应为 {method_name} 除pattern外的参数设置默认值"
                )

            # type hint correct
            if p.default != "PatternArg":
                supposed_type = kwarg_name_type_mapping.get(arg_name)
                if not supposed_type:
                    raise InitializationError(
                        common_prefix + f"{arg_name} 无对应的类型，请确认该参数是否为有效参数"
                    )

                is_kwarg_annotation_correct(
                    arg_name, p.annotation, supposed_type, common_prefix
                )

        # pattern args
        if p.default == "PatternArg":
            # no pattern in lifecycle hooks
            if method_name in LIFECYCLE_WITHOUT_PATTERNS:
                raise InitializationError(common_prefix + f"这些生命周期不应支持pattern")

            if p.annotation not in runtime_pattern_arg_types:
                raise InitializationError(
                    common_prefix + f"仅支持str, bool, int, float和所有消息类型"
                )


def get_ids(elt):
    """Extract identifiers if present. If not return None"""

    if isinstance(elt, (ast.Tuple,)):
        # For tuple get id of each item if item is a Name
        return [x.id for x in elt.elts if isinstance(x, (ast.Name,))]

    if isinstance(elt, (ast.Name,)):
        return [elt.id]


def get_return_identifiers(f: Callable):
    """
    [{'ids': ['x'],
     'lineno': 3,
     'statement': <_ast.Return object at 0x00000233AC624610>},
    {'ids': None,
     'lineno': 5,
     'statement': <_ast.Return object at 0x00000233AC6240D0>},
    {'ids': ['x', 'y'],
     'lineno': 7,
     'statement': <_ast.Return object at 0x00000233AC624100>}]
    """
    (tree,) = ast.parse(inspect.getsource(f).lstrip()).body

    return_statements: List = []

    for node in ast.walk(tree):
        if isinstance(node, (ast.Return,)):
            return_statements.append(
                dict(
                    statement=node,
                    lineno=node.lineno,
                    ids=get_ids(node.value),
                )
            )

    return return_statements


def is_command_method_return_valid(
    method: Callable, method_name: str, method_names: List[str], common_prefix: str
):
    """
    通过ast，保证方法返回值要么为None，要么是同一class的其它方法名

    同时不能是catch, timeout, exit，不应该由指令作者主动触发；initial和finish可以

    即使有了静态检测，运行时检测方法返回值也是需要的
    """
    for info in get_return_identifiers(method):
        ids = info["ids"]

        wrong = False

        if not ids:  # 不返回
            continue

        if len(ids) > 1:  # 不能返回多个值
            wrong = True

        identifier = ids[0]
        if identifier not in method_names:  # 要么返回下一步的方法名，要么不返回
            wrong = True

        if identifier in LIFECYCLE_NO_PROGRAMMIC:
            wrong = True

        if wrong:
            raise InitializationError(
                common_prefix + f"方法 {method_name} 的返回值可以为除catch, timeout, exit以外的生命周期，"
                "即initial和finish，或者直接返回None(不返回)以结束会话"
            )


def is_valid_route_validator(validator: Callable):
    """参数检查"""

    validator.__annotations__

    return True
