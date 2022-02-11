from typing import Dict, Optional, Union, overload
from pepperbot.core.message.base import BaseMessageSegment
from pepperbot.utils.common import DictNoNone


class OnebotFace(BaseMessageSegment):
    universal = ("onebot",)

    @overload
    def __init__(self, id: int):
        ...

    @overload
    def __init__(self, id: Dict):
        ...

    def __init__(self, id: Union[dict, int]):

        data = id

        if isinstance(data, dict):
            identifier = data["data"]["id"]

            for key, value in data.items():
                setattr(self, key, value)

            self.onebot = {**data}

        else:
            identifier = data

            self.id = data
            self.onebot = {"type": "face", "data": {"id": id}}

        super().__init__(**{"identifier": identifier})


class OnebotShare(BaseMessageSegment):
    universal = ("onebot",)

    @overload
    def __init__(
        self,
        url: str,
        title: str,
        content: Optional[str] = None,
        imageUrl: Optional[str] = None,
    ):
        ...

    @overload
    def __init__(self, url: Dict):
        ...

    def __init__(
        self,
        url: Union[Dict, str],
        title: str = "",
        content: Optional[str] = None,
        imageUrl: Optional[str] = None,
    ):

        data = url

        if isinstance(data, dict):
            identifier = data["data"]["url"]

            for key, value in data.items():
                setattr(self, key, value)

            self.formatted = {**data}
        else:
            identifier = data

            kwargs = DictNoNone()
            kwargs["title"] = title
            kwargs["content"] = content
            kwargs["image"] = imageUrl

            self.formatted = {"type": "share", "data": {**kwargs, "file": url}}

        super().__init__(**{"identifier": identifier})
