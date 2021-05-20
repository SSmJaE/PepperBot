from abc import ABC
from typing import Any, Dict, List, Literal, Optional, Union, overload

from devtools import debug

from src.utils.common import DictNoNone


class MessageSegMentBase:
    def __init__(self, identifier: Any):
        self.identifier = identifier

    def __str__(self) -> str:
        return f"Segment[{self.__class__.__name__}, {self.identifier}]"

    def __repr__(self) -> str:
        return f"Segment[{self.__class__.__name__}, {self.identifier}]"

    def __eq__(self, other: "MessageSegMentBase") -> bool:
        if type(self) == type(other):
            if self.identifier == other.identifier:
                return True
        return False


class At(MessageSegMentBase):
    def __init__(self, data: Union[dict, int]):

        if isinstance(data, dict):
            # todo pydantic pydantic
            # 这个str和int不一致，判断has的时候，排查了半天
            userId = int(data["qq"])

            for key, value in data.items():
                setattr(self, key, value)
        else:
            userId = data

        super().__init__(**{"identifier": userId})

        self.formatted = {"type": "at", "data": {"qq": userId}}


class Text(MessageSegMentBase):
    def __init__(self, data: Union[dict, str]):

        if isinstance(data, dict):
            text = data["text"]

            for key, value in data.items():
                setattr(self, key, value)
        else:
            text = data

        super().__init__(**{"identifier": text})

        self.formatted = {"type": "text", "data": {"text": text}}


class Face(MessageSegMentBase):
    def __init__(self, data: Union[dict, int]):

        if isinstance(data, dict):
            id = data["id"]

            for key, value in data.items():
                setattr(self, key, value)
        else:
            id = data

        super().__init__(**{"identifier": id})

        self.formatted = {"type": "face", "data": {"id": id}}


class Image(MessageSegMentBase):
    """
    除了支持使用收到的图片文件名直接发送外，还支持：
    绝对路径，例如 file:///C:\\Users\\Richard\\Pictures\\1.png，格式使用 file URI
    网络 URL，例如 http://i1.piimg.com/567571/fdd6e7b6d93f1ef0.jpg
    Base64 编码，例如 base64://iVBORw0
    """

    @overload
    def __init__(self, data: Dict):
        ...

    @overload
    def __init__(self, data: str, mode: Optional[Literal["flash"]] = None):
        ...

    def __init__(self, data: Union[Dict, str], mode: Optional[Literal["flash"]] = None):

        if isinstance(data, dict):
            url = data.get("file")
            if not url:
                raise Exception("无法解析图片地址")

            for key, value in data.items():
                setattr(self, key, value)
        else:
            url = data

        super().__init__(**{"identifier": url})

        kwargs = DictNoNone()
        kwargs["type"] = mode

        self.formatted = {"type": "image", "data": {**kwargs, "file": url}}

    def download(self):
        # todo download
        pass


class Share(MessageSegMentBase):
    @overload
    def __init__(self, data: Dict):
        ...

    @overload
    def __init__(
        self,
        data: str,
        title: str,
        content: Optional[str] = None,
        imageUrl: Optional[str] = None,
    ):
        ...

    def __init__(
        self,
        data: Union[Dict, str],
        title: str = "",
        content: Optional[str] = None,
        imageUrl: Optional[str] = None,
    ):

        if isinstance(data, dict):
            url = data["url"]

            for key, value in data.items():
                setattr(self, key, value)
        else:
            url = data

        super().__init__(**{"identifier": url})

        kwargs = DictNoNone()
        kwargs["title"] = title
        kwargs["content"] = content
        kwargs["image"] = imageUrl

        self.formatted = {"type": "share", "data": {**kwargs, "file": url}}


class Poke(MessageSegMentBase):
    @overload
    def __init__(self, qq: Dict):
        ...

    @overload
    def __init__(
        self,
        qq: int,
    ):
        ...

    def __init__(
        self,
        qq: Union[Dict, int],
    ):

        data = qq

        if isinstance(data, dict):
            identifier = data["url"]

            for key, value in data.items():
                setattr(self, key, value)
        else:
            if not (data or id):
                raise Exception("必须提供mode和id")

            identifier = data

        super().__init__(**{"identifier": identifier})

        self.formatted = {
            "type": "poke",
            "data": {"qq": qq},
        }


# class Poke(MessageSegMentBase):
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


class Reply(MessageSegMentBase):
    def __init__(self, data: Union[dict, int]):

        if isinstance(data, dict):
            messageId = data["id"]

            for key, value in data.items():
                setattr(self, key, value)
        else:
            messageId = data

        super().__init__(**{"identifier": messageId})

        self.formatted = {"type": "reply", "data": {"id": f"{messageId}"}}


class Audio(MessageSegMentBase):
    def __init__(self, data: Union[dict, str]):

        if isinstance(data, dict):
            url = data["file"]

            for key, value in data.items():
                setattr(self, key, value)
        else:
            url = data

        super().__init__(**{"identifier": url})

        self.formatted = {"type": "record", "data": {"file": url}}


class Video(MessageSegMentBase):
    def __init__(self, data: Union[dict, str]):

        if isinstance(data, dict):
            url = data["file"]

            for key, value in data.items():
                setattr(self, key, value)
        else:
            url = data

        super().__init__(**{"identifier": url})

        self.formatted = {"type": "video", "data": {"file": url}}


class Music(MessageSegMentBase):
    def __init__(
        self, data: Union[dict, str], source: Literal["qq", "163", "xm"] = "qq"
    ):

        if isinstance(data, dict):
            id = data["id"]
            source = data["type"]

            for key, value in data.items():
                setattr(self, key, value)
        else:
            id = data
            source = source

        super().__init__(**{"identifier": id})

        self.formatted = {"type": "music", "data": {"type": source, "id": id}}
