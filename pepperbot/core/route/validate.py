import ast
import inspect
import re
import textwrap
from typing import Any, Callable, Dict, List, Sequence, Set, Union, get_args, get_origin

from devtools import debug

from pepperbot.adapters.keaimao import KeaimaoAdapter
from pepperbot.adapters.onebot import OnebotV11Adapter
from pepperbot.adapters.telegram import TelegramAdapter
from pepperbot.adapters.universal import UniversalAdapter
from pepperbot.core.event.universal import ALL_PROTOCOL_EVENT_NAMES
from pepperbot.exceptions import InitializationError
from pepperbot.extensions.command.constant import (
    COMMAND_COMMON_KWARGS,
    COMMAND_DEFAULT_KWARGS,
)
from pepperbot.extensions.command.handle import LIFECYCLE_WITHOUT_PATTERNS
from pepperbot.store.command import PATTERN_ARG_TYPES, TemporaryPatternArg
from pepperbot.store.event import EventHandlerKwarg
from pepperbot.store.meta import command_relations_cache
from pepperbot.types import COMMAND_CONFIG
from pepperbot.utils.common import get_own_methods


def is_valid_class_handler(class_handler: object):
    for method in get_own_methods(class_handler):
        method_name = method.__name__

        is_class_handler_method_name_valid(method_name)
        is_class_handler_method_args_valid(class_handler, method, method_name)

    return True


def is_class_handler_method_name_valid(method_name: str):
    # if not (method_name in ALL_EVENTS):
    #     raise InitializationError(f"无效的事件名 {method_name}")

    # 允许非事件名的方法名
    return True


def gen_usable_kwargs_hint(keyword_arguments: Sequence[EventHandlerKwarg]):
    kwarg_name_type_mapping = {}
    for kwarg in keyword_arguments:
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


def is_class_handler_method_args_valid(
    class_handler: Any, method: Callable, method_name: str
):
    if method_name not in ALL_PROTOCOL_EVENT_NAMES:
        return

    if "onebot" in method_name:
        keyword_arguments = OnebotV11Adapter.kwargs_mapping[method_name]

    elif "keaimao" in method_name:
        keyword_arguments = KeaimaoAdapter.kwargs_mapping[method_name]

    elif "telegram" in method_name:
        keyword_arguments = TelegramAdapter.kwargs_mapping[method_name]

    else:
        keyword_arguments = UniversalAdapter.kwargs_mapping[method_name]

    kwarg_name_type_mapping, usable_kwargs_hint = gen_usable_kwargs_hint(
        keyword_arguments
    )
    usable_kwarg_names = kwarg_name_type_mapping.keys()

    source_file_name = inspect.getsourcefile(class_handler)
    class_handler_name = class_handler.__name__

    common_prefix = (
        f"\n{source_file_name}文件中的类响应器{class_handler_name}的" + f"{method_name}事件"
    )

    # all_args, var_args, var_kwargs = inspect.getargs(method.__code__)

    # if var_args or var_kwargs:
    #     raise InitializationError(
    #         common_prefix
    #         + "不需要提供*或者**参数，PepperBot会自动根据声明的参数以及类型注入"
    #         + usable_kwargs_hint
    #     )

    parameters = inspect.signature(method).parameters

    for arg_name in (list(parameters.keys()))[1:]:  # 第一个是self
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
    assert hasattr(
        class_command, COMMAND_CONFIG
    ), f"需要通过as_command装饰器修饰{class_command.__class__.__name__}"

    source_file_name = inspect.getsourcefile(class_command)
    class_command_name = class_command.__name__

    common_prefix = f"\n{source_file_name} 文件中的指令 {class_command_name} 的"

    methods = list(get_own_methods(class_command))
    method_names = [method.__name__ for method in methods]
    method_mapping = {method.__name__: method for method in methods}

    sub_command_method_names = list(command_relations_cache[class_command_name].keys())
    # debug(sub_command_method_names)

    if not "initial" in method_names:
        raise InitializationError("指令必须定义initial方法作为入口")

    for method in methods:
        method_name = method.__name__

        is_class_command_method_return_valid(
            method, method_name, method_names, sub_command_method_names, common_prefix
        )

    # 先通过上面的验证，此时的方法一定有返回值，并且只返回了一个值
    involved_method_names = get_all_returned_identifiers(methods)
    involved_method_names.add("initial")  # initial方法也需要验证

    # 只验证被返回的方法，其他的方法不需要验证
    for method_name in involved_method_names:
        method = method_mapping[method_name]
        is_class_command_method_args_valid(method, method_name, common_prefix)

    return True


