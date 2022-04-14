from random import randint, random
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
    universal = ("onebot",)
    __slots__ = (
        "onebot",
        # "keaimao",
        "user_id",
    )

    def __init__(self, user_id: str):

        self.user_id = user_id
        super().__init__(**{"identifier": user_id})

        self.onebot = {"type": "at", "data": {"qq": user_id}}


def onebot_at_factory(raw_segment: Dict):
    content = str(raw_segment["data"]["qq"])
    return At(content)


class Text(BaseMessageSegment):
    universal = ("onebot", "keaimao")
    __slots__ = (
        "onebot",
        "keaimao",
        "content",
    )

    def __init__(self, content: str):

        self.content = content
        super().__init__(**{"identifier": content})

        self.onebot = {
            "type": "text",
            "data": {"text": content},
        }
        self.keaimao = content


def onebot_text_factory(raw_segment: Dict):
    content: str = raw_segment["data"]["text"]
    return Text(content)


def keaimao_text_factory(raw_event: Dict):
    return Text(raw_event["msg"])


class Image(BaseMessageSegment):
    """
    微信只支持URL方式

    QQ支持：

    绝对路径，例如 file:///C:\\Users\\Richard\\Pictures\\1.png，格式使用 file URI

    网络 URL，例如 http://i1.piimg.com/567571/fdd6e7b6d93f1ef0.jpg

    Base64 编码，例如 base64://iVBORw0

    """

    universal = ("onebot", "keaimao")
    __slots__ = (
        "onebot",
        "file_path",
        "mode",
    )

    def __init__(self, file_path: str, mode: Optional[Literal["flash"]] = None):

        self.file_path = file_path
        self.mode = mode
        super().__init__(**{"identifier": file_path})

        # debug(file_path)
        self.onebot = {
            "type": "image",
            "data": {
                "file": file_path,
                "url": file_path,
            },
        }

    @property
    def keaimao(self):
        if not self.file_path.startswith("http"):
            raise EventHandleError(f"可爱猫仅支持通过URL发送图片")

        return {
            "name": f"{random()}.png",
            "url": self.file_path,
        }

    def download(self):
        # todo download
        pass

    def onebot_to_flash(self):
        self.onebot["data"]["type"] = "flash"

        return self

    def onebot_un_flash(self):
        if self.onebot["data"].get("type"):
            del self.onebot["data"]["type"]

        return self


def validate_image_path(path: str):
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

    file_path = validate_image_path(file_path)

    return Image(file_path)


def keaimao_image_factory(raw_event: Dict):
    file_path = raw_event["msg"]
    file_path = validate_image_path(file_path)
    return Image(file_path)


class Poke(BaseMessageSegment):
    universal = ("onebot",)

    def __init__(self, user_id: str):

        identifier = user_id
        super().__init__(**{"identifier": identifier})

        self.onebot = {
            "type": "poke",
            "data": {"qq": user_id},
        }


def onebot_poke_factory(raw_segment: Dict):
    user_id = str(raw_segment["data"]["qq"])
    return Poke(user_id)


class Audio(BaseMessageSegment):
    universal = ("onebot",)

    def __init__(self, path: str):

        identifier = path
        super().__init__(**{"identifier": identifier})

        self.onebot = {
            "type": "record",
            "data": {
                "file": path,
            },
        }


def onebot_audio_factory(raw_segment: Dict):
    path: str = raw_segment["data"]["file"]
    return Audio(path)


class Video(BaseMessageSegment):
    universal = ("onebot", "keaimao")

    def __init__(self, file_path: str):

        identifier = file_path
        super().__init__(**{"identifier": identifier})
        self.file_path = file_path

        self.onebot = {"type": "video", "data": {"file": file_path}}

    @property
    def keaimao(self):
        if not self.file_path.startswith("http"):
            raise EventHandleError(f"可爱猫仅支持通过URL发送视频")

        return {
            "name": f"{random()}.mp4",
            "url": self.file_path,
        }


def onebot_video_factory(raw_segment: Dict):
    path: str = raw_segment["data"]["file"]
    return Video(path)


def keaimao_video_factory(raw_segment: Dict):
    path: str = raw_segment["msg"]
    return Video(validate_image_path(path))


class Music(BaseMessageSegment):
    universal = ("onebot",)

    def __init__(self, music_id: str, source: Literal["qq", "163", "xm"] = "qq"):

        identifier = music_id + source
        super().__init__(**{"identifier": identifier})

        self.onebot = {
            "type": "music",
            "data": {
                "type": source,
                "id": music_id,
            },
        }

        self.keaimao = {
            "name": "\u6211\u8981\u4f60",
            "type": 0,
        }


def onebot_music_factory(raw_segment: Dict):
    music_id = str(raw_segment["data"]["id"])
    source: str = raw_segment["data"]["type"]
    return Music(music_id, source)  # type:ignore


def keaimao_music_factory(raw_segment: Dict):
    path: str = raw_segment["msg"]
    return Music(validate_image_path(path))


class Reply(BaseMessageSegment):
    universal = ("onebot",)

    def __init__(self, message_id: str):

        identifier = message_id
        super().__init__(**{"identifier": identifier})

        self.onebot = {
            "type": "reply",
            "data": {
                "id": message_id,
            },
        }


def onebot_reply_factory(raw_segment: Dict):
    message_id = str(raw_segment["data"]["id"])
    return Reply(message_id)


T_SegmentClass = Union[
    Type[At],
    Type[Music],
    Type[Audio],
    Type[Image],
    Type[Text],
    Type[OnebotFace],
    Type[Video],
    Type[Reply],
    Type[Poke],
    Type[OnebotShare],
]
T_SegmentInstance = Union[
    At,
    Text,
    Music,
    Audio,
    Image,
    Video,
    Poke,
    Reply,
    OnebotFace,
    OnebotShare,
]
GT_SegmentInstance = TypeVar(
    "GT_SegmentInstance",
    At,
    Text,
    Music,
    Audio,
    Image,
    Video,
    Poke,
    Reply,
    OnebotFace,
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
