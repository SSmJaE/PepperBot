from typing import Any, Type

import databases
import ormar
import sqlalchemy

from pepperbot.config import global_config

database = databases.Database(global_config.database.url)
metadata = sqlalchemy.MetaData()
engine = sqlalchemy.create_engine(global_config.database.url)


class Share(ormar.Model):
    """专门给开发者使用的、键值对形式的存储表，用于跨进程的数据共享"""

    class Meta:
        tablename = "share"
        database = database
        metadata = metadata

    key: str = ormar.String(primary_key=True, max_length=100)  # type: ignore
    value: Any = ormar.JSON(default=None)


class Metadata(ormar.Model):
    """框架本身使用的、键值对形式的存储表，用于跨进程的数据共享

    替代直接使用全局变量，因为要考虑到多进程的情况
    """

    class Meta:
        tablename = "metadata"
        database = database
        metadata = metadata

    key: str = ormar.String(primary_key=True, max_length=100)  # type: ignore
    value: Any = ormar.JSON(default=None)


async def get_value_from(
    model: Type[ormar.Model], key: str, default: Any = None
) -> Any:
    """获取键值对形式的数据"""

    column, created = await model.objects.get_or_create(
        key=key,
        _defaults=dict(value=default),
    )

    return column.value if column.value is not None else default


async def get_metadata(key: str, default: Any = None) -> Any:
    """获取键值对形式的数据"""

    return await get_value_from(Metadata, key, default)


async def get_value(key: str, default: Any = None) -> Any:
    """获取键值对形式的数据"""

    return await get_value_from(Share, key, default)


async def set_value_from(model: Type[ormar.Model], key: str, value: Any) -> None:
    """设置键值对形式的数据"""

    # update_or_create并不能自动create
    try:
        column = await model.objects.get(key=key)
        await column.update(value=value)

    except ormar.NoMatch:
        await model.objects.create(key=key, value=value)


async def set_metadata(key: str, value: Any) -> None:
    """设置键值对形式的数据"""

    await set_value_from(Metadata, key, value)


async def set_value(key: str, value: Any) -> None:
    """设置键值对形式的数据"""

    await set_value_from(Share, key, value)


async def delete_value_from(model: Type[ormar.Model], key: str) -> None:
    """删除键值对形式的数据"""

    try:
        column = await model.objects.get(key=key)
        await column.delete()

    except ormar.NoMatch:
        pass


async def delete_metadata(key: str) -> None:
    """删除键值对形式的数据"""

    await delete_value_from(Metadata, key)


async def delete_value(key: str) -> None:
    """删除键值对形式的数据"""

    await delete_value_from(Share, key)
