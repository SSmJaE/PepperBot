from typing import List, Optional, Union, get_args, get_origin

from devtools import debug

from pepperbot.core.message.segment import Image


types = [
    # Union[Image, str],
    str,
    Image,
    List[str],
    List[Image],
    Optional[str],
    Optional[Image],
    Optional[List[str]],
    Optional[List[Image]],
]


def test_type():
    for type_ in types:
        container_type = get_origin(type_)  # None，如果没有
        element_types = get_args(type_)  # 如果没有容器，则为空tuple

        debug(type_, container_type, element_types)

    assert False == True
