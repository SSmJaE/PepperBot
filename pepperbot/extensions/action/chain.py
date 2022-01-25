from __future__ import annotations

import asyncio
import inspect
import random
from abc import abstractmethod
from functools import wraps
from typing import (
    Any,
    AsyncGenerator,
    Awaitable,
    Callable,
    Coroutine,
    Generator,
    Generic,
    Iterable,
    List,
    Literal,
    Sequence,
    TypeVar,
    Union,
    cast,
)

from devtools import debug
from httpx import Response
from pepperbot.action import APICaller
from pepperbot.action.decorators import (
    BranchableChain,
    ContextItem,
    end_point,
    ensure_not_empty_selection,
    permission,
    schedule,
)
from pepperbot.globals import GLOBAL_CONFIG
from pepperbot.message.chain import SegmentInstance_T
from pepperbot.models import *
from pepperbot.models.api import get_group_member_list_return
from pepperbot.models.user import *
from pepperbot.models.UserInfo import UserInfo
from pepperbot.utils.common import get_current_function_name
from pydantic import BaseModel

RunnerReturn = TypeVar(
    "RunnerReturn",
    GroupMember,
    GroupAdmin,
    GroupOwner,
    GroupFile,
)

EndPoint_T = TypeVar("EndPoint_T", Callable, AsyncGenerator)


ACTION_PERMISSION = {
    "owner": [
        "set_admin",
        "remove_admin",
    ],
    "admin": ["set_group_portrait", "new_notice"],
    "member": ["send_message"],
}

# todo 检查禁言状态
# todo 全员禁言状态时的权限检查


# todo 抽象基类
# @ABC()


api = globalApi = APICaller(port=5700, proxies=GLOBAL_CONFIG.get("HTTP_PROXY") or None)


class OnlyRunner:
    context: List[ContextItem]
    _selections: List[Any]
    selectionType: Union[Literal["group", "user"]]

    _OnlyRunner__schedule: Callable[..., Awaitable[Any]]

    # Iterable[Union[GroupMember, GroupFile, GroupAdmin]]

    async def run(self, *args) -> None:
        # todo 不直接使用asyncio的run方法，全局应只使用一次
        await self.__schedule()
        return

    # todo 对__方法自动加类名，只是在实例化之后吗？也就是说，mixin是，子类也是可以访问到__方法的
    async def __schedule(self):
        """
        根据runnerContext，编译出真正的执行链

        包括对catch的切片
        """

        debug(self.context)

        # todo 类型转换，int | None => int
        targetGroup: Any = None
        # targetGroup:Optional[int]=None
        # todo 先预处理一下，而不是直接执行，因为要切片catch
        for item in self.context:
            # todo 不判断字符串，直接判断 action == SingleGroup.members，直接判断函数是否相等
            if item.action == "select_group":
                targetGroup = item.payload

            elif item.action == "send_message":
                await api.group_msg(targetGroup, *item.args)

            elif item.action == "sleep":
                await asyncio.sleep(item.args[0])

            elif item.action == "members":
                return await api.members(targetGroup)

        return

    def __await__(self):
        return self.__schedule().__await__()


class CommonAction(OnlyRunner):
    @schedule
    def catch(self, *args):
        # todo 以catch造断面，或者说切片
        return self

    @end_point
    # @schedule
    async def save(self, *args):
        """save也是end point，执行完save之前的所有chain后，直接返回当前的selections"""

        await self.__schedule()
        return self.selections

    @schedule
    def sleep(self, *args):
        return self

    @property
    def selections(self):
        return self._selections


# class SingleSelectAction(ABC):
class SingleSelectAction:
    @abstractmethod
    def send_message(self, *args):
        raise NotImplementedError()


