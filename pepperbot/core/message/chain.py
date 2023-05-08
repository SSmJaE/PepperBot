import re
from pprint import pprint
from random import random
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Coroutine,
    Dict,
    List,
    Optional,
    Tuple,
    Union,
    cast,
)

from devtools import debug
from pepperbot.core.message.base import BaseMessageSegment

# if TYPE_CHECKING:
from pepperbot.core.message.segment import (
    At,
    Audio,
    Image,
    Music,
    OnebotFace,
    OnebotShare,
    Poke,
    Reply,
    T_SegmentClass,
    T_SegmentClassOrInstance,
    T_SegmentInstance,
    Text,
    Video,
    Voice,
    keaimao_image_factory,
    keaimao_text_factory,
    keaimao_video_factory,
    onebot_at_factory,
    onebot_audio_factory,
    onebot_face_factory,
    onebot_image_factory,
    onebot_poke_factory,
    onebot_reply_factory,
    onebot_text_factory,
    onebot_video_factory,
    telegram_image_factory,
    telegram_text_factory,
    telegram_video_factory,
)
from pepperbot.exceptions import EventHandleError
from pepperbot.extensions.log import logger
from pepperbot.store.event import EventMetadata
from pepperbot.types import T_BotProtocol, T_ConversationType
from pepperbot.utils.common import await_or_sync
from pyrogram.enums.message_media_type import MessageMediaType


ONEBOT_SEGMENT_FACTORY_MAPPING: Dict[str, Callable[[Dict], T_SegmentInstance]] = {
    "at": onebot_at_factory,
    "record": onebot_audio_factory,
    "image": onebot_image_factory,
    "face": onebot_face_factory,
    "poke": onebot_poke_factory,
    "reply": onebot_reply_factory,
    "text": onebot_text_factory,
    "video": onebot_video_factory,
}

KEAIMAO_SEGMENT_FACTORY_MAPPING: Dict[int, Callable[[Dict], T_SegmentInstance]] = {
    3: keaimao_image_factory,
    1: keaimao_text_factory,
    43: keaimao_video_factory,
}

TELEGRAM_SEGMENT_FACTORY_MAPPING: Dict[
    Optional[MessageMediaType],
    Callable[[Dict], Union[T_SegmentInstance, Coroutine[Any, Any, T_SegmentInstance]]],
] = {
    MessageMediaType.PHOTO: telegram_image_factory,
    None: telegram_text_factory,
    MessageMediaType.VIDEO: telegram_video_factory,
    # MessageMediaType.STICKER: telegram_sticker_factory,
}


async def construct_segments(
    protocol: T_BotProtocol, mode: T_ConversationType, raw_event: Dict
) -> List[T_SegmentInstance]:
    result: List[T_SegmentInstance] = []

    if protocol == "onebot":
        raw_chain: List[dict] = raw_event.get("message", list)
        for raw_segment in raw_chain:
            segment_type: str = raw_segment["type"]

            segment_factory = ONEBOT_SEGMENT_FACTORY_MAPPING.get(segment_type)
            if not segment_factory:
                # raise EventHandleError()
                logger.error(f"尚未适配的 {protocol} 消息类型 {segment_type}，将忽略该消息片段")
                continue

            segment_instance = segment_factory(raw_segment)
            result.append(segment_instance)

    elif protocol == "keaimao":
        message_type: int = raw_event["type"]
        message_factory = KEAIMAO_SEGMENT_FACTORY_MAPPING.get(message_type)
        if not message_factory:
            # raise EventHandleError(f"尚未适配的可爱猫消息类型")
            logger.error(f"尚未适配的 {protocol} 消息类型 {message_type}，将忽略该消息片段")
            return []

        segment_instance = message_factory(raw_event)
        result.append(segment_instance)

    elif protocol == "telegram":
        telegram_message_type: Optional[MessageMediaType] = getattr(
            raw_event["callback_object"], "media", None
        )
        message_factory = TELEGRAM_SEGMENT_FACTORY_MAPPING.get(telegram_message_type)
        if not message_factory:
            # raise EventHandleError(f"尚未适配的 telegram 消息类型")
            logger.error(f"尚未适配的 {protocol} 消息类型 {telegram_message_type}，将忽略该消息片段")
            return []

        segment_instance = await await_or_sync(message_factory, raw_event)
        result.append(segment_instance)

    else:
        raise EventHandleError(f"尚未支持 {protocol} 的消息链构造")

    # debug(result)
    return result


async def chain_factory(event_meta: EventMetadata):
    chain = MessageChain(
        event_meta.protocol,
        # 能够构造MessageChain的事件，一定可以获取到conversation_type
        cast(T_ConversationType, event_meta.conversation_type),
        event_meta.raw_event,
        event_meta.source_id,
        event_meta.user_id,
    )
    await chain.construct()
    return chain


