import asyncio
from inspect import isawaitable

from src.Action.main import OnlyRunner
from src.Exceptions import NotRunnableError


class ActionRunner:
    """
    按照规则调用所有传入的action的run方法

    对asyncio库封装了常用操作，降低与PepperBot的整合成本
    """

    @staticmethod
    def __is_runnable(action: OnlyRunner):
        # runMethod = getattr(action, "run")

        # if runMethod:
        #     return True
        # return False

        return isawaitable(action)

    @staticmethod
    async def in_turn(*actions: OnlyRunner, timeout=30, ensureRun=True):
        """按顺序，执行完前一个，再执行下一个"""
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
        """同时执行所有，任意一个任务的异常会打断所有任务的执行"""
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
        """同时执行所有，任意一个任务的异常不会打断其它任务的执行，并且能从函数的返回值中捕获到该错误"""
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