class SingleGroupAction(SingleSelectAction, CommonAction):
    def __init__(self):
        self.context = []
        self._selections = []
        self.selectionType = "group"

    def __get_bot_info(self):
        """获取bot自身的信息，用于权限校验"""
        pass

    # def __await__(self):
    #     return self.__schedule().__await__()

    @schedule
    def send_message(self, *messageChains: SegmentInstance_T):
        # item = ContextItem(action=get_current_function_name(), payload=messageChains)
        # self.context = [*self.context]
        # self.context.append(item)
        return self

    @permission
    @schedule
    def new_notice(self, *args, **kwargs):
        return self

    @permission
    @schedule
    def set_admin(self, *args, **kwargs):
        # todo 权限校验，如果机器人不是群主，raise PermissionError
        pass

    @permission
    @schedule
    def remove_admin(self, *args, **kwargs):
        # todo 权限校验，如果机器人不是群主，raise PermissionError
        pass

    @permission
    @schedule
    def set_group_portrait(self, *args, **kwargs):
        # todo 权限校验
        pass

    @end_point
    async def members(self):
        # async def members(self, *args) -> Generator[GroupMember, None, None]:
        debug(dir(self))
        result: Response = await self._OnlyRunner__schedule()
        # debug()
        members = get_group_member_list_return(**result.json()).data
        debug(members)

        for member in members:
            yield member

    @end_point
    async def files(self, *args):
        for i in range(10):
            yield GroupFile()

    @end_point
    async def admins(self, *args):
        for i in range(10):
            yield GroupAdmin()

    @end_point
    async def info(self, *args):
        return GroupInfo()

    @end_point
    async def owner(self, *args):
        return GroupOwner()


class SingleUserAction(SingleSelectAction, CommonAction):
    def __init__(self, context=None):
        self.context = []

    def info(self, *args):
        return UserInfo()


class MultiSelectAction(CommonAction):
    context: List[ContextItem]

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


class MultiGroupAction(MultiSelectAction):
    context: List[ContextItem]

    def __init__(self, context=None):
        self.context = []

    # @schedule
    def exclude(self, *args):
        return self

    # @schedule
    def include(self, *args):
        return self

    # @schedule
    def clear(self, *args):
        return self

    @schedule
    @ensure_not_empty_selection
    def each(
        self,
        handler: Union[Callable[..., Union[Any, Coroutine[Any, Any, None]]]] = None,
    ):
        return self

    @schedule
    @ensure_not_empty_selection
    def async_each(
        self,
        handler: Union[Callable[..., Union[Any, Coroutine[Any, Any, None]]]] = None,
    ):
        return self

    @schedule
    @ensure_not_empty_selection
    def send_message(self, *args):
        """因为非常常用，所以从singleSelection提升至multiSelection，内部仅仅是循环调用__send_message"""
        return self


class MultiUserAction(MultiSelectAction):
    def __init__(self, context=None):
        self.context = []

    async def run(self):
        pass

    async def __await__(self):
        return await self.run()


# def branch(prevChain: BranchableChain) -> BranchableChain:
#     context = prevChain.context

#     chainClass = prevChain.__class__

#     instance = chainClass()
#     instance.context = context

#     return instance


def is_end_point(metaChain):
    return False


def merge(*chains: BranchableChain) -> BranchableChain:
    """返回不带end point的合并后的chain"""
    first, rest = chains[0], chains[1:]

    bufferContext = []

    for chain in rest:
        for metaChain in chain.context:
            if not is_end_point(metaChain):
                bufferContext.append(metaChain)

    # todo deepcopy
    copiedContext = [*first.context]
    copiedContext.extend(bufferContext)

    chainClass = first.__class__

    instance = chainClass()
    instance.context = copiedContext
    return instance


# middleware1 = MultiGroupAction().sleep(1)
# middleware2 = MultiGroupAction().send_message(Text("11"))
# middleware3 = MultiGroupAction().send_message(Face(111))

# merge(middleware1, middleware2, middleware3)


class ActionChain:
    def select_group(self, groupId: int) -> SingleGroupAction:
        # todo 如果仅有的一个选择也是无效的，那么raise EmptySelectionException

        # if len(args) == 1:  # 选择一个群
        instance = SingleGroupAction()
        item = ContextItem(action=get_current_function_name(), payload=groupId)
        instance.context.append(item)
        return instance
        # else:
        #     raise Exception("未指定")

    def select_groups(self, *args) -> MultiGroupAction:
        argsLength = len(args)

        if argsLength:
            return MultiGroupAction()
        else:  # 选择所有群
            return MultiGroupAction()

    def select_user(self, *args):
        # todo 如果仅有的一个选择也是无效的，那么raise EmptySelectionException

        return SingleUserAction()

    def select_users(self, *args):
        return MultiUserAction()

    def groups(self):
        return []

    def friends(self):
        return []


switch_to()
