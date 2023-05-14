import datetime
import random
import time
from typing import List
import zoneinfo
from devtools import debug

import pytest

from pepperbot.core.event import handle
from pepperbot.core.event.handle import handle_event
from pepperbot.core.message.segment import Image, Text
from pepperbot.extensions.command import as_command
from pepperbot.extensions.command.timeout import run_timeout
from pepperbot.initial import PepperBot
from pepperbot.store import command
from pepperbot.store.command import (
    ClassCommandStatus,
    CLIArgument,
    command_timeout_jobs,
)
from pepperbot.store.meta import BotRoute
from tests.utils import fake_group_event
from tests.conftest import api_results

called_methods: List[str] = []


class InitialOnly:
    def initial(self):
        called_methods.append("initial")


class InitialReturnSelf:
    def initial(self):
        called_methods.append("initial")
        return self.initial


class InitialException:
    def initial(self):
        called_methods.append("initial")
        raise Exception("initial")


class CatchOnly:
    def catch(self):
        called_methods.append("catch")


class CatchException:
    def catch(self):
        called_methods.append("catch")
        raise Exception("catch")


class ExitOnly:
    def exit(self):
        called_methods.append("exit")


class ExitException:
    def exit(self):
        called_methods.append("exit")
        raise Exception("exit")


class TimeoutOnly:
    def timeout(self):
        called_methods.append("timeout")


class TimeoutException:
    def timeout(self):
        called_methods.append("timeout")
        raise Exception("timeout")


class FinishOnly:
    def finish(self):
        called_methods.append("finish")


class FinishException:
    def finish(self):
        called_methods.append("finish")
        raise Exception("finish")


class CleanupOnly:
    def cleanup(self):
        called_methods.append("cleanup")


class CleanupException:
    def cleanup(self):
        called_methods.append("cleanup")
        raise Exception("cleanup")


class InitialForExit(InitialReturnSelf, ExitOnly, CleanupOnly):
    pass


class InitialWithoutReturn(InitialOnly, FinishOnly, CleanupOnly):
    pass


class InitialWithReturnNone(InitialOnly, FinishOnly):
    def initial(self):
        called_methods.append("initial")
        return None


class InitialExceptionWithoutCatch(
    InitialException, ExitOnly, TimeoutOnly, FinishOnly, CleanupOnly
):
    pass


class ExitExceptionWithoutCatch(
    InitialReturnSelf, ExitException, TimeoutOnly, FinishOnly, CleanupOnly
):
    pass


class TimeoutExceptionWithoutCatch(
    InitialReturnSelf, ExitOnly, TimeoutException, FinishOnly, CleanupOnly
):
    pass


class FinishExceptionWithoutCatch(
    InitialOnly, ExitOnly, TimeoutOnly, FinishException, CleanupOnly
):
    pass


class CatchExceptionSelf(
    InitialException, ExitOnly, TimeoutOnly, CatchException, FinishOnly, CleanupOnly
):
    pass


class CleanupExceptionSelf(
    InitialOnly, ExitOnly, TimeoutOnly, CatchOnly, FinishOnly, CleanupException
):
    pass


class InitialExceptionWithCatch(
    InitialException, ExitOnly, TimeoutOnly, CatchOnly, FinishOnly, CleanupOnly
):
    pass


class ExitExceptionWithCatch(
    InitialReturnSelf, ExitException, TimeoutOnly, CatchOnly, FinishOnly, CleanupOnly
):
    pass


class TimeoutExceptionWithCatch(
    InitialReturnSelf, ExitOnly, TimeoutException, CatchOnly, FinishOnly, CleanupOnly
):
    pass


class FinishExceptionWithCatch(
    InitialOnly, ExitOnly, TimeoutOnly, CatchOnly, FinishException, CleanupOnly
):
    pass


class InitialWithPattern(ExitOnly, CatchOnly, TimeoutOnly, FinishOnly, CleanupOnly):
    def initial(self, test: Image = CLIArgument()):
        called_methods.append("initial")
        return None


