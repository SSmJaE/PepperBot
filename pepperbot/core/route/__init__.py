from inspect import isclass
from typing import Callable, Dict, Iterable, Literal, Optional, Type, Union

from pepperbot.exceptions import InitializationError
from pepperbot.store.meta import (
    BotRoute,
    T_RouteRelation,
    register_routes,
)


# 消息响应器的调用顺序，和加入route的顺序是一致的


# validator
# 123 in api.admins


def register(
    *,
    commands: Iterable[object] = None,
    groups: T_RouteRelation = "*",
    friends: T_RouteRelation = "*",
    # **kwargs,
):
    def decorator(handler: Callable):

        if not isclass(handler):
            raise InitializationError("register装饰器只能注册class，不能注册function")

        # 收集register中的BotRoute，apply_routes中应用
        register_routes.append(
            BotRoute(
                handler=handler,
                commands=commands,
                groups=groups,
                friends=friends,
            )
        )

        return handler

    return decorator
