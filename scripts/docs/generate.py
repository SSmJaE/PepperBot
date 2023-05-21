import inspect
import re
from textwrap import dedent
from typing import Any, Iterable, List, Union, get_args, get_origin

from devtools import debug


import os
import sys

# 可以直接from tests.conftest import
base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
print(base_dir)
sys.path.append(base_dir)


from pepperbot.adapters.keaimao.api import (
    KeaimaoAPI,
    KeaimaoGroupAPI,
    KeaimaoPrivateAPI,
)
from pepperbot.adapters.keaimao.event import KeaimaoEvent
from pepperbot.adapters.onebot.api import (
    OnebotV11API,
    OnebotV11GroupAPI,
    OnebotV11PrivateAPI,
)
from pepperbot.adapters.onebot.event import OnebotV11Event
from pepperbot.adapters.telegram.api import (
    TelegramAPI,
    TelegramGroupAPI,
    TelegramPrivateAPI,
)
from pepperbot.adapters.telegram.event import TelegramEvent
from pepperbot.adapters.universal.api import UniversalGroupAPI, UniversalPrivateAPI
from pepperbot.adapters.universal.event import UniversalEvent
from pepperbot.store.event import ProtocolEvent
from pepperbot.utils.common import get_own_attributes, get_own_methods

from scripts.docs.markdown import Markdown
from scripts.docs.utils import cleanup


def generate_api_doc(target_api_class: Any, output_file_path: str):
    md = Markdown()

    for method in get_own_methods(target_api_class):
        method_name = method.__name__
        md.title(method_name, level=2)

        docstring = method.__doc__
        if docstring:
            md.text(dedent(docstring))

        parameter_table = [["参数名称", "类型", "默认值"]]

        for parameter in inspect.signature(method).parameters.values():
            if parameter.name == "self":
                continue

            row = [parameter.name]

            # # TODO auto determine if is generic type like Iterable, List
            # if get_origin(parameter.annotation) in [Union, Iterable]:
            #     # group_msg = group_message
            #     continue

            # if "Iterable" in repr(parameter):
            #     row.append(parameter.annotation)
            #     continue

            # debug(repr(parameter))
            # debug(parameter.annotation)
            # print(str(parameter.annotation))
            # row.append(parameter.annotation.__name__)
            annotation_string = str(parameter.annotation)
            if "segment.At" in annotation_string:
                annotation_string = "T_SegmentInstance(任意消息片段)"
            row.append(annotation_string)

            if parameter.default == inspect._empty:
                row.append("无")
            else:
                if parameter.default:
                    row.append(str(parameter.default))
                else:
                    row.append("无")

            parameter_table.append(row)

        if len(parameter_table) > 1:
            md.table(parameter_table)

    md.to_file(output_file_path)
    print(f"成功生成{output_file_path}文件")


root_api_prefix = "./docs/docs/API"


universal_api_prefix = f"{root_api_prefix}/Universal API"
cleanup(universal_api_prefix)
# generate_api_doc(UniversalAPI, f"{universal_api_prefix}/common")
generate_api_doc(UniversalGroupAPI, f"{universal_api_prefix}/group")
generate_api_doc(UniversalPrivateAPI, f"{universal_api_prefix}/private")
# generate_api_doc(UniversalChannelAPI, f"{universal_api_prefix}/频道")

keaimao_api_prefix = f"{root_api_prefix}/Keaimao API"
cleanup(keaimao_api_prefix)
generate_api_doc(KeaimaoAPI, f"{keaimao_api_prefix}/common")
generate_api_doc(KeaimaoGroupAPI, f"{keaimao_api_prefix}/group")
generate_api_doc(KeaimaoPrivateAPI, f"{keaimao_api_prefix}/private")
# generate_api_doc(KeaimaoChannelAPI, f"{keaimao_api_prefix}/频道")


