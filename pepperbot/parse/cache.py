import inspect
import random
import re
from typing import Set, cast, get_args, get_origin

from devtools import debug
from pepperbot.exceptions import EventHandlerDefineError
from pepperbot.globals import *
from pepperbot.parse import GROUP_EVENTS, GROUP_EVENTS_T, is_valid_group_method
from pepperbot.parse.bots import *
from pepperbot.parse.kwargs import (
    DEFAULT_KWARGS,
    HANDLER_KWARGS_MAP,
    HandlerKwarg,
    construct_GroupCommonBot,
)
from pepperbot.utils.common import get_own_methods


def cache():
    # groupHandler可能有多个装饰器，比如register, withCommand
    # 先解析为与装饰器名称相关的缓存至groupMeta，
    # 解析完所有装饰器之后，再生成classHandlers.groupCache中的缓存
    # 生成缓存时，确保register的存在，不然报错(withCommand也可以向group中推送meta信息)
    # 这才是真正的meta，全局保存class和对应的meta，而不是绑定到class上，可能会涉及到bound和unbound的问题
    _cache = classHandlers.groupCache

    # 多个group handler，相同command的处理(解析所有指令和groupId，重新生成缓存)
    uniqueCommandClasses: Set[Callable] = set()

    for handlerClass, classMeta in classHandlers.groupMeta.items():

        # 检查事件响应的参数
        for method in get_own_methods(handlerClass):
            if is_valid_group_method(method.__name__):
                # before和after钩子的参数和正常响应相同
                handlerName: str = re.sub(r"^before_", "", method.__name__)
                handlerName = re.sub(r"^after_", "", method.__name__)
                handlerName = cast(GROUP_EVENTS_T, handlerName)

                kwargList: List[HandlerKwarg] = HANDLER_KWARGS_MAP.get(
                    handlerName, DEFAULT_KWARGS
                )
                kwargList.append(
                    HandlerKwarg(
                        name="event", type=Union[dict, Dict, Dict[str, Any]], value=None
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
                for index, (kwargName, kwargType) in enumerate(
                    kwargNameTypeMap.items(), start=1
                ):
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

        #  不要每次都创建实例，on/register监听器新增时建立一次保存起来即可
        _instance = handlerClass()

        decoratorNames = list(classMeta.decorators.keys())
        if "register" not in decoratorNames:
            raise Exception("基于class的事件响应处理器必须通过register装饰器注册")

        currentCommandClasses: List[Callable] = []

        # 除register以外的class级装饰器
        decoratorNames.remove("register")

        for decoratorName in decoratorNames:
            argDict = classMeta.decorators[decoratorName]
            args = argDict.args
            kwargs = argDict.kwargs

            if decoratorName == "with_command":
                commandClasses: List[Callable] = kwargs["commandClasses"]

                currentCommandClasses = [*commandClasses]

                for commandClass in commandClasses:
                    uniqueCommandClasses.add(commandClass)

            # elif decoratorName == ""

        # 处理完所有其它装饰器后，最后处理register，建立groupId与classHandler的映射
        finalGroupIds: List[int] = []

        groupId = classMeta.decorators["register"].kwargs["groupId"]

        if isinstance(groupId, int):
            finalGroupIds.append(groupId)

        elif isinstance(groupId, str):
            finalGroupIds.append(int(groupId))

        elif isinstance(groupId, list):
            for id in groupId:
                finalGroupIds.append(int(id))

        for id in finalGroupIds:

            # 是否可以只实例化一次botInstance？动态注入groupId
            # 似乎每个群一个bot，效果更好一点
            groupCache = GroupCache(
                instance=_instance,
                # 为每一个group，缓存一个GroupCommonBot
                botInstance=construct_GroupCommonBot({"group_id": id}, cast(Any, None)),
                commandClasses=currentCommandClasses,
            )

            # 初始化时，遍历生成缓存，不要每次接收到消息都去遍历
            for method in get_own_methods(_instance):
                if is_valid_group_method(method.__name__):
                    groupCache.methods[method.__name__].append(method)

                else:
                    print("无效的hook")
                    debug(method)

            _cache[id].append(groupCache)

    # 在提取所有可能的with_command装饰器之后执行
    # 同一个commandClass，就实例化一次
    for commandClass in uniqueCommandClasses:

        commandInstance = commandClass()

        commandKwargs: Dict = getattr(commandClass, "kwargs")
        # debug(commandKwargs)

        commandBuffer = CommandCache(instance=commandInstance, kwargs=commandKwargs)

        for method in get_own_methods(commandInstance):
            commandBuffer.methods[method.__name__] = method

        classHandlers.commandCache[commandClass] = commandBuffer

        maxSize = commandKwargs["maxSize"]
        timeout = commandKwargs["timeout"]
        mode = commandKwargs["mode"]

        commandContext = CommandContext(
            maxSize=maxSize or globalContext.maxSize,
            timeout=timeout or globalContext.timeout,
            mode=mode,
        )

        globalContext.cache[commandClass] = commandContext
