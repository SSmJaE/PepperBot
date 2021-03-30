from abc import abstractmethod
import asyncio
import random
from typing import Any, Callable, Coroutine, Generator, Generic, Iterable, List, Sequence, TypeVar, Generic
from pydantic import BaseModel
from functools import wraps

from src.main import *


def create_bot(port=13121):
    bot = {}

    return ActionChain()


actionBot = create_bot(port=13121)

# todo 原生event使用pydantic


class GroupMemberModel(BaseModel):
    user_iq: str
    nickname: str


class GroupMember(GroupMemberModel):
    nickname: str

    async def kickout(self):
        pass


class GroupAdmin(GroupMember):
    pass


class GroupOwner(GroupAdmin):
    pass


class GroupFile:
    name: str
    pass


RunnerReturn = TypeVar('RunnerReturn', GroupMember, GroupAdmin, GroupOwner, GroupFile,)


class GroupInfo:
    pass


class UserInfo:
    pass


def ensure_not_empty_selection(f):
    # todo 当当前选择的group被exclude之后，如果此时选择的group为零，raise EmptySelectException
    @wraps
    def wrapper(self: CommonAction, *args, **kwargs):
        if not len(self.selections):
            raise EmptySelectionException

        return f(self, *args, **kwargs)
    return wrapper


class PermissionError(Exception):
    pass


def permission(f):
    @wraps
    def wrapper(self, *args, **kwargs):

        return f(self, *args, **kwargs)
    return wrapper


# 之所以使用外部context，而不是挂载到class或实例上，是因为复用选择的缘故
# 还有并发时的锁的问题
runnerContext = {}


class OnlyRunner():

    # Iterable[Union[GroupMember, GroupFile, GroupAdmin]]
    async def run(self, *args) -> None:
                # todo 不直接使用asyncio的run方法，全局应只使用一次
        await self.__schedule()
        return

    # todo 对__方法自动加类名，只是在实例化之后吗？也就是说，mixin是，子类也是可以访问到__方法的
    async def __schedule(self):
        """根据runnerContext，编译出真正的执行链

        包括对catch的切片
        """
        return


class CommonAction(OnlyRunner):

    def catch(self, *args):
        # todo 以catch造断面，或者说切片
        return self

    def sleep(self, *args):
        return self

    def __send_message(self, *args):
        pass

    @property
    def selections(self):
        return []


class SingleSelectAction(ABC):
    @abstractmethod
    def send_message(self, *args):
        raise NotImplementedError()


ACTION_PERMISSION = {
    "owner": [
        "set_admin",
        "remove_admin",
    ],
    "admin": [
        "set_group_portrait",
        "new_notice"
    ],
    "member": [
        "send_message"
    ]
}

# todo 检查禁言状态
# todo 全员禁言状态时的权限检查


class SingleGroupAction(SingleSelectAction, CommonAction):
    def __get_bot_info(self):
        """获取bot自身的信息，用于权限校验"""
        pass

    def send_message(self, *args):
        return self

    @permission
    def new_notice(self, *args, **kwargs):
        return self

    @permission
    def set_admin(self, *args, **kwargs):
        # todo 权限校验，如果机器人不是群主，raise PermissionError
        pass

    @permission
    def remove_admin(self, *args, **kwargs):
        # todo 权限校验，如果机器人不是群主，raise PermissionError
        pass

    @permission
    def set_group_portrait(self, *args, **kwargs):
        # todo 权限校验
        pass

    # 以下都是end point

    async def members(self, *args) -> Generator[GroupMember, None, None]:
        for i in range(10):
            yield GroupMember()

    async def files(self, *args):
        for i in range(10):
            yield GroupFile()

    async def admins(self, *args):
        for i in range(10):
            yield GroupAdmin()

    def info(self, *args):
        return GroupInfo()

    def owner(self, *args):
        return GroupOwner()


class SingleUserAction(SingleSelectAction, CommonAction):
    def info(self, *args):
        return UserInfo()


