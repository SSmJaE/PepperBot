from typing import Any, cast

import ormar

from pepperbot.store.orm import database, metadata


class GPTInfo(ormar.Model):
    class Meta:
        tablename = "gpt_info"
        database = database
        metadata = metadata

    id: int = cast(int, ormar.Integer(primary_key=True))
    account: str = cast(str, ormar.String(max_length=20))
    count: int = cast(int, ormar.Integer(default=0))
    # history: list[dict] = ormar.JSON(default=[])
