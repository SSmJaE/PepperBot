import re
import time
from typing import Callable, Dict, List

from pepperbot.action.chain import globalApi
from pepperbot.globals import CommandContext, UserMessage, globalContext
from pepperbot.message.chain import MessageChain
from pepperbot.message.segment import At


def util_factory(
    commandContext: CommandContext,
    commandClass: Callable,
    groupId,
    userId,
):
    def update_command_status(status: str = "initial"):
        if commandContext.mode == "normal":
            globalContext.cache[commandClass].normalContextMap[userId][
                groupId
            ].commandStatus = status
        elif commandContext.mode == "crossGroup":
            globalContext.cache[commandClass].crossGroupCommandStatus[
                userId
            ].commandStatus = status
        elif commandContext.mode == "crossUser":
            globalContext.cache[commandClass].crossUserCommandStatus[
                groupId
            ].commandStatus = status
        elif commandContext.mode == "global":
            globalContext.cache[commandClass].globalCommandStatus = status

    def process_messageQueue(
        messageQueue: List[UserMessage],
        receive: Dict,
        chain: MessageChain,
    ):
        if len(messageQueue) >= commandContext.maxSize:
            messageQueue.pop(0)

        newMessage = UserMessage(
            messageId=receive["message_id"],
            # todo unix
            createTime=round(time.time()),
            message=[*chain.chain],
            groupId=groupId,
            userId=userId,
        )
        messageQueue.append(newMessage)

    return update_command_status, process_messageQueue


async def is_valid_request(
    chain: MessageChain, commandClassName: str, kwargs: Dict
) -> bool:
    """
    通过commandClass的kwargs和messageChain的pure_text，判断是否触发命令的initial
    """

    # todo kwargs pydantic化
    isValidRequest = False

    # 是否需要@机器人

    atFlag = False
    at: bool = kwargs["at"]
    if at:
        selfId = (await globalApi.self_info()).user_id

        if chain.has(At(selfId)):
            atFlag = True

    needPrefix: bool = kwargs["needPrefix"]
    prefixes: List[str] = kwargs["prefix"]

    also: List[str] = kwargs["also"]
    includeClassName: bool = kwargs["includeClassName"]
    if includeClassName:
        if commandClassName not in also:
            also.append(commandClassName)

    # debug(commandClassName)
    # debug(prefixes)
    # debug(also)

    keywordFlag = False
    for alias in also:
        if isValidRequest:
            break

        for prefix in prefixes if needPrefix else [""]:
            finalPrefix = prefix + alias
            if re.search(f"^{finalPrefix}", chain.pure_text):
                keywordFlag = True
                # debug(finalPrefix)
                break

    # debug(keywordFlag, atFlag)
    if keywordFlag:
        if at:
            if atFlag:
                isValidRequest = True
        else:
            isValidRequest = True

    # debug(isValidRequest)

    return isValidRequest