class MessageChain:
    __slots__ = (
        "id",
        "segments",
        "raw_event",
        "source_id",
        "user_id",
        "protocol",
        "mode",
        "onebot_message_id",
    )

    onebot_message_id: str

    def __init__(
        self,
        protocol: T_BotProtocol,
        mode: T_ConversationType,
        raw_event: Dict,
        source_id: str,
        user_id: str,
    ) -> None:
        # debug(locals())

        self.id = random()
        self.segments: List[T_SegmentInstance] = []

        self.raw_event = raw_event
        self.source_id = source_id
        self.user_id = user_id
        self.protocol = protocol
        self.mode = mode

        self.onebot_message_id = raw_event.get("message_id", "")

    async def construct(self):
        self.segments = await construct_segments(
            self.protocol,  # type:ignore
            self.mode,  # type:ignore
            self.raw_event,
        )

    # def __repr__(self) -> str:
    #     json.dumps

    def __equal(self, segment: "BaseMessageSegment", other: T_SegmentClassOrInstance):
        # 如果是实例，data是否相等
        if isinstance(other, BaseMessageSegment):
            if segment == other:
                return True

        # 是否是同一类型
        else:
            if type(segment) == other:
                return True

        return False

    # todo part in raw operator in
    # if

    def has(self, other: T_SegmentClassOrInstance):
        for segment in self.segments:
            if self.__equal(segment, other):
                return True

        return False

    def has_and_first(
        self, other: T_SegmentClassOrInstance
    ) -> Tuple[bool, T_SegmentInstance]:
        for segment in self.segments:
            if self.__equal(segment, other):
                return True, segment

        # 返回Text只是为了提供更好的类型注解，因为python并不能自动判断union类型的分支情况
        # 即 True => type1 , False => type2
        # generic可以，不过还是直接Text("")最简单
        return False, Text("")

    def has_and_last(self, other: T_SegmentClassOrInstance):
        for segment in reversed(self.segments):
            if self.__equal(segment, other):
                return True, segment

        return False, Text("")

    def has_and_all(self, other: T_SegmentClassOrInstance):
        results = []

        for segment in self.segments:
            if self.__equal(segment, other):
                results.append(segment)

        if len(results):
            return True, results
        return False, Text("")

    def __getItems(self, type_: T_SegmentClass):
        results = []

        for segment in self.segments:
            if isinstance(segment, type_):
                results.append(segment)

        return results

    @property
    def at(self) -> List[At]:
        return self.__getItems(At)

    @property
    def onebot_faces(self) -> List[OnebotFace]:
        return self.__getItems(OnebotFace)

    @property
    def audio(self) -> List[Audio]:
        return self.__getItems(Audio)

    @property
    def images(self) -> List[Image]:
        return self.__getItems(Image)

    @property
    def replies(self) -> List[Reply]:
        return self.__getItems(Reply)

    @property
    def music(self) -> List[Music]:
        return self.__getItems(Music)

    @property
    def text(self) -> List[Text]:
        return self.__getItems(Text)

    @property
    def pure_text(self) -> str:
        result = ""

        # 这里不+空格，因为从event解析，基本不存在连续的Text Segment
        for segment in self.text:
            result += segment.content

        return result

    def any(self, *parts: str):
        for part in parts:
            if part in self.pure_text:
                return True
        return False

    def regex(self, part: str):
        if re.search(part, self.pure_text):
            return True
        return False

    def regex_any(self, *parts: str):
        for part in parts:
            if re.search(part, self.pure_text):
                return True
        return False

    def all(self, *parts: str):
        for part in parts:
            if part not in self.pure_text:
                return False
        return True

    def regex_all(self, *parts: str):
        for part in parts:
            if not re.search(part, self.pure_text):
                return False
        return True

    def startswith(self, string: str):
        return self.pure_text.startswith(string)

    def endswith(self, string: str):
        return self.pure_text.endswith(string)

    async def onebot_reply(self, *segments: T_SegmentInstance):
        from pepperbot.adapters.onebot.api import OnebotV11API

        if self.mode == "group":
            api = OnebotV11API.group_message
        else:
            api = OnebotV11API.private_message

        return await api(
            self.source_id,
            *[Reply(self.onebot_message_id), *segments],
        )

    async def onebot_withdraw(
        self,
    ):
        """仅群聊中有效，需要管理员权限"""

        from pepperbot.adapters.onebot.api import OnebotV11API

        return await OnebotV11API.withdraw_message(self.onebot_message_id)

    def __getitem__(self, index: int) -> T_SegmentInstance:
        return self.segments[index]

    def __contains__(self, item: Union[str, T_SegmentClassOrInstance]):
        if isinstance(item, str):
            if item in self.pure_text:
                return True

        else:
            for segment in self.segments:
                if self.__equal(segment, item):
                    return True

        return False

    def __eq__(self, other: "MessageChain") -> bool:
        if not isinstance(other, MessageChain):
            return False

        return self.id == other.id

    def __len__(self):
        return len(self.segments)

    def only(self, _type: T_SegmentClassOrInstance) -> bool:
        for segment in self.segments:
            if not self.__equal(segment, _type):
                return False

        return True

    def only_one(self, _type: T_SegmentClassOrInstance) -> bool:
        if len(self.segments) != 1:
            return False

        return self.__equal(self.segments[0], _type)
