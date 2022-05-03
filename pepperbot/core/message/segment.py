import os
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
)

from devtools import debug
from pepperbot.core.message.base import BaseMessageSegment
from pepperbot.exceptions import EventHandleError
from pepperbot.store.meta import get_telegram_caller
from pyrogram.enums.parse_mode import ParseMode
from pyrogram.types import Message


async def telegram_download_media(file_id: str, file_name: str):
    """
    通过client.download_media，获取到文件的filepath，实现跨平台转发

    https://docs.pyrogram.org/api/methods/download_media?highlight=download_media#pyrogram.Client.download_media
    """
    client = get_telegram_caller()

    await client.download_media(file_id, file_name=file_name)

    file_path = f"file:///{os.getcwd()}/downloads/{file_name}"

    return file_path


class At(BaseMessageSegment):
    __slots__ = ("user_id",)

    def __init__(self, user_id: str):

        self.user_id = user_id

        super().__init__(**{"identifier": user_id})

    async def onebot(self):
        return {
            "type": "at",
            "data": {
                "qq": self.user_id,
            },
        }


def onebot_at_factory(raw_segment: Dict):
    content = str(raw_segment["data"]["qq"])
    return At(content)


class Audio(BaseMessageSegment):
    __slots__ = (
        "temporary_file_path",
        "telegram_lazy_download",
        "file_path",
    )

    def __init__(
        self,
        file_path: str,
        telegram_lazy_download=False,
    ):

        self.temporary_file_path = file_path
        self.telegram_lazy_download = telegram_lazy_download
        self.file_path = ""

        super().__init__(**{"identifier": file_path})

    async def get_file_path(self):
        # only when protocol is telegram, we need to lazy download
        if not self.telegram_lazy_download:
            return self.temporary_file_path

        # file_path is actually pyrogram file_id now
        if self.file_path:
            return self.file_path

        file_name = f"{random()}.wav"

        # lazy download when transfering to other platfrom for better performance
        # download huge file with delay the execution of event handler
        # unless using separate process or thread for downloading
        file_path = await telegram_download_media(self.temporary_file_path, file_name)
        self.file_path = file_path
        return file_path

    async def onebot(self):
        await self.get_file_path()

        return {
            "type": "record",
            "data": {
                "file": self.file_path,
            },
        }


def onebot_audio_factory(raw_segment: Dict):
    path: str = raw_segment["data"]["file"]
    return Audio(path)


class Image(BaseMessageSegment):
    """
    微信只支持URL方式

    QQ支持：

    绝对路径，例如 file:///C:\\Users\\Richard\\Pictures\\1.png，格式使用 file URI

    网络 URL，例如 http://i1.piimg.com/567571/fdd6e7b6d93f1ef0.jpg

    Base64 编码，例如 base64://iVBORw0

    """

    __slots__ = (
        "mode",
        "temporary_file_path",
        "telegram_lazy_download",
        "file_path",
    )

    def __init__(
        self,
        file_path: str,
        mode: Optional[Literal["flash"]] = None,
        telegram_lazy_download=False,
    ):

        self.temporary_file_path = file_path
        self.mode = mode
        self.telegram_lazy_download = telegram_lazy_download
        self.file_path = ""

        super().__init__(**{"identifier": file_path})

    async def get_file_path(self):
        # only when protocol is telegram, we need to lazy download
        if not self.telegram_lazy_download:
            return self.temporary_file_path

        # file_path is actually pyrogram file_id now
        if self.file_path:
            return self.file_path

        file_name = f"{random()}.jpg"

        # lazy download when transfering to other platfrom for better performance
        # download huge file with delay the execution of event handler
        # unless using separate process or thread for downloading
        file_path = await telegram_download_media(self.temporary_file_path, file_name)
        self.file_path = file_path
        return file_path

    async def onebot(self):
        await self.get_file_path()

        temp = {
            "type": "image",
            "data": {
                "file": self.file_path,
                "url": self.file_path,
            },
        }

        if self.mode == "flash":
            temp["data"]["type"] = "flash"

    async def keaimao(self):
        await self.get_file_path()

        if not self.file_path.startswith("http"):
            raise EventHandleError(f"可爱猫仅支持通过URL发送图片")

        return {
            "name": f"{random()}.jpg",
            "url": self.file_path,
        }

    async def telegram(self):
        await self.get_file_path()

        return {
            "photo": self.file_path,
        }

    def download(self):
        # todo download
        pass

    def onebot_to_flash(self):
        self.mode = "flash"

        return self

    def onebot_un_flash(self):
        self.mode = None

        return self

    def onebot_is_flash(self) -> bool:
        return self.mode == "flash"


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


async def telegram_image_factory(raw_event: Dict):
    message: Message = raw_event["callback_object"]
    return Image(message.photo.file_id, telegram_lazy_download=True)


