from random import random
from typing import (
    Any,
    Dict,
    List,
    Literal,
    Optional,
    Tuple,
    Type,
    TypeVar,
    Union,
    overload,
)

from pepperbot.adapters.onebot.message.segment import OnebotFace, OnebotShare
from pepperbot.core.message.base import BaseMessageSegment
from pepperbot.exceptions import EventHandleError

from pepperbot.utils.common import DictNoNone
from devtools import debug


class At(BaseMessageSegment):
    @overload
    def __init__(self, userId: str):
        ...

    @overload
    def __init__(self, userId: Dict):
        ...

    def __init__(self, userId: Union[dict, str]):

        data = userId

        # todo pydantic pydantic
        # 这个str和int不一致，判断has的时候，排查了半天
        if isinstance(data, dict):
            identifier = int(data["data"]["qq"])

            for key, value in data.items():
                setattr(self, key, value)

            self.formatted = {**data}
        else:
            identifier = data

            self.qq = data

            self.formatted = {"type": "at", "data": {"qq": data}}

        super().__init__(**{"identifier": identifier})


def onebot_text_factory(raw_segment: Dict):
    content: str = raw_segment["data"]["text"]
    return Text(content)


def keaimao_text_factory(raw_event: Dict):
    return Text(raw_event["msg"])


class Text(BaseMessageSegment):
    universal = ("onebot", "keaimao")
    __slots__ = (
        "onebot",
        "keaimao",
        "content",
    )

    def __init__(self, content: str):

        self.content = content

        self.onebot = {
            "type": "text",
            "data": {"text": content},
        }
        self.keaimao = content

        super().__init__(**{"identifier": content})


def validate_onebot_image_file_path(path: str):
    prefix = path.split("://")[0]
    if prefix not in ("file", "http", "https", "base64"):
        if ":/" in path:  # 微信会直接将收到的图片保存至本地
            return f"file:///{path}"
        else:
            raise EventHandleError(f"无法解析的图片路径 {path}")

    return path


def onebot_image_factory(raw_segment: Dict):
    file_path = raw_segment["data"].get("url")
    if not file_path:
        raise Exception("无法解析图片地址")

    file_path = validate_onebot_image_file_path(file_path)

    return Image(file_path)


def keaimao_image_factory(raw_event: Dict):
    file_path = raw_event["msg"]
    file_path = validate_onebot_image_file_path(file_path)
    return Image(file_path)


class Image(BaseMessageSegment):
    """
    微信只支持URL方式

    QQ支持：

    绝对路径，例如 file:///C:\\Users\\Richard\\Pictures\\1.png，格式使用 file URI

    网络 URL，例如 http://i1.piimg.com/567571/fdd6e7b6d93f1ef0.jpg

    Base64 编码，例如 base64://iVBORw0

    """

    universal = ("onebot", "keaimao")
    __slots__ = ("onebot",)

    def __init__(self, file_path: str, mode: Optional[Literal["flash"]] = None):

        self.file_path = file_path
        self.mode = mode

        # debug(file_path)
        self.onebot = {
            "type": "image",
            "data": {
                "file": file_path,
                "url": file_path,
            },
        }

        super().__init__(**{"identifier": file_path})

    @property
    def keaimao(self):
        if not self.file_path and not self.file_path.startswith("http"):
            raise EventHandleError(f"可爱猫仅支持发送URL格式的图片")

        return {
            "name": f"{random()}.png",
            "url": self.file_path,
        }

    def download(self):
        # todo download
        pass

    def to_flash(self):
        self.onebot["data"]["type"] = "flash"

        return self

    def un_flash(self):
        if self.onebot["data"].get("type"):
            del self.onebot["data"]["type"]

        return self


class Poke(BaseMessageSegment):
    universal = ("onebot", "keaimao")

    @overload
    def __init__(
        self,
        qq: int,
    ):
        ...

    @overload
    def __init__(self, qq: Dict):
        ...

    def __init__(
        self,
        qq: Union[Dict, int],
    ):

        data = qq

        if isinstance(data, dict):
            identifier = data["data"]["url"]

            for key, value in data.items():
                setattr(self, key, value)

            self.formatted = {**data}
        else:
            identifier = data

            self.formatted = {
                "type": "poke",
                "data": {"qq": qq},
            }

        super().__init__(**{"identifier": identifier})


