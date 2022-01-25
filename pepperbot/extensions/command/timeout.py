async def __check_command_timeout():
    # todo 超时判断应该每次心跳都判断，而不是接收到该用户消息时
    # 超时判断，与上一条消息的createTime判断
    # timeout: Optional[int] = commandCache.kwargs[
    #     "timeout"
    # ]

    # if timeout:

    #     prevChain = finalMessageQueue[-2]
    #     currentChain = finalMessageQueue[-1]

    #     debug(
    #         prevChain.createTime
    #         - currentChain.createTime
    #     )
    #     debug(timeout)

    #     if (
    #         prevChain.createTime
    #         - currentChain.createTime
    #         >= timeout
    #     ):
    #         raise CommandClassOnTimeout()
    pass