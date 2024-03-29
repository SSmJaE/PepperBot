---
title: 定时任务
---

PepperBot 集成了`apscheduler`，可以非常轻松的实现异步定时任务(同步任务也可以)

当然，你也可以直接通过`Sanic`的`add_task`来实现定时任务

其实定时任务和一次性任务很相似，区别在于

- 如果直接通过 `asyncio.run()`运行任务，那么就只会执行一次，也就是一次性任务
- 如果通过 `bot.run()`，并且将任务注册到了 `async_scheduler` 中，那么他就是会多次执行的定时任务了

```py
from pepperbot import async_scheduler

async def task():
    print("Hello World")

async_scheduler.add_job(task, "interval", seconds=5)
```

`async_scheduler`其实就是一个实例化的，`apscheduler` 的 `AsyncScheduler`，所以具体参数见 `apscheduler` 的[文档]即可

具体例子[见此](../../examples/定时任务)
