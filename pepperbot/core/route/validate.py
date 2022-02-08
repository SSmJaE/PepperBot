import inspect
import re
from typing import Any, Callable, List, Union, get_args, get_origin

from devtools import debug
from pepperbot.adapters.keaimao.event.kwargs import KEAIMAO_KWARGS_MAPPING
from pepperbot.adapters.onebot.event.kwargs import ONEBOTV11_KWARGS_MAPPING
from pepperbot.core.event.kwargs import UNIVERSAL_KWARGS_MAPPING
from pepperbot.core.event.universal import (
    ALL_COMMON_EVENTS,
    ALL_GROUP_EVENTS,
    ALL_META_EVENTS,
    ALL_PRIVATE_EVENTS,
)
from pepperbot.exceptions import InitializationError
from pepperbot.store.meta import EventHandlerKwarg
from pepperbot.utils.common import get_own_methods


def is_valid_class_handler(class_handler: object):
    for method in get_own_methods(class_handler):
        method_name = method.__name__

        is_handler_method_name_valid(method_name)
        is_handler_method_args_valid(class_handler, method, method_name)

    return True


def is_valid_class_command(class_command: object):

    return True


def is_valid_route_validator(validator: Callable):
    """参数检查"""

    validator.__annotations__

    return True


def is_handler_method_name_valid(method_name: str):
    if not (
        method_name in ALL_META_EVENTS
        or method_name in ALL_COMMON_EVENTS
        or method_name in ALL_GROUP_EVENTS
        or method_name in ALL_PRIVATE_EVENTS
    ):
        raise InitializationError(f"无效的事件名 {method_name}")


def is_handler_method_args_valid(
    class_handler: Any, method: Callable, method_name: str
):

    if "onebot" in method_name:
        mapping = ONEBOTV11_KWARGS_MAPPING
        event_name = method_name.replace("onebot_", "")
    elif "keaimao" in method_name:
        mapping = KEAIMAO_KWARGS_MAPPING
        event_name = method_name.replace("keaimao_", "")
    else:
        mapping = UNIVERSAL_KWARGS_MAPPING
        event_name = method_name

    kwarg_list: List[EventHandlerKwarg] = mapping.get(event_name, [])

    kwarg_name_type_mapping = {}
    for kwarg in kwarg_list:
        kwarg_name_type_mapping[kwarg.name] = kwarg.type_

    usable_kwarg_names = kwarg_name_type_mapping.keys()

    all_args, var_args, var_kwargs = inspect.getargs(method.__code__)

    usable_kwargs_hint = "\n可用的参数及类型有\n"
    kwargs_count = len(kwarg_name_type_mapping)

    for index, (kwargName, kwargType) in enumerate(
        kwarg_name_type_mapping.items(), start=1
    ):
        usable_kwargs_hint += f"{kwargName} : {kwargType}"

        if index != kwargs_count:
            usable_kwargs_hint += ",\n"

    source_file_name = inspect.getsourcefile(class_handler)
    class_handler_name = class_handler.__name__

    common_prefix = (
        f"\n{source_file_name}文件中的类响应器{class_handler_name}的" + f"{method_name}事件"
    )

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

        wrong_type_flag = True

        if get_origin(supposed_arg_type) is Union:
            for type_ in get_args(supposed_arg_type):
                if type_ == arg_type:
                    wrong_type_flag = False

        else:
            if type(supposed_arg_type) == str:  # 避免循环导入，有时会使用字符串形式的类型
                # <class 'pepperbot.core.message.chain.MessageChain'>
                pattern = re.search(r"<class '(.*)'>", str(arg_type))
                if not pattern:
                    raise InitializationError(f"无法确认参数{arg_name}的类型")

                str_arg_type = pattern.groups()[0].split(".")[-1]
                if supposed_arg_type == str_arg_type:
                    wrong_type_flag = False

            else:
                if supposed_arg_type == arg_type:
                    wrong_type_flag = False

        if wrong_type_flag:
            raise InitializationError(
                common_prefix + f"的参数{arg_name}的类型应该为{supposed_arg_type}，而不是{arg_type}"
            )