def is_class_command_method_args_valid(
    method: Callable, method_name: str, common_prefix: str
):
    common_prefix += f"方法 {method_name} "

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
        keyword_arguments = COMMAND_DEFAULT_KWARGS.get(
            method_name, COMMAND_COMMON_KWARGS
        )
        kwarg_name_type_mapping, usable_kwargs_hint = gen_usable_kwargs_hint(
            keyword_arguments
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
            if p.default != p.empty and not isinstance(p.default, TemporaryPatternArg):
                raise InitializationError(common_prefix + f"不应为除CLI，或者Depends外的参数设置默认值")

            # type hint correct
            if not isinstance(p.default, TemporaryPatternArg):
                supposed_type = kwarg_name_type_mapping.get(arg_name)
                if not supposed_type:
                    raise InitializationError(
                        common_prefix + f"中不存在参数 {arg_name} ，请确认该参数是否为有效参数"
                    )

                is_kwarg_annotation_correct(
                    arg_name, p.annotation, supposed_type, common_prefix
                )

        # pattern args
        if isinstance(p.default, TemporaryPatternArg):
            # no pattern in lifecycle hooks
            if method_name in LIFECYCLE_WITHOUT_PATTERNS:
                raise InitializationError(common_prefix + f"这些生命周期不应支持pattern")

            # 考虑到Optional、List的情况
            element_type = get_args(p.annotation)

            # TODO 优化一下判断optional、list的逻辑，和pattern里的add_arguments一起
            if element_type:
                if container_type := get_origin(element_type[0]) is list:
                    element_type = get_args(element_type[0])[0]
                else:
                    element_type = element_type[0]

            else:  # 没有container
                element_type = p.annotation

            # debug(element_type)

            if element_type not in PATTERN_ARG_TYPES and element_type is not Any:
                raise InitializationError(
                    common_prefix
                    + f"仅支持str, bool, int, float和所有消息类型，或者Any"
                    + f"，而你提供了 {element_type}"
                )


def get_ids_from_single_return(elt):
    if isinstance(elt, (ast.Name,)):
        return [elt.id]

    # Return(
    #     value=Attribute(
    #         value=Name(id="self", ctx=Load()),
    #         attr="privilege",
    #         ctx=Load(),
    #     )
    # )
    if isinstance(elt, (ast.Attribute,)):
        if isinstance(elt.value, (ast.Name,)):
            if elt.value.id == "self":  # 必须是self
                return [elt.attr]

    return []


def get_ids(elt):
    """Extract identifiers if present. If not return None"""

    if isinstance(elt, (ast.Tuple,)):
        results = []
        for item in elt.elts:
            results.append(*get_ids_from_single_return(item))

    return get_ids_from_single_return(elt)


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
    function_source = inspect.getsource(f)
    # '    @sub_command(privilege)\n'
    # '    async def delete(self, sender: CommandSender):\n'
    # '        await sender.send_message(\n'
    # '            At(sender.user_id),\n'
    # '            Text("删除成功"),\n'
    # '        )\n'

    without_extra_indent = textwrap.dedent(function_source)
    # '@sub_command(privilege)\n'
    # 'async def delete(self, sender: CommandSender):\n'
    # '    await sender.send_message(\n'
    # '        At(sender.user_id),\n'
    # '        Text("删除成功"),\n'
    # '    )\n'

    # debug(function_source)
    # debug(without_extra_indent)

    # 如果有装饰器，装饰器也会一并获取到，要手动去掉，不然无法正常解析函数定义
    # 可能有多个装饰器
    while without_extra_indent.startswith("@"):
        without_decorator = without_extra_indent[without_extra_indent.index("\n") :]
        without_extra_indent = textwrap.dedent(without_decorator)

        # debug(without_decorator)
        # debug(without_first_indent)

    (tree,) = ast.parse(without_extra_indent).body

    # debug(tree)

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


def get_all_returned_identifiers(f_list: List[Callable]):
    identifiers: Set[str] = set()

    for f in f_list:
        return_statements = get_return_identifiers(f)

        for info in return_statements:
            ids = info["ids"]

            if ids:  # 不为None，且len(ids) == 1
                identifiers.update(ids)

    return identifiers


def is_class_command_method_return_valid(
    method: Callable,
    method_name: str,
    method_names: List[str],
    sub_command_method_names: List[str],
    common_prefix: str,
):
    """
    通过ast，保证方法返回值要么为None，要么是同一class的其它方法名

    同时不能是catch, timeout, exit，不应该由指令作者主动触发；initial和finish可以

    即使有了静态检测，运行时检测方法返回值也是需要的
    """

    # debug(get_return_identifiers(method))

    for info in get_return_identifiers(method):
        ids = info["ids"]

        wrong = False

        if not ids:  # 不返回
            continue

        if len(ids) > 1:  # 不能返回多个值
            wrong = True

        identifier = ids[0]
        # debug(identifier)

        your_error = ""

        if identifier not in method_names:  # 要么返回下一步的方法名，要么不返回
            wrong = True
            your_error = f"返回值 {identifier} 返回的不是指令的方法名，必须是当前class中的方法名"

        if identifier in LIFECYCLE_WITHOUT_PATTERNS:  # 不应该由指令作者主动触发
            wrong = True
            your_error = f"返回值 {identifier} 是生命周期，不应该由指令作者主动触发"

        if identifier in sub_command_method_names:  # sub command应该由框架调度，而不能直接返回
            wrong = True
            your_error = f"返回值 {identifier} 是sub command，应该由框架调度，而不能直接返回"

        if wrong:
            raise InitializationError(
                common_prefix
                + f"方法 {method_name} 的返回值未正确设置\n"
                + f"{your_error}\n\n"
                + "- 不能返回多个值\n"
                + "- 不能是catch, timeout, exit之类的生命周期，这些不应该由指令作者主动触发\n"
                + "- 可以返回initial生命周期\n"
                + "- 不能是sub command，sub command应该由框架调度，而不能直接返回\n\n"
                + "如果返回None，或者不写返回语句，会触发finish和cleanup生命周期，结束回话"
            )


def is_valid_route_validator(validator: Callable):
    """参数检查"""

    validator.__annotations__

    return True
