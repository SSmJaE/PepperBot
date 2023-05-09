---
title: 数据库
---


`PepperBot`选择通过数据库，来实现进程间的数据共享

orm为`ormar`，基于`sqlalchemy` + `pydantic`的异步orm，支持`sqlite`、`mysql`、`postgresql`等数据库

这里只是简单涉及了一些`ormar`的用法，具体用法见[`ormar`的文档](https://collerek.github.io/ormar/)

默认使用`sqlite`，可以通过`.env`修改数据库配置

## 开发者可用的表

`PepperBot`提供了一个键值对形式的`Share`表，便于开发者存储一些结构比较简单的数据

语法类似`JavaScript`的`localStorage`

可以存储任意可JSON序列化的数据

```python
from pepperbot.store.orm import get_value, set_value, delete_value

await get_value('key') # 如果不存在，会返回None
await get_value('key', default='default')

await set_value('key', 'value')
await set_value('key', [1, 2, 3])
await set_value('key', {'a': 1, 'b': 2})
await set_value('key', True)

await delete_value('key')
```

### 实现自己的表

开发者只需要定义好模型即可，`PepperBot`会负责创建表等操作(只要设置了`Meta`的`database`和`metadata`)

这是一个简单的例子

`ormar`的类型，在`vscode`下，有点小问题，如果不想看到报错，可以手动`cast`或者`type: ignore`

```python
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

```

## 使用建议

### 数据库迁移

`ormar`基于`sqlalchemy`，所以我们使用`alembic`来进行数据库迁移

### 在多worker中同步数据的示例

## 框架本身使用的表