# class Poke(BaseMessageSegment):
#     @overload
#     def __init__(self, data: Dict):
#         ...

#     @overload
#     def __init__(
#         self,
#         data: int,
#         id: int,
#     ):
#         ...

#     def __init__(
#         self,
#         data: Union[Dict, int],
#         id: Optional[int] = None,
#     ):

#         if isinstance(data, dict):
#             url = data["url"]

#             for key, value in data.items():
#                 setattr(self, key, value)
#         else:
#             if not (data or id):
#                 raise Exception("必须提供mode和id")

#             url = data

#         super().__init__(**{"identifier": url})

#         kwargs = DictNoNone()
#         kwargs["type"] = data
#         kwargs["id"] = id

#         self.formatted = {
#             "type": "poke",
#             "data": {
#                 **kwargs,
#             },
#         }


class Reply(BaseMessageSegment):
    @overload
    def __init__(self, messageId: str):
        ...

    @overload
    def __init__(self, messageId: Dict):
        ...

    def __init__(self, messageId: Union[dict, str]):

        data = messageId

        if isinstance(data, dict):
            identifier = data["data"]["id"]

            for key, value in data.items():
                setattr(self, key, value)

            self.formatted = {**data}
        else:
            identifier = data

            self.formatted = {"type": "reply", "data": {"id": f"{data}"}}

        super().__init__(**{"identifier": identifier})


class Audio(BaseMessageSegment):
    @overload
    def __init__(
        self,
        path: str,
    ):
        ...

    @overload
    def __init__(self, path: Dict):
        ...

    def __init__(self, path: Union[dict, str]):

        data = path

        if isinstance(data, dict):
            identifier = data["data"]["file"]

            for key, value in data.items():
                setattr(self, key, value)

            self.formatted = {**data}
        else:
            identifier = data

            self.formatted = {"type": "record", "data": {"file": data}}

        super().__init__(**{"identifier": identifier})


class Video(BaseMessageSegment):
    @overload
    def __init__(
        self,
        path: str,
    ):
        ...

    @overload
    def __init__(self, path: Dict):
        ...

    def __init__(self, path: Union[dict, str]):

        data = path

        if isinstance(data, dict):
            identifier = data["data"]["file"]

            for key, value in data.items():
                setattr(self, key, value)

            self.formatted = {**data}
        else:
            identifier = data

            self.formatted = {"type": "video", "data": {"file": data}}

        super().__init__(**{"identifier": identifier})


class Music(BaseMessageSegment):
    @overload
    def __init__(self, id: str, source: Literal["qq", "163", "xm"] = "qq"):
        ...

    @overload
    def __init__(self, id: Dict):
        ...

    def __init__(self, id: Union[dict, str], source: Literal["qq", "163", "xm"] = "qq"):

        data = id

        if isinstance(data, dict):
            identifier = data["data"]["id"] + data["data"]["type"]

            for key, value in data.items():
                setattr(self, key, value)

            self.formatted = {**data}
        else:
            identifier = data + source

            self.formatted = {"type": "music", "data": {"type": source, "id": id}}

        super().__init__(**{"identifier": identifier})


T_SegmentClass = Union[
    Type[At],
    Type[Music],
    Type[Audio],
    Type[Image],
    Type[Reply],
    Type[Text],
    Type[OnebotFace],
    Type[Video],
    Type[Poke],
    Type[OnebotShare],
]
T_SegmentInstance = Union[
    At,
    Text,
    OnebotFace,
    Music,
    Audio,
    Image,
    Reply,
    Video,
    Poke,
    OnebotShare,
]
GT_SegmentInstance = TypeVar(
    "GT_SegmentInstance",
    At,
    Text,
    OnebotFace,
    Music,
    Audio,
    Image,
    Reply,
    Video,
    Poke,
    OnebotShare,
)
T_SegmentClassOrInstance = Union[T_SegmentClass, T_SegmentInstance]
GT_SegmentClassOrInstance = TypeVar(
    "GT_SegmentClassOrInstance",
    T_SegmentClass,
    T_SegmentInstance
    # At,
    # Text,
    # Face,
    # Music,
    # Audio,
    # Image,
    # Reply,
    # Type[At],
    # Type[Music],
    # Type[Audio],
    # Type[Image],
    # Type[Reply],
    # Type[Text],
    # Type[Face],
)