@pytest.fixture(scope="class")
async def setup_routes():
    bot = PepperBot()

    bot.register_adapter(
        bot_protocol="onebot",
        receive_protocol="http",
        backend_protocol="http",
        backend_host="127.0.0.1",
        backend_port=5700,
        receive_uri="/test_lifecycle",
    )

    commands = [
        # test_pattern_error
        InitialWithPattern,
        # test_exit
        InitialForExit,
        ExitExceptionWithCatch,
        ExitExceptionWithoutCatch,
        # test_timeout,
        TimeoutExceptionWithCatch,
        TimeoutExceptionWithoutCatch,
        # test_finish
        InitialWithoutReturn,
        InitialWithReturnNone,
        # test_exception_without_catch
        InitialExceptionWithoutCatch,
        FinishExceptionWithoutCatch,
        CatchExceptionSelf,
        CleanupExceptionSelf,
        # test_exception_with_catch
        InitialExceptionWithCatch,
        FinishExceptionWithCatch,
    ]

    configured_commands = []

    for command in commands:
        configured_commands.append(
            as_command(
                need_prefix=True,
                include_class_name=True,
            )(command)
        )

    bot.apply_routes(
        [
            BotRoute(
                commands=configured_commands,
                groups="*",
            )
        ]
    )

    yield


@pytest.fixture(scope="function")
async def reset_called_methods():
    yield

    called_methods.clear()


@pytest.fixture(scope="function")
async def reset_command_timeouts():
    yield

    command_timeout_jobs.clear()


