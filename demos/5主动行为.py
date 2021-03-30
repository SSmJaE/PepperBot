

from typing import Iterable


def create_bot(*args, **kwargs):
    bot = {}

    return object  # type:Any


actionBot = create_bot()


class ActionChain:
    pass


actionChain = (
    actionBot
    .selectGroup(1111, 2222, 3333, 4444)
    .sendMessage(Text("一条跨群消息"))
    .sleep(5)
    .sendMessage(Face(100))
    .run()
)

(
    actionBot
    .selectGroup(1111, 2222, 3333, 4444)
    .sendMessage(Text("4个群"))
    .exclude(111)
    .sendMessage(Text("3个群"))
    .exclude(222)
    .sendMessage(Text("2个群"))
    .exclude(333)
    .sendMessage(Text("1个群"))
    .run()
)

defaultCatchHandler


def catchHandler(exception: CatchException, results: Any):
    pass


async def eachGroup(group: ActionGroup):
    pass

# 如果机器人不在该群中，会报错，可以try except
# 适配指定多个群和单个群的情况
withTargetGroup = await (
    actionBot
    .selectGroup(1111, 2222, 3333, 4444)
    .catch(catchHandler)
    .each(eachGroup)
    .asyncEach()
    .run()
)
# 根据catch标记进行分割片段，捕获每一个片段
# 比较长的行为链+catch的try except等价实现


withTargetUser = actionBot.selectUser(1111, 2222, 3333, 4444)


def sendCrossOriginMessage(chain: ActionChain):
    chain.run()


def multiActionChain(*chains: Iterable[ActionChain]):
    for chain in chains:
        yield chain


# 常用操作，对asyncio库的gather进行封装，降低与PepperBot的整合成本
ActionRunner.all() timeout
asyncio.gather(*chains)
ActionRunner.all_settled() timeout

actionChain.run()

for chain in multiActionChain():
    chain.run()

# 凡是要返回可迭代数据的，全都是生成器
members = await (
    actionBot
    .selectGroup(1111)
    .members()
    .run()
)
交流群 = actionBot.selectGroup(1111)
files = 交流群.files()
交流群.admins()
交流群.info()


actionBot.selectGroup(1111).newNotice(
    title="",
    body=""
)

for member in 交流群.members():
    nickname = member.nickname

    if re.search("(网课)|(代刷)|(工作室)|(接单)", nickname):
        member.kickout()
