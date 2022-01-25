from typing import Callable


def is_valid_class_handler(handler: object):
    return True


def is_valid_class_command(command: object):
    return True


def is_valid_route_validator(validator: Callable):
    """ 参数检查 """
    
    validator.__annotations__

    return True



def is_valid_event_handler(class_handler: object, method: Callable, method_name: str):
    # for method in get_own_methods(handlerClass):
    if is_valid_group_method(method.__name__):
        # before和after钩子的参数和正常响应相同
        # handlerName: str = re.sub(r"^before_", "", method.__name__)
        # handlerName = re.sub(r"^after_", "", method.__name__)
        handlerName = cast(GROUP_EVENTS_T, handlerName)

    kwargList: List[HandlerKwarg] = HANDLER_KWARGS_MAP.get(handlerName, DEFAULT_KWARGS)
    kwargList.append(
        HandlerKwarg(
            name="event",
            type=Union[dict, Dict, Dict[str, Any]],
            value=None,
        )
    )

    kwargNameTypeMap = {}
    for kwarg in kwargList:
        kwargNameTypeMap[kwarg.name] = kwarg.type

    kwargNames = kwargNameTypeMap.keys()

    # debug(method.__name__)
    [args, varargs, varkw] = inspect.getargs(method.__code__)

    usableKwargsHint = "\n可用的参数及类型有"
    kwargsLength = len(kwargNameTypeMap)
    for index, (kwargName, kwargType) in enumerate(kwargNameTypeMap.items(), start=1):
        usableKwargsHint += f"{kwargName}: {kwargType}"

        if index != kwargsLength:
            usableKwargsHint += ", "

    for argName in args[1:]:
        if argName not in kwargNames:
            raise EventHandlerDefineError(
                f"{inspect.getsourcefile(handlerClass)}中的类响应器{handlerClass.__name__}的"
                f"{method.__name__}事件不存在参数{argName}" + usableKwargsHint
            )

        if argName not in method.__annotations__.keys():
            raise EventHandlerDefineError(
                f"{inspect.getsourcefile(handlerClass)}中的类响应器{handlerClass.__name__}的"
                f"{method.__name__}事件的参数{argName}未提供类型注解，其类型为{kwargNameTypeMap[argName]}"
                + usableKwargsHint
            )

    if varargs or varkw:
        raise EventHandlerDefineError(
            f"{inspect.getsourcefile(handlerClass)}中的类响应器{handlerClass.__name__}的"
            f"{method.__name__}事件不需要提供*或者**参数，PepperBot会自动根据声明的参数以及类型注入"
            + usableKwargsHint
        )

    # debug(method.__annotations__)

    for argName, argType in method.__annotations__.items():
        if argName not in kwargNames:
            raise EventHandlerDefineError(
                f"{inspect.getsourcefile(handlerClass)}中的类响应器{handlerClass.__name__}的"
                f"{method.__name__}事件不存在参数{argName}" + usableKwargsHint
            )

        kwargType = kwargNameTypeMap[argName]

        wrongTypeFlag = True
        if get_origin(kwargType) is Union:
            for _type in get_args(kwargType):
                if _type == argType:
                    wrongTypeFlag = False

        if kwargType == argType:
            wrongTypeFlag = False

        if wrongTypeFlag:
            raise EventHandlerDefineError(
                f"{inspect.getsourcefile(handlerClass)}中的类响应器{handlerClass.__name__}的\n"
                + f"{method.__name__}事件的参数{argName}的类型应该为{kwargType}，而不是{argType}"
            )