@pytest.mark.usefixtures(
    "reset_database",
    "patch_api_caller",
    "setup_routes",
    "reset_api_results",
    "reset_called_methods",
    "reset_command_timeouts",
)
class TestLifecycle:
    """验证有无异常时的调用顺序(隐含验证了该方法是否被调用)"""

    async def test_pattern_error(self):
        """pattern解析出错，不应该触发生命周期

        保持pointer不改变

        通过故意提供错误的pattern，来触发PatternFormatError
        """

        await handle_event(
            "onebot",
            await fake_group_event(
                Text(f"/{InitialWithPattern.__name__} parse_error"),
            ),
        )

        action = api_results[0][0]
        content = api_results[0][1]["message"][0]["data"]["text"]

        assert action == "send_group_msg"
        assert "参数格式错误" in content

        status = await ClassCommandStatus.objects.get(
            command_name=InitialWithPattern.__name__
        )

        assert status.running == True

        # exit、timeout、cleanup、finish、cleanup都不应该被调用
        # 因为没有解析成功，所以不会调用initial
        assert called_methods == []
        assert status.pointer == "initial"

    async def test_exit_with_catch(self):
        """当满足exit_patterns时，应该会执行exit生命周期"""

        # 先触发running，再触发exit
        await handle_event(
            "onebot",
            await fake_group_event(
                Text(f"/{ExitExceptionWithCatch.__name__} no matter what"),
            ),
        )

        await handle_event(
            "onebot",
            await fake_group_event(
                Text(f"退出"),
            ),
        )

        assert called_methods == ["initial", "exit", "catch", "cleanup"]

        status = await ClassCommandStatus.objects.get_or_none(
            command_name=ExitExceptionWithCatch.__name__
        )
        assert status is None, "执行完exit后，应该会删除status(在finally中)"

    async def test_exit_without_catch(self, capfd):
        # 先触发running，再触发exit
        await handle_event(
            "onebot",
            await fake_group_event(
                Text(f"/{ExitExceptionWithoutCatch.__name__} no matter what"),
            ),
        )

        await handle_event(
            "onebot",
            await fake_group_event(
                Text(f"退出"),
            ),
        )

        captured = capfd.readouterr()

        # debug(captured.out.encode().decode("utf-8"))

        # assert "事件响应执行异常，将继续执行下一个事件响应" in captured.out

        # assert False == True

        assert called_methods == ["initial", "exit", "cleanup"]

        status = await ClassCommandStatus.objects.get_or_none(
            command_name=ExitExceptionWithoutCatch.__name__
        )
        assert status is None, "执行完exit后，应该会删除status(在finally中)"

    async def test_timeout_schedule(self):
        """当超时时，应该会执行timeout生命周期

        这里通过直接判断scheduler的调度情况来验证，不自己模拟时间了
        """

        await handle_event(
            "onebot",
            await fake_group_event(
                Text(f"/{TimeoutExceptionWithCatch.__name__} no matter what"),
            ),
        )

        assert len(command_timeout_jobs) == 1

        status = await ClassCommandStatus.objects.get(
            command_name=TimeoutExceptionWithCatch.__name__
        )
        job = command_timeout_jobs[status.id]

        supposed_run_time = datetime.datetime.fromtimestamp(
            status.last_updated_time + status.timeout,
            tz=zoneinfo.ZoneInfo(key="Asia/Shanghai"),
        )

        # 数据库过了一遍的float，可能和实际float不一致
        assert (
            job.next_run_time - datetime.timedelta(seconds=1)
            <= supposed_run_time
            <= job.next_run_time + datetime.timedelta(seconds=1)
        )

    async def test_timeout_with_catch(self):
        """直接通过scheduler触发timeout，看看是否正常运行"""

        await handle_event(
            "onebot",
            await fake_group_event(
                Text(f"/{TimeoutExceptionWithCatch.__name__} no matter what"),
            ),
        )

        status = await ClassCommandStatus.objects.get(
            command_name=TimeoutExceptionWithCatch.__name__
        )

        await run_timeout(status)

        assert called_methods == ["initial", "timeout", "catch", "cleanup"]
        assert len(command_timeout_jobs) == 0

    async def test_timeout_without_catch(self):
        await handle_event(
            "onebot",
            await fake_group_event(
                Text(f"/{TimeoutExceptionWithoutCatch.__name__} no matter what"),
            ),
        )

        status = await ClassCommandStatus.objects.get(
            command_name=TimeoutExceptionWithoutCatch.__name__
        )

        with pytest.raises(Exception, match="timeout"):
            await run_timeout(status)

        assert called_methods == ["initial", "timeout", "cleanup"]
        assert len(command_timeout_jobs) == 0

    @pytest.mark.parametrize(
        "command_class, results",
        [
            (
                InitialWithoutReturn,
                ["initial", "finish", "cleanup"],
            ),  # 顺便测试下，只有有cleanup时，才会执行
            (InitialWithReturnNone, ["initial", "finish"]),
        ],
    )
    async def test_finish(self, command_class, results):
        """当return None或者不return时，应该会执行finish生命周期"""

        await handle_event(
            "onebot",
            await fake_group_event(
                Text(f"/{command_class.__name__} no matter what"),
            ),
        )

        status = await ClassCommandStatus.objects.get_or_none(
            command_name=command_class.__name__
        )
        assert status is None, "执行完finish后，应该会删除status(在finally中)"

        assert called_methods == results

    @pytest.mark.parametrize(
        "command_class, results, exception_name",
        [
            (
                InitialExceptionWithoutCatch,
                ["initial", "cleanup"],  # 如果第一次运行initial就出错的情况
                "initial",
            ),  # 在非生命周期中，出现异常
            (
                FinishExceptionWithoutCatch,
                ["initial", "finish", "cleanup"],
                "finish",
            ),  # 在finish生命周期中，出现异常
            (
                CatchExceptionSelf,
                ["initial", "catch", "cleanup"],
                "catch",
            ),  # 在catch生命周期中，出现异常
            (
                CleanupExceptionSelf,
                ["initial", "finish", "cleanup"],
                "cleanup",
            ),  # 在cleanup生命周期中，出现异常
        ],
    )
    async def test_exception_without_catch(
        self, command_class, results, exception_name
    ):
        """出现异常，但是没有定义catch生命周期

        此时，应该会执行cleanup，然后再抛出异常
        """

        # with pytest.raises(Exception, match=exception_name):
        await handle_event(
            "onebot",
            await fake_group_event(
                Text(f"/{command_class.__name__} no matter what"),
            ),
        )

        assert results == called_methods

        status = await ClassCommandStatus.objects.get_or_none(
            command_name=command_class.__name__
        )
        assert status is None, "抛出异常之前，应该会删除status(在finally中)"

    @pytest.mark.parametrize(
        "command_class, results",
        [
            (InitialExceptionWithCatch, ["initial", "catch", "cleanup"]),
            (FinishExceptionWithCatch, ["initial", "finish", "catch", "cleanup"]),
        ],
    )
    async def test_exception_with_catch(self, command_class, results):
        await handle_event(
            "onebot",
            await fake_group_event(
                Text(f"/{command_class.__name__} no matter what"),
            ),
        )

        assert results == called_methods

        status = await ClassCommandStatus.objects.get_or_none(
            command_name=command_class.__name__
        )
        assert status is None, "应该会删除status(在finally中)"
