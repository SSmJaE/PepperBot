from abc import ABC
from typing import Any, List, Literal, Union


class MessageSegMentBase:
    def __init__(self, identifier: Any):
        self.identifier = identifier

    def __str__(self) -> str:
        return f"Segment[{self.__class__.__name__}, {self.identifier}]"

    def __repr__(self) -> str:
        return f"Segment[{self.__class__.__name__}, {self.identifier}]"

    def __eq__(self, other: 'MessageSegMentBase') -> bool:
        if type(self) == type(other):
            if self.identifier == other.identifier:
                return True
        return False


class At(MessageSegMentBase):
    def __init__(self, data: Union[dict, int]):

        if isinstance(data, dict):
            userId = data['user_id']

            for key, value in data.items():
                setattr(self, key, value)
        else:
            userId = data

        super().__init__(**{
            "identifier": userId
        })

        self.formatted = {
            "type": "at",
            "data": {
                "qq": userId
            }
        }


class Text(MessageSegMentBase):
    def __init__(self, data: Union[dict, str]):

        if isinstance(data, dict):
            text = data['text']

            for key, value in data.items():
                setattr(self, key, value)
        else:
            text = data

        super().__init__(**{
            "identifier": text
        })

        self.formatted = {
            "type": "text",
            "data": {
                "text": text
            }
        }


class Face(MessageSegMentBase):
    def __init__(self, data: Union[dict, int]):

        if isinstance(data, dict):
            id = data['id']

            for key, value in data.items():
                setattr(self, key, value)
        else:
            id = data

        super().__init__(**{
            "identifier": id
        })

        self.formatted = {
            "type": "face",
            "data": {
                "id": id
            }
        }


class Image(MessageSegMentBase):
    def __init__(self, data: Union[dict, str]):

        if isinstance(data, dict):
            url = data['file']

            for key, value in data.items():
                setattr(self, key, value)
        else:
            url = data

        super().__init__(**{
            "identifier": url
        })

        self.formatted = {
            "type": "image",
            "data": {
                "file": url
            }
        }


class Reply(MessageSegMentBase):
    def __init__(self, data: Union[dict, int]):

        if isinstance(data, dict):
            messageId = data['id']

            for key, value in data.items():
                setattr(self, key, value)
        else:
            messageId = data

        super().__init__(**{
            "identifier": messageId
        })

        self.formatted = {
            "type": "reply",
            "data": {
                "id": f"{messageId}"
            }
        }


class Audio(MessageSegMentBase):
    def __init__(self, data: Union[dict, str]):

        if isinstance(data, dict):
            url = data['file']

            for key, value in data.items():
                setattr(self, key, value)
        else:
            url = data

        super().__init__(**{
            "identifier": url
        })

        self.formatted = {
            "type": "record",
            "data": {
                "file": url
            }
        }


class Music(MessageSegMentBase):
    def __init__(self, data: Union[dict, str], source: Literal['qq', "163", "xm"] = "qq"):

        if isinstance(data, dict):
            id = data['id']
            source = data["type"]

            for key, value in data.items():
                setattr(self, key, value)
        else:
            id = data
            source = source

        super().__init__(**{
            "identifier": id
        })

        self.formatted = {
            "type": "music",
            "data": {
                "type": source,
                "id": id
            }
        }