class Music(BaseMessageSegment):
    __slots__ = (
        "music_id",
        "source",
    )

    def __init__(self, music_id: str, source: Literal["qq", "163", "xm"] = "qq"):

        self.music_id = music_id
        self.source = source

        super().__init__(**{"identifier": music_id + source})

    async def onebot(self):
        return {
            "type": "music",
            "data": {
                "type": self.source,
                "id": self.music_id,
            },
        }

    async def keaimao(self):
        return {
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


class OnebotFace(BaseMessageSegment):
    __slots__ = ("face_id",)

    def __init__(self, face_id: int):

        self.face_id = face_id

        super().__init__(**{"identifier": face_id})

    async def onebot(self):
        return {
            "type": "face",
            "data": {
                "id": self.face_id,
            },
        }


def onebot_face_factory(raw_segment: Dict):
    content = raw_segment["data"]["id"]
    return OnebotFace(int(content))


class OnebotShare(BaseMessageSegment):
    __slots__ = (
        "url",
        "title",
        "content",
        "image_url",
    )

    def __init__(
        self,
        url: str,
        title: str = "",
        content: Optional[str] = None,
        image_url: Optional[str] = None,
    ):

        self.url = url
        self.title = title
        self.content = content
        self.image_url = image_url

        super().__init__(**{"identifier": url})

    async def onebot(self):
        return {
            "type": "share",
            "data": {
                "file": self.url,
                "title": self.title,
                "content": self.content,
                "image_url": self.image_url,
            },
        }


class Poke(BaseMessageSegment):
    __slots__ = ("user_id",)

    def __init__(self, user_id: str):

        self.user_id = user_id

        super().__init__(**{"identifier": user_id})

    async def onebot(self):
        return {
            "type": "poke",
            "data": {
                "qq": self.user_id,
            },
        }


def onebot_poke_factory(raw_segment: Dict):
    user_id = str(raw_segment["data"]["qq"])
    return Poke(user_id)


class Reply(BaseMessageSegment):
    __slots__ = ("message_id",)

    def __init__(self, message_id: str):

        self.message_id = message_id

        super().__init__(**{"identifier": message_id})

    async def onebot(self):
        return {
            "type": "reply",
            "data": {
                "id": self.message_id,
            },
        }


def onebot_reply_factory(raw_segment: Dict):
    message_id = str(raw_segment["data"]["id"])
    return Reply(message_id)


class Text(BaseMessageSegment):
    __slots__ = ("content",)

    def __init__(self, content: str):

        self.content = content

        super().__init__(**{"identifier": content})

    async def onebot(self):
        return {
            "type": "text",
            "data": {
                "text": self.content,
            },
        }

    async def keaimao(self):
        return self.content

    async def telegram(self):
        return {
            "text": self.content,
            "parse_mode": ParseMode.MARKDOWN,
        }


def onebot_text_factory(raw_segment: Dict):
    content: str = raw_segment["data"]["text"]
    return Text(content)


def keaimao_text_factory(raw_event: Dict):
    return Text(raw_event["msg"])


def telegram_text_factory(raw_event: Dict):
    message: Message = raw_event["callback_object"]
    return Text(message.text)


class Video(BaseMessageSegment):
    __slots__ = (
        "temporary_file_path",
        "telegram_lazy_download",
        "file_path",
    )

    def __init__(
        self,
        file_path: str,
        telegram_lazy_download=False,
    ):

        self.temporary_file_path = file_path
        self.telegram_lazy_download = telegram_lazy_download
        self.file_path = ""

        super().__init__(**{"identifier": file_path})

    async def get_file_path(self):
        # only when protocol is telegram, we need to lazy download
        if not self.telegram_lazy_download:
            return self.temporary_file_path

        # file_path is actually pyrogram file_id now
        if self.file_path:
            return self.file_path

        file_name = f"{random()}.mp4"

        # lazy download when transfering to other platfrom for better performance
        # download huge file with delay the execution of event handler
        # unless using separate process or thread for downloading
        file_path = await telegram_download_media(self.temporary_file_path, file_name)
        self.file_path = file_path
        return file_path

    async def onebot(self):
        await self.get_file_path()

        return {
            "type": "video",
            "data": {
                "file": self.file_path,
            },
        }

    async def keaimao(self):
        await self.get_file_path()

        if not self.file_path.startswith("http"):
            raise EventHandleError(f"可爱猫仅支持通过URL发送视频")

        return {
            "name": f"{random()}.mp4",
            "url": self.file_path,
        }

    async def telegram(self):
        await self.get_file_path()

        return {
            "video": self.file_path,
        }


def onebot_video_factory(raw_segment: Dict):
    path: str = raw_segment["data"]["file"]
    return Video(path)


def keaimao_video_factory(raw_segment: Dict):
    path: str = raw_segment["msg"]
    return Video(validate_image_path(path))


def telegram_video_factory(raw_event: Dict):
    message: Message = raw_event["callback_object"]
    return Video(message.video.file_id)


class Voice(BaseMessageSegment):
    pass


# def telegram_sticker_factory(raw_event: Dict):
#     # message: Message = raw_event["callback_object"]
#     # return Text(message.text)
#     return None


T_SegmentClass = Union[
    Type[At],
    Type[Audio],
    Type[Image],
    Type[Music],
    Type[OnebotFace],
    Type[OnebotShare],
    Type[Poke],
    Type[Reply],
    Type[Text],
    Type[Video],
    Type[Voice],
]
T_SegmentInstance = Union[
    At,
    Audio,
    Image,
    Music,
    OnebotFace,
    OnebotShare,
    Poke,
    Reply,
    Text,
    Video,
    Voice,
]
GT_SegmentInstance = TypeVar(
    "GT_SegmentInstance",
    At,
    Audio,
    Image,
    Music,
    OnebotFace,
    OnebotShare,
    Poke,
    Reply,
    Text,
    Video,
    Voice,
)
T_SegmentClassOrInstance = Union[T_SegmentClass, T_SegmentInstance]
GT_SegmentClassOrInstance = TypeVar(
    "GT_SegmentClassOrInstance",
    T_SegmentClass,
    T_SegmentInstance,
)
