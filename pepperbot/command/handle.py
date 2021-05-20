import re
from inspect import isawaitable
from typing import Any, Dict, List, Optional, cast

from devtools import debug
from pepperbot.command.parse import is_valid_request, util_factory
from pepperbot.exceptions import (
    CommandClassDefineException,
    CommandClassOnExit,
    CommandClassOnFinish,
    CommandClassOnTimeout,
)
from pepperbot.globals import (
    classHandlers,
    GroupCache,
    NormalContext,
    UserMessage,
    globalContext,
)
from pepperbot.message.chain import MessageChain
from pepperbot.parse.kwargs import construct_chain, construct_sender
from pepperbot.utils.common import await_or_normal, fit_kwargs


async def handle_command(
    receive: Dict[str, Any],
    kwargs: Dict[str, Any],
    groupId: int,
    groupHandler: GroupCache,
):

    # todo 命令的优先级，
    # 命令需要优先级吗？
    # 普通的group_message也有默认优先级，所以命令可以先于group_message执行，也可以后于

    chain = construct_chain(receive, groupId=groupId)
    sender = construct_sender(receive)

    for commandClass, commandCache in classHandlers.commandCache.items():

        if not commandClass in groupHandler.commandClasses:
            return

        commandContext = globalContext.cache[commandClass]
        commandClassName = commandClass.__name__

        userId = cast(int, sender.user_id)
        chain = cast(MessageChain, chain)

        (update_command_status, process_messageQueue,) = util_factory(
            commandContext,
            commandClass,
            groupId,
            userId,
        )

        # 每一个用户一个指向，可以设置跨群还是不跨群
        # 跨群就是使用一个指向，
        # 不跨群，就是同一个用户，在不同群，有不同的指向
        finalMessageQueue: List[UserMessage] = []
        finalStatus: str = ""
        finalContext: Optional[Dict] = None

        if commandContext.mode == "normal":
            userGroupMap = commandContext.normalContextMap[userId]

            normalContext = userGroupMap.get(groupId)
            if not normalContext:
                normalContext = NormalContext()
                userGroupMap[groupId] = normalContext

            finalContext = normalContext.userContext
            finalStatus = normalContext.commandStatus
            finalMessageQueue = normalContext.messageQueue

        elif commandContext.mode == "crossGroup":
            status = commandContext.crossGroupCommandStatus[userId]

            finalContext = status.userContext
            finalStatus = status.commandStatus
            finalMessageQueue = status.messageQueue

        elif commandContext.mode == "crossUser":
            status = commandContext.crossUserCommandStatus[groupId]

            finalContext = status.userContext
            finalStatus = status.commandStatus
            finalMessageQueue = status.messageQueue

        elif commandContext.mode == "global":

            finalContext = commandContext.globalContext
            finalStatus = commandContext.globalCommandStatus
            finalMessageQueue = commandContext.globalMessageQueue

        debug(
            {
                "className": commandClassName,
                # "userId": userId,
                # "groupId": groupId,
                # "chain": chain.chain,
                # "context": finalContext,
                # "status": finalStatus,
                # "messageQueue": finalMessageQueue,
            }
        )
        # debug(finalStatus)
        # debug(finalMessageQueue)
        # debug(globalContext)

        collectMessageFlag = False
        if finalStatus == "initial":

            # 判断是否触发命令前缀
            isValidRequest = await is_valid_request(
                chain, commandClassName, commandCache.kwargs
            )

            debug(isValidRequest)

            if isValidRequest:
                collectMessageFlag = True
            else:
                continue

        else:
            collectMessageFlag = True

        if collectMessageFlag:
            process_messageQueue(
                finalMessageQueue,
                receive,
                chain,
            )

        # 当前指向的方法，或者说，当前激活的命令回调方法
        targetMethod = commandCache.methods[finalStatus]
        methodNames = commandCache.methods.keys()

        # 判断是否正常退出
        try:
            # todo 对所有事件的回调，都判断是否awaitable

            if finalStatus != "initial":

                # 退出判断
                exitPatterns: List[str] = commandCache.kwargs["exitPattern"]

                debug(exitPatterns)
                for pattern in exitPatterns:
                    debug(re.search(pattern, chain.pure_text))
                    if re.search(pattern, chain.pure_text):
                        raise CommandClassOnExit()

            # 参数和group_message事件参数一致
            result = await await_or_normal(
                targetMethod,
                **fit_kwargs(
                    targetMethod,
                    {
                        **kwargs,
                        "context": finalContext,
                        "messageQueue": finalMessageQueue,
                    },
                ),
            )
            debug(result)

            # 流程正常退出
            if result == True or result == None:
                raise CommandClassOnFinish()
            else:

                if not (callable(result) or isawaitable(result)):
                    raise CommandClassDefineException("未提供命令类中可继续执行的下一个方法")

                if not result.__name__ in methodNames:
                    raise CommandClassDefineException("下一步方法，需要在命令类中定义过，不能是外部函数或方法")

                # 设置下一次执行时要调用的方法
                update_command_status(result.__name__)

        except CommandClassDefineException as e:
            debug(e)

        except CommandClassOnFinish:  # 流程正常退出时执行，return True时

            update_command_status()

            if "finish" in methodNames:
                finishHandler = commandCache.methods["finish"]
                await await_or_normal(
                    finishHandler,
                    **fit_kwargs(
                        targetMethod,
                        {
                            **kwargs,
                            "context": finalContext,
                            "messageQueue": finalMessageQueue,
                        },
                    ),
                )

        except CommandClassOnExit:  # 用户主动退出时执行

            update_command_status()

            if "exit" in methodNames:
                exitHandler = commandCache.methods["exit"]
                await await_or_normal(
                    exitHandler,
                    **fit_kwargs(
                        targetMethod,
                        {
                            **kwargs,
                            "context": finalContext,
                            "messageQueue": finalMessageQueue,
                        },
                    ),
                )

        except CommandClassOnTimeout:  # 用户响应超时时执行

            update_command_status()

            if "timeout" in methodNames:
                timeoutHandler = commandCache.methods["timeout"]
                await await_or_normal(
                    timeoutHandler,
                    **fit_kwargs(
                        targetMethod,
                        {
                            **kwargs,
                            "context": finalContext,
                            "messageQueue": finalMessageQueue,
                        },
                    ),
                )

        except Exception as e:
            update_command_status()

            if "error" in methodNames:  # 用户定义的异常捕获方法
                errorHandler = commandCache.methods["error"]
                await await_or_normal(
                    errorHandler,
                    **fit_kwargs(
                        targetMethod,
                        {
                            **kwargs,
                            "context": finalContext,
                            "messageQueue": finalMessageQueue,
                            "error": e,
                        },
                    ),
                )

            else:
                raise e
