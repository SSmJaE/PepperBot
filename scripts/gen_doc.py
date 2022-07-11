import inspect
import os
import re
import shutil
from typing import Any, Iterable, List, Union, get_origin

from devtools import debug
from pepperbot.adapters.keaimao.api import (
    KeaimaoApi,
    KeaimaoGroupApi,
    KeaimaoPrivateApi,
)
from pepperbot.adapters.keaimao.event.kwargs import KEAIMAO_KWARGS_MAPPING
from pepperbot.adapters.onebot.api import (
    OnebotV11Api,
    OnebotV11GroupApi,
    OnebotV11PrivateApi,
)
from pepperbot.adapters.onebot.event import OnebotV11EventComments
from pepperbot.adapters.onebot.event.kwargs import ONEBOTV11_KWARGS_MAPPING
from pepperbot.adapters.telegram.api import (
    TelegramApi,
    TelegramGroupApi,
    TelegramPrivateApi,
)
from pepperbot.adapters.telegram.event.kwargs import TELEGRAM_KWARGS_MAPPING
from pepperbot.core.bot.universal import UniversalGroupApi, UniversalPrivateApi
from pepperbot.core.event.kwargs import UNIVERSAL_KWARGS_MAPPING
from pepperbot.store.meta import T_HandlerKwargMapping
from pepperbot.utils.common import get_own_methods


def gen_table(rows: List[List[str]]):
    string = ""

    for index, row in enumerate(rows):
        if index == 0:
            string += f"|{'|'.join(row)}|\n"
            string += f"|{'|'.join(':---:' for _ in row)}|\n"

        else:
            string += f"|{'|'.join(row)}|\n"

    return string


def create_md_file(output_file_path: str, content: str):
    if not output_file_path.endswith(".md"):
        output_file_path += ".md"

    with open(output_file_path, "w", encoding="utf8") as f:
        f.write(content)


def gen_api_markdown(
    target_api_class: Any, output_file_path: str, extra_head: str = ""
):
    md_file = ""

    if extra_head:
        md_file += extra_head

    for method in get_own_methods(target_api_class):
        method_name = method.__name__
        md_file += f"## {method_name}\n\n"

        docstring = method.__doc__
        if docstring:
            md_file += f"\n{method.__doc__}\n"

        parameter_table = [["参数名称", "类型", "默认值"]]

        for parameter in inspect.signature(method).parameters.values():
            if parameter.name == "self":
                continue

            row = [parameter.name]

            if isinstance(parameter.annotation, str):
                row.append(parameter.annotation)
            else:
                # ! todo auto determine if is generic type like Iterable, List
                if get_origin(parameter.annotation) in [Union, Iterable]:
                    # group_msg = group_message
                    continue

                if "Iterable" in repr(parameter):
                    row.append(parameter.annotation)
                    continue

                # debug(repr(parameter))
                # debug(parameter.annotation)
                row.append(parameter.annotation.__name__)

            if parameter.default == inspect._empty:
                row.append("无")
            else:
                if parameter.default:
                    row.append(str(parameter.default))
                else:
                    row.append("无")

            parameter_table.append(row)

        if len(parameter_table) > 1:
            md_file += gen_table(parameter_table)

    create_md_file(output_file_path, md_file)
    print(f"成功生成{output_file_path}文件")


def cleanup(output_dir: str):
    shutil.rmtree(output_dir)
    os.makedirs(output_dir)


api_prefix = "./docs/docs/API"

cleanup(f"{api_prefix}/Arbitrary API")
gen_api_markdown(OnebotV11Api, f"{api_prefix}/Arbitrary API/Onebot")
gen_api_markdown(KeaimaoApi, f"{api_prefix}/Arbitrary API/可爱猫")
gen_api_markdown(TelegramApi, f"{api_prefix}/Arbitrary API/Telegram")

os.makedirs(f"{api_prefix}/区分模式 API/", exist_ok=True)

cleanup(f"{api_prefix}/区分模式 API/群/")
gen_api_markdown(UniversalGroupApi, f"{api_prefix}/区分模式 API/群/跨平台")
gen_api_markdown(OnebotV11GroupApi, f"{api_prefix}/区分模式 API/群/Onebot")
gen_api_markdown(KeaimaoGroupApi, f"{api_prefix}/区分模式 API/群/可爱猫")
gen_api_markdown(TelegramGroupApi, f"{api_prefix}/区分模式 API/群/Telegram")

cleanup(f"{api_prefix}/区分模式 API/私聊/")
gen_api_markdown(UniversalPrivateApi, f"{api_prefix}/区分模式 API/私聊/跨平台")
gen_api_markdown(OnebotV11PrivateApi, f"{api_prefix}/区分模式 API/私聊/Onebot")
gen_api_markdown(KeaimaoPrivateApi, f"{api_prefix}/区分模式 API/私聊/可爱猫")
gen_api_markdown(TelegramPrivateApi, f"{api_prefix}/区分模式 API/私聊/Telegram")


def gen_kwargs_markdown(
    mapping: T_HandlerKwargMapping,
    comments: Union[object, None],
    output_file_path: str,
    extra_head: str = "",
):
    # md_file = MdUtils(file_name=output_file_path)
    md_file = ""

    if extra_head:
        md_file += extra_head

    for event_name, kwargs in mapping.items():
        md_file += f"## {event_name}\n\n"

        if comments:
            comment = getattr(comments, event_name, None)
            if comment:
                md_file += f"> {comment}\n\n"

        parameter_table = [["参数名称", "类型"]]

        import_block = ""
        parameter_block = ""
        for kwarg in kwargs:

            row = [kwarg.name]

            type_string = str(kwarg.type_)

            if "<class '" in type_string:
                module_path = re.search(r"<class '(.*)'>", type_string).groups()[0]

            elif type_string == "MessageChain":
                module_path = "pepperbot.core.message.chain.MessageChain"

            else:
                module_path = type_string

            debug(module_path)

            modules = module_path.split(".")
            if len(modules) == 1:
                hint = modules[0]

            else:
                hint = f"from {'.'.join(modules[:len(modules)-1])} import {modules[-1]}"

            debug(hint)
            row.append(f"`{hint}`")
            import_block += f"{hint}\n"
            parameter_block += f"        {kwarg.name}: {modules[-1]},\n"

            parameter_table.append(row)

        # debug(parameter_table)

        if len(parameter_table) > 1:
            md_file += gen_table(parameter_table)

        snippet = f"""\

```py
{import_block}

class MyHandler:
    async def {event_name}(
        {parameter_block[8:]}    ):
        pass
```

"""

        md_file += snippet

    create_md_file(output_file_path, md_file)

    print(f"成功生成{output_file_path}文件")


cleanup(f"{api_prefix}/事件参数/")
gen_kwargs_markdown(
    UNIVERSAL_KWARGS_MAPPING,
    None,
    f"{api_prefix}/事件参数/跨平台",
)
gen_kwargs_markdown(
    ONEBOTV11_KWARGS_MAPPING,
    OnebotV11EventComments,
    f"{api_prefix}/事件参数/Onebot",
)
gen_kwargs_markdown(
    KEAIMAO_KWARGS_MAPPING,
    None,
    f"{api_prefix}/事件参数/可爱猫",
)
gen_kwargs_markdown(
    TELEGRAM_KWARGS_MAPPING,
    None,
    f"{api_prefix}/事件参数/Telegram",
)
