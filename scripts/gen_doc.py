import os
import sys
from os import path
from typing import Any, Iterable, Union, get_origin
from pepperbot.adapters.onebot.event.kwargs import ONEBOTV11_KWARGS_MAPPING
from pepperbot.adapters.keaimao.event.kwargs import KEAIMAO_KWARGS_MAPPING
from pepperbot.adapters.telegram.api import (
    TelegramApi,
    TelegramGroupApi,
    TelegramPrivateApi,
)
from pepperbot.adapters.telegram.event.kwargs import TELEGRAM_KWARGS_MAPPING

from pepperbot.core.bot.universal import UniversalGroupApi, UniversalPrivateApi
from pepperbot.core.event.kwargs import UNIVERSAL_KWARGS_MAPPING
from pepperbot.store.meta import T_HandlerKwargMapping

# BASE_DIR = path.dirname(path.dirname(path.abspath(__file__)))
# sys.path.append(BASE_DIR)

import inspect

import better_exceptions
from devtools import debug
from mdutils.mdutils import MdUtils
from pepperbot.adapters.keaimao.api import (
    KeaimaoApi,
    KeaimaoGroupApi,
    KeaimaoPrivateApi,
)
from pepperbot.adapters.onebot.api import (
    OnebotV11Api,
    OnebotV11GroupApi,
    OnebotV11PrivateApi,
)

from pepperbot.utils.common import get_own_methods


def gen_api_markdown(
    target_api_class: Any, output_file_path: str, extra_head: str = ""
):
    md_file = MdUtils(file_name=output_file_path)

    if extra_head:
        md_file.write(extra_head)

    md_file.new_header(level=1, title="")

    for method in get_own_methods(target_api_class):
        method_name = method.__name__
        md_file.new_header(level=2, title=method_name)

        docstring = method.__doc__
        if docstring:
            md_file.write(f"\n{method.__doc__}\n")

        parameter_table = ["参数名称", "类型", "默认值"]

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
                    row.append(parameter.default)
                else:
                    row.append("无")

            parameter_table.extend(row)

        # debug(parameter_table)

        # md_file.new_line()
        if len(parameter_table) > 3:
            md_file.new_table(
                columns=3,
                rows=int(len(parameter_table) / 3),
                text=parameter_table,
                text_align="center",
            )

    md_file.create_md_file()
    print(f"成功生成{output_file_path}文件")


# ! clean before recreate

api_prefix = "./docs/docs/API"
os.makedirs(f"{api_prefix}/Arbitrary API/", exist_ok=True)
gen_api_markdown(OnebotV11Api, f"{api_prefix}/Arbitrary API/Onebot")
gen_api_markdown(KeaimaoApi, f"{api_prefix}/Arbitrary API/可爱猫")
gen_api_markdown(TelegramApi, f"{api_prefix}/Arbitrary API/Telegram")

os.makedirs(f"{api_prefix}/区分模式 API/", exist_ok=True)
os.makedirs(f"{api_prefix}/区分模式 API/群/", exist_ok=True)
gen_api_markdown(UniversalGroupApi, f"{api_prefix}/区分模式 API/群/跨平台")
gen_api_markdown(OnebotV11GroupApi, f"{api_prefix}/区分模式 API/群/Onebot")
gen_api_markdown(KeaimaoGroupApi, f"{api_prefix}/区分模式 API/群/可爱猫")
gen_api_markdown(TelegramGroupApi, f"{api_prefix}/区分模式 API/群/Telegram")

os.makedirs(f"{api_prefix}/区分模式 API/私聊/", exist_ok=True)
gen_api_markdown(UniversalPrivateApi, f"{api_prefix}/区分模式 API/私聊/跨平台")
gen_api_markdown(OnebotV11PrivateApi, f"{api_prefix}/区分模式 API/私聊/Onebot")
gen_api_markdown(KeaimaoPrivateApi, f"{api_prefix}/区分模式 API/私聊/可爱猫")
gen_api_markdown(TelegramPrivateApi, f"{api_prefix}/区分模式 API/私聊/Telegram")


def gen_kwargs_markdown(
    mapping: T_HandlerKwargMapping, output_file_path: str, extra_head: str = ""
):
    md_file = MdUtils(file_name=output_file_path)

    if extra_head:
        md_file.write(extra_head)

    md_file.new_header(level=1, title="")

    for event_name, kwargs in mapping.items():
        md_file.new_header(level=2, title=event_name)

        parameter_table = ["参数名称", "类型"]

        for kwarg in kwargs:

            row = [kwarg.name]

            if isinstance(kwarg.type_, str):
                row.append(kwarg.type_)
            else:
                # if get_origin(parameter.annotation) is Union:
                #     # group_msg = group_message
                #     continue

                row.append(kwarg.type_)

            parameter_table.extend(row)

        # debug(parameter_table)

        if len(parameter_table) > 2:
            md_file.new_table(
                columns=2,
                rows=int(len(parameter_table) / 2),
                text=parameter_table,
                text_align="center",
            )

    md_file.create_md_file()
    print(f"成功生成{output_file_path}文件")


os.makedirs(f"{api_prefix}/事件参数/", exist_ok=True)
gen_kwargs_markdown(UNIVERSAL_KWARGS_MAPPING, f"{api_prefix}/事件参数/跨平台")
gen_kwargs_markdown(ONEBOTV11_KWARGS_MAPPING, f"{api_prefix}/事件参数/Onebot")
gen_kwargs_markdown(KEAIMAO_KWARGS_MAPPING, f"{api_prefix}/事件参数/可爱猫")
gen_kwargs_markdown(TELEGRAM_KWARGS_MAPPING, f"{api_prefix}/事件参数/Telegram")
