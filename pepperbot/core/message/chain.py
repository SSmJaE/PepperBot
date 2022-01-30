from pprint import pprint
from random import random
import re
from typing import TYPE_CHECKING, Dict, List, Tuple, Union
from pepperbot.adapters.onebot.message.segment import (
    OnebotFace,
    OnebotShare,
)
from pepperbot.core.message.base import BaseMessageSegment
from devtools import debug
# if TYPE_CHECKING:
from pepperbot.core.message.segment import (
    At,
    Audio,
    Image,
    Music,
    Reply,
    T_SegmentClass,
    T_SegmentClassOrInstance,
    T_SegmentInstance,
    Text,
)


from pepperbot.exceptions import EventHandleError
from pepperbot.types import T_BotProtocol, T_RouteMode


ONEBOT_SEGMENT_MAPPING: Dict[str, T_SegmentClass] = {
    "face": OnebotFace,
    "share": OnebotShare,
    "text": Text,
    "image": Image,
}


def construct_chain(
    protocol: T_BotProtocol, mode: T_RouteMode, raw_event: Dict
) -> List[T_SegmentInstance]:

    result: List[T_SegmentInstance] = []

    if protocol == "onebot":
        raw_chain: List[dict] = raw_event.get("message", list)
        for segment in raw_chain:
            segment_type: str = segment["type"]

            segment_class = ONEBOT_SEGMENT_MAPPING.get(segment_type)
            if not segment_class:
                raise EventHandleError(f"无法识别的onebot消息类型 {segment_type}")

            segment_instance = segment_class(segment)
            result.append(segment_instance)

    elif protocol == "keaimao":
        pass

    else:
        raise EventHandleError(f"尚未支持 {protocol} 的消息链构造")

    # debug(result)
    return result


class MessageChain:
    __slots__ = (
        "id",
        "chain",
        "raw_event",
        "source_id",
        "protocol",
        "mode",
        "onebot_message_id",
    )

    onebot_message_id: str

    def __init__(
        self,
        protocol: T_BotProtocol,
        mode: T_RouteMode,
        raw_event: Dict,
        source_id: str,
    ) -> None:
        """
        [summary]

        Args:
            event: [description]
            source_id: 当mode为group时，source_id就是group_id，mode为private时同理
            protocol: [description]
            mode: [description]

        """
        # debug(locals())

        self.id = random()
        self.chain: List[T_SegmentInstance] = []

        self.raw_event = raw_event
        self.source_id = source_id
        self.protocol = protocol
        self.mode = mode

        self.chain = construct_chain(protocol, mode, raw_event)

        self.onebot_message_id = raw_event.get("message_id", "")

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
        for segment in self.chain:
            if self.__equal(segment, other):
                return True

        return False

    def has_and_first(
        self, other: T_SegmentClassOrInstance
    ) -> Tuple[bool, T_SegmentInstance]:
        for segment in self.chain:
            if self.__equal(segment, other):
                return True, segment

        # 返回Text只是为了提供更好的类型注解，因为python并不能自动判断union类型的分支情况
        # 即 True => type1 , False => type2
        # generic可以，不过还是直接Text("")最简单
        return False, Text("")

    def has_and_last(self, other: T_SegmentClassOrInstance):
        for segment in reversed(self.chain):
            if self.__equal(segment, other):
                return True, segment

        return False, Text("")

    def has_and_all(self, other: T_SegmentClassOrInstance):
        results = []

        for segment in self.chain:
            if self.__equal(segment, other):
                results.append(segment)

        if len(results):
            return True, results
        return False, Text("")

    def __getItems(self, type_: T_SegmentClass):
        results = []

        for segment in self.chain:
            if isinstance(segment, type_):
                results.append(segment)

        return results

    @property
    def at(self):
        return self.__getItems(At)

    @property
    def onebot_faces(self):
        return self.__getItems(OnebotFace)

    @property
    def audio(self):
        return self.__getItems(Audio)

    @property
    def images(self):
        return self.__getItems(Image)

    @property
    def replies(self):
        return self.__getItems(Reply)

    @property
    def music(self):
        return self.__getItems(Music)

    @property
    def text(
        self,
    ) -> List[Text]:
        return self.__getItems(Text)

    @property
    def pure_text(self) -> str:
        if self.protocol == "onebot":

            result = ""

            for segment in self.text:
                result += segment.onebot["data"]["text"]

            return result

        elif self.protocol == "keaimao":
            return self.text[0].keaimao

        else:
            raise EventHandleError(f"")

    def any(self, *parts):
        for part in parts:
            if part in self.pure_text:
                return True
        return False

    def regex(self, part):
        if re.search(part, self.pure_text):
            return True
        return False

    def regex_any(self, *parts):
        for part in parts:
            if re.search(part, self.pure_text):
                return True
        return False

    def all(self, *parts):
        for part in parts:
            if part not in self.pure_text:
                return False
        return True

    def regex_all(self, *parts):
        for part in parts:
            if not re.search(part, self.pure_text):
                return False
        return True

    def startswith(self, string: str):
        return self.pure_text.startswith(string)

    def endswith(self, string: str):
        return self.pure_text.endswith(string)

    async def onebot_reply(self, *segments: T_SegmentInstance):
        from pepperbot.adapters.onebot.api import OnebotV11Api

        if self.mode == "group":
            api = OnebotV11Api.group_message
        else:
            api = OnebotV11Api.private_message

        return await api(
            self.source_id,
            *(segment.onebot for segment in [Reply(self.onebot_message_id), *segments]),
        )

    async def onebot_withdraw(
        self,
    ):
        # await self.api(
        #     "delete_msg",
        #     **{
        #         "message_id": self.messageId,
        #     },
        # )
        pass

    def __getitem__(self, index: int) -> T_SegmentInstance:
        return self.chain[index]

    def __contains__(self, item: Union[str, T_SegmentClassOrInstance]):
        if isinstance(item, str):
            if item in self.pure_text:
                return True

        else:
            for segment in self.chain:
                if self.__equal(segment, item):
                    return True

        return False

    def __eq__(self, other: "MessageChain") -> bool:
        if not isinstance(other, MessageChain):
            return False

        return self.id == other.id

    def __len__(self):
        return len(self.chain)

    def only(self, _type: T_SegmentClassOrInstance) -> bool:
        for segment in self.chain:
            if not self.__equal(segment, _type):
                return False

        return True

    def only_one(self, _type: T_SegmentClassOrInstance) -> bool:
        if len(self.chain) != 1:
            return False

        return self.__equal(self.chain[0], _type)