# todo 抽象基类
# @ABC()
class MultiSelectAction(CommonAction):
    def exclude(self, *args):
        raise NotImplementedError()

    def include(self, *args):
        raise NotImplementedError()

    def clear(self, *args):
        raise NotImplementedError()

    def each(self, *args):
        raise NotImplementedError()

    def async_each(self, *args):
        raise NotImplementedError()

    def send_message(self, *args):
        raise NotImplementedError()


class EmptySelectionException(Exception):
    pass


class MultiGroupAction(MultiSelectAction):
    def exclude(self, *args):
        return self

    def include(self, *args):
        return self

    def clear(self, *args):
        return self

    @ensure_not_empty_selection
    def each(self, handler: Union[Callable[..., Union[Any, Coroutine[Any, Any, None]]]] = None):
        return self

    @ensure_not_empty_selection
    def async_each(self, handler: Union[Callable[..., Union[Any, Coroutine[Any, Any, None]]]] = None):
        return self

    @ensure_not_empty_selection
    def send_message(self, *args):
        """因为非常常用，所以从singleSelection提升至multiSelection，内部仅仅是循环调用__send_message"""
        return self


class MultiUserAction(MultiSelectAction):
    pass


class ActionChain:

    def selectGroup(self, groupId) -> SingleGroupAction:
        # todo 如果仅有的一个选择也是无效的，那么raise EmptySelectionException

        # if len(args) == 1:  # 选择一个群
        return SingleGroupAction()
        # else:
        #     raise Exception("未指定")

    def selectGroups(self, *args) -> MultiGroupAction:
        argsLength = len(args)

        if argsLength:
            return MultiGroupAction()
        else:  # 选择所有群
            return MultiGroupAction()

    def selectUser(self, *args):
        # todo 如果仅有的一个选择也是无效的，那么raise EmptySelectionException

        return SingleUserAction()

    def selectUsers(self, *args):
        return MultiUserAction()

    def groups(self):
        return []

    def friends(self):
        return []


class NotRunnableError(Exception):
    # todo 定义的所有Exception，都应有trace
    pass


class ActionRunner:
    """按照规则调用所有传入的action的run方法

    对asyncio库封装了常用操作，降低与PepperBot的整合成本
    """

    @staticmethod
    def __is_runnable(action: OnlyRunner):
        runMethod = getattr(action, "run")

        if runMethod:
            return True
        return False

    @staticmethod
    async def in_turn(*actions: OnlyRunner, timeout=30, ensureRun=True):
        for action in actions:
            if ActionRunner.__is_runnable(action):
                # todo timeout控制
                await action.run()
            else:
                if ensureRun:
                    raise NotRunnableError()
                else:
                    print("receive invalid action")
                    pass

        return {}

    @staticmethod
    async def all(*actions: OnlyRunner, timeout=30, ensureRun=True):
        tasks = []

        for action in actions:
            if ActionRunner.__is_runnable(action):
                asyncio.create_task(action.run())
            else:
                if ensureRun:
                    raise NotRunnableError()
                else:
                    print("receive invalid action")
                    pass

        asyncio.gather(*tasks)
        return {}

    @staticmethod
    async def all_settled(*actions: OnlyRunner, timeout=30, ensureRun=True):
        tasks = []

        for action in actions:
            if ActionRunner.__is_runnable(action):
                asyncio.create_task(action.run())
            else:
                if ensureRun:
                    raise NotRunnableError()
                else:
                    print("receive invalid action")
                    pass

        # todo asyncio包中，相当于Promise.allSettled的方法
        asyncio.gather(*tasks)
        return {}


class CatchException(Exception):
    pass


# defaultCatchHandler
def catchHandler(exception: CatchException, results: Any):
    pass


async def eachGroup(group: SingleGroupAction):
    pass


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

    # 只能接受runnable的action，即不能members，info等为终点的行为链
    results = await ActionRunner.in_turn(action1, action2)
    results = await ActionRunner.all(action1, action2)
    results = await ActionRunner.all_settled(action1, action2)


if __name__ == "__main__":
    asyncio.run(do_something())
