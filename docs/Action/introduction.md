::: danger
行为链尚未实现，这里只是展示行为链可能的样子
:::

```py
async def do_something():
    await actionBot.selectGroup(1111).new_notice(
        title="",
        body=""
    ).run()

    await (
        actionBot
        .selectGroups(1111, 2222, 3333, 4444)
        .send_message(Text("一条跨群消息"))
        .sleep(5)
        .send_message(Face(100))
        .run()
    )

    # ? 异常情况
    # 如果机器人不在该群中，会报错，可以try except
    await (
        actionBot
        .selectGroup(1111)
        .catch()
        .send_message(Text("一条跨群消息"))
        .run()
    )

    # ? catchHandler的声明
    # 函数是一等对象的概念
    # 为什么不建议使用匿名函数？
    # 不易理解，没有类型提示，不可复用

    # 根据catch标记进行分割片段，捕获每一个片段
    # 比较长的行为链+catch的try except等价实现
    await (
        actionBot
        .selectGroups(1111, 2222, 3333, 4444)
        .send_message(Text("4个群"))
        .exclude(111)  # 删除不存在的群，不会报错
        .send_message(Text("3个群"))
        .catch(catchHandler)
        .exclude(222)
        .send_message(Text("2个群"))
        .exclude(333)
        .send_message(Text("1个群"))
        .run()
    )

    # ? 复杂选择操作
    await (
        actionBot
        .selectGroups(1111, 2222, 3333, 4444)
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

    # ? 复用选择结果
    交流群 = actionBot.selectGroup(1111)

    # ? 唯一性数据，直接返回
    交流群.admins()
    交流群.info()

    # ? 凡是要返回可迭代数据的，全都是异步生成器
    交流群.files()

    async for member in 交流群.members():
        nickname = member.nickname

        if re.search("(网课)|(代刷)|(工作室)|(接单)", nickname):
            await member.kickout()

    async for file in 交流群.files():
        print(file.name)

    # ? 不要耦合发送操作(send_message)和获取操作(members)
    #! 不要这样做，错误示例
    # todo 调用members等非run end point时，也在内部执行一次run执行的方法，以适配这种情况
    getMembersAfterSendMessage = (
        actionBot
        .selectGroup(1111)
        .send_message(Text("一条跨群消息"))
        .members()
    )

    async for member in getMembersAfterSendMessage:
        print(member.nickname)

    # 分两次，代码更易读，最佳实践
    # 可以复用选择结果
    targetGroup = actionBot.selectGroup(1111)

    # 一个action发送消息
    await targetGroup.send_message(Text("一条跨群消息")).run()

    # 一个action获取群员
    getMembersIndependently = targetGroup.members()

    async for member in getMembersIndependently:
        print(member.nickname)

    # ? 对每个群执行同样的操作，通过each或者async_each
    await (
        actionBot
        .selectGroups(1111, 2222, 3333, 4444)
        .catch(catchHandler)
        .each(eachGroup)
        .async_each(eachGroup)
        .run()
    )

    # ? members，info，files等获取方法上，并没有run方法
    # 这些获取方法和run方法一样，都是行为链的end point
    (
        actionBot
        .selectGroup(1111)
        .members()
        # .run() #! members是end point，无法再调用run方法
    )

    # ? action分支选择
    targetUser = actionBot.selectUser(1111)

    action1 = targetUser.send_message(Text("11"))
    action2 = targetUser.send_message(Face(100))

    finalAction = None

    if "condition1":
        finalAction = action1
    else:
        finalAction = action2

    finalAction.run()

    # ? 批量运行action

    # 可以手动运行
    await targetUser.send_message(Text("11")).run()
    await targetUser.send_message(Face(100)).run()

    # 也可以使用工具函数
    action1 = targetUser.send_message(Text("11"))
    action2 = targetUser.send_message(Face(100))

    # 只能接受runnable的action，即不能是members，info等为终点的行为链
    results = await ActionRunner.in_turn(action1, action2)
    results = await ActionRunner.all(action1, action2)
    results = await ActionRunner.all_settled(action1, action2)


if __name__ == "__main__":
    asyncio.run(do_something())

```