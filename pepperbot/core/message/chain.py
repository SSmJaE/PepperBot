import re
import sys
from pprint import pprint
from typing import Iterable, Tuple, Type, TypeVar

from devtools import debug
from pepperbot.core.bot.api_caller import ApiCaller

from pepperbot.core.message.segment import *

T_SegmentClass = Union[
    Type[At],
    Type[Music],
    Type[Audio],
    Type[Image],
    Type[Reply],
    Type[Text],
    Type[Face],
    Type[Video],
    Type[Poke],
    Type[Share],
]
T_SegmentInstance = Union[
    At, Text, Face, Music, Audio, Image, Reply, Video, Poke, Share
]
T_SegmentClassOrInstance = Union[T_SegmentClass, T_SegmentInstance]
TypeofSegmentClassOrInstance_Generic = TypeVar(
    "TypeofSegmentClassOrInstance_Generic",
    At,
    Text,
    Face,
    Music,
    Audio,
    Image,
    Reply,
    Type[At],
    Type[Music],
    Type[Audio],
    Type[Image],
    Type[Reply],
    Type[Text],
    Type[Face],
)

currentModule = sys.modules[__name__]


class MessageChain:
    pass
    # def __init__(
    #     self,
    #     event: dict,
    #     source_id: int,
    #     protocol: T_BotProtocol,
    #     mode: T_RouteMode,
    #     api_caller: ApiCaller,
    # ) -> None:
    #     self.chain: List[T_SegmentInstance] = []

    #     self.event = event
    #     self.groupId = groupId
    #     self.api: API_Caller_T = api

    #     self.messageId = event["message_id"]

    #     for key, value in event.items():
    #         setattr(self, key, value)

    #     originChain: Iterable[dict] = event.get("message", list)
    #     for segment in originChain:
    #         messageType: str = segment["type"]
    #         # data: dict = segment["data"]
    #         # pprint(segment)

    #         segmentClass = getattr(currentModule, messageType.capitalize())
    #         segmentInstance = segmentClass(segment)

    #         self.chain.append(segmentInstance)

    #     pprint(self.chain)

    # # def __repr__(self) -> str:
    # #     json.dumps

    # def __equal(self, segment: "MessageSegMentBase", other: T_SegmentClassOrInstance):
    #     # 如果是实例，data是否相等
    #     if isinstance(other, MessageSegMentBase):
    #         if segment == other:
    #             return True

    #     # 是否是同一类型
    #     else:
    #         if type(segment) == other:
    #             return True

    #     return False

    # # todo part in raw operator in
    # # if

    # def has(self, other: T_SegmentClassOrInstance):
    #     for segment in self.chain:
    #         if self.__equal(segment, other):
    #             return True

    #     return False

    # def has_and_first(
    #     self, other: T_SegmentClassOrInstance
    # ) -> Tuple[bool, T_SegmentInstance]:
    #     for segment in self.chain:
    #         if self.__equal(segment, other):
    #             return True, segment

    #     # 返回Text只是为了提供更好的类型注解，因为python并不能自动判断union类型的分支情况
    #     # 即 True => type1 , False => type2
    #     # generic可以，不过还是直接Text("")最简单
    #     return False, Text("")

    # def has_and_last(self, other: T_SegmentClassOrInstance):
    #     for segment in reversed(self.chain):
    #         if self.__equal(segment, other):
    #             return True, segment

    #     return False, Text("")

    # def has_and_all(self, other: T_SegmentClassOrInstance):
    #     results = []

    #     for segment in self.chain:
    #         if self.__equal(segment, other):
    #             results.append(segment)

    #     if len(results):
    #         return True, results
    #     return False, Text("")

    # def __getItems(self, _type: SegmentClass_T):
    #     results = []

    #     for segment in self.chain:
    #         if isinstance(segment, _type):
    #             results.append(segment)

    #     return results

    # @property
    # def at(self):
    #     return self.__getItems(At)

    # @property
    # def faces(self):
    #     return self.__getItems(Face)

    # @property
    # def audio(self):
    #     return self.__getItems(Audio)

    # @property
    # def images(self):
    #     return self.__getItems(Image)

    # @property
    # def replies(self):
    #     return self.__getItems(Reply)

    # @property
    # def music(self):
    #     return self.__getItems(Music)

    # @property
    # def text(
    #     self,
    # ) -> List[Text]:
    #     return self.__getItems(Text)

    # @property
    # def pure_text(self) -> str:
    #     result = ""

    #     for part in self.text:
    #         result += part.formatted["data"]["text"]

    #     return result

    # def any(self, *parts):
    #     for part in parts:
    #         if part in self.pure_text:
    #             return True
    #     return False

    # def regex(self, part):
    #     if re.search(part, self.pure_text):
    #         return True
    #     return False

    # def regex_any(self, *parts):
    #     for part in parts:
    #         if re.search(part, self.pure_text):
    #             return True
    #     return False

    # def all(self, *parts):
    #     for part in parts:
    #         if part not in self.pure_text:
    #             return False
    #     return True

    # def regex_all(self, *parts):
    #     for part in parts:
    #         if not re.search(part, self.pure_text):
    #             return False
    #     return True

    # def startswith(self, string: str):
    #     return self.pure_text.startswith(string)

    # def endswith(self, string: str):
    #     return self.pure_text.endswith(string)

    # async def reply(self, *messageChain: T_SegmentInstance):
    #     await self.api(
    #         "send_group_msg",
    #         **{
    #             "group_id": self.groupId,
    #             "message": [
    #                 segment.formatted
    #                 for segment in [Reply(self.messageId), *messageChain]
    #             ],
    #         }
    #     )

    # async def withdraw(
    #     self,
    # ):
    #     await self.api(
    #         "delete_msg",
    #         **{
    #             "message_id": self.messageId,
    #         }
    #     )

    # def __getitem__(self, index: int) -> Union[T_SegmentInstance]:
    #     return self.chain[index]

    # def __contains__(self, item: Union[str, T_SegmentClassOrInstance]):
    #     if isinstance(item, str):
    #         if item in self.pure_text:
    #             return True

    #     else:
    #         for segment in self.chain:
    #             if self.__equal(segment, item):
    #                 return True

    #     return False

    # def __eq__(self, other: "MessageChain") -> bool:
    #     return self.messageId == other.messageId

    # def __len__(self):
    #     return len(self.chain)

    # def only(self, _type: T_SegmentClassOrInstance) -> bool:
    #     for segment in self.chain:
    #         if not self.__equal(segment, _type):
    #             return False

    #     return True

    # def only_one(self, _type: T_SegmentClassOrInstance) -> bool:
    #     if len(self.chain) != 1:
    #         return False

    #     return self.__equal(self.chain[0], _type)
