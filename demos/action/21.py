from pepperbot.Action.main import ActionChain


# defaultCatchHandler
def catchHandler(exception: CatchException, results: Any):
    pass


async def test():
    actionBot = ActionChain()

    # ? 复杂选择操作
    await (
        actionBot.select_groups(1111, 2222, 3333, 4444)
        .send_message(Text("4个群"))
        .exclude(1111)  # 删除不存在的群，不会报错
        .send_message(Text("3个群"))
        .clear()
        .send_message(Text("0个群，此时会报错，被catch拦截"))
        .catch(catchHandler)
        .include(5555)
        .send_message(Text("1个群"))
        .include(6666)
        .send_message(Text("2个群"))
        .run()
    )
