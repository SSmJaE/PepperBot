---
title: 直接操作 Sanic
---


```py
from pepperbot import sanic_app
```

绑定listener，add_task之类，需要在__name__ == '__main__'之前

这是因为，多进程的问题