onebot_api_prefix = f"{root_api_prefix}/Onebot API"
cleanup(onebot_api_prefix)
generate_api_doc(OnebotV11API, f"{onebot_api_prefix}/common")
generate_api_doc(OnebotV11GroupAPI, f"{onebot_api_prefix}/group")
generate_api_doc(OnebotV11PrivateAPI, f"{onebot_api_prefix}/private")
# generate_api_doc(OnebotV11ChannelAPI, f"{onebot_api_prefix}/频道")


telegram_api_prefix = f"{root_api_prefix}/Telegram API"
cleanup(telegram_api_prefix)
generate_api_doc(TelegramAPI, f"{telegram_api_prefix}/common")
generate_api_doc(TelegramGroupAPI, f"{telegram_api_prefix}/group")
generate_api_doc(TelegramPrivateAPI, f"{telegram_api_prefix}/private")
# generate_api_doc(TelegramChannelAPI, f"{telegram_api_prefix}/频道")


def get_module_path(type_: Any) -> str:
    type_string = str(type_)

    if "<class '" in type_string:
        module_path = re.search(r"<class '(.*)'>", type_string).groups()[0]  # type: ignore

    elif type_string == "MessageChain":
        module_path = "pepperbot.core.message.chain.MessageChain"

    # elif "segment.At" in type_string:
    #     module_path = "pepperbot.core.message.segment"

    else:
        module_path = type_string

    return module_path


EXAMPLE_EVENT_TEMPLATE = """\
{import_block}

class MyHandler:
    async def {event_name}(
        self,
{parameters}
    ):
        pass
"""


def construct_import_path(type_: Any):
    module_path = get_module_path(type_)

    modules = module_path.split(".")

    # 不可能是<class 'xxx'>，在get_module_path中已经处理过了
    absolute_symbol = modules[-1]

    if len(modules) == 1:  # builtin type
        hint = None

    else:
        source_path = ".".join(modules[: len(modules) - 1])
        hint = f"from {source_path} import {absolute_symbol}"

    return hint, absolute_symbol


def generate_event_doc(
    event_class: Any,
    output_file_path: str,
):
    md = Markdown()

    for event_name in get_own_attributes(event_class):
        protocol_event: ProtocolEvent = getattr(event_class, event_name)

        md.title(event_name, level=2)

        if protocol_event.description:
            md.text("> " + protocol_event.description)

        parameter_table = [["参数名称", "类型"]]

        import_block = ""
        parameter_block = ""

        arguments_count = len(protocol_event.keyword_arguments)

        for index, kwarg in enumerate(protocol_event.keyword_arguments):
            if get_origin(kwarg.type_) is Union:
                element_type = get_args(kwarg.type_)[0]
            else:
                element_type = kwarg.type_

            hint, absolute_symbol = construct_import_path(element_type)

            row = [kwarg.name]
            row.append(hint or absolute_symbol)
            parameter_table.append(row)

            if hint:
                import_block += f"{hint}\n"
            parameter_block += f"{' '*8}{kwarg.name}: {absolute_symbol},"

            if index != arguments_count - 1:
                parameter_block += "\n"

        if len(parameter_table) > 1:
            md.table(parameter_table)

        md.code(
            EXAMPLE_EVENT_TEMPLATE.format(
                import_block=import_block,
                event_name=event_name,
                parameters=parameter_block,
            ),
            language="python",
        )

    md.to_file(output_file_path)
    print(f"成功生成{output_file_path}文件")


event_doc_prefix = f"{root_api_prefix}/事件参数"

cleanup(event_doc_prefix)

with open(f"{event_doc_prefix}/概览.md", "w", encoding="utf-8") as f:
    f.write(
        """\
---
slug: /event/
---\
"""
    )

generate_event_doc(
    UniversalEvent,
    f"{event_doc_prefix}/跨平台",
)
generate_event_doc(
    KeaimaoEvent,
    f"{event_doc_prefix}/可爱猫",
)
generate_event_doc(
    OnebotV11Event,
    f"{event_doc_prefix}/Onebot",
)
generate_event_doc(
    TelegramEvent,
    f"{event_doc_prefix}/Telegram",
)
