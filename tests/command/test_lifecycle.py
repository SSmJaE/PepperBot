from typing import List

import pytest


called_methods: List[str] = []


class InitialOnly:
    def initial(self):
        called_methods.append("initial")


class InitialOnlyWithException:
    def initial(self):
        called_methods.append("initial")
        raise Exception("initial")


class CatchOnly:
    def catch(self):
        called_methods.append("catch")


class ExitOnly:
    def exit(self):
        called_methods.append("exit")


class TimeoutOnly:
    def timeout(self):
        called_methods.append("timeout")


class FinishOnly:
    def finish(self):
        called_methods.append("finish")


class CleanupOnly:
    def cleanup(self):
        called_methods.append("cleanup")


class WithInitialAndCleanup(InitialOnly, CleanupOnly):
    pass


class WithFinishAndCleanup(FinishOnly, CleanupOnly):
    pass


class WithCatch(InitialOnlyWithException):
    def catch(self):
        called_methods.append("catch")


@pytest.mark.parametrize(
    "command_class",
    [
        InitialOnly,
        FinishOnly,
    ],
)
def setup_commands(command_class):
    current_command = as_command()(command_class)


class TestLifecycle:
    def test_pattern_error(self):
        pass


# 全排列
# 验证有无异常时的调用顺序(隐含验证了该方法是否被调用)

[
    (InitialOnly, InitialOnlyWithException),
    CatchOnly,
    ExitOnly,
    TimeoutOnly,
    FinishOnly,
    CleanupOnly,
]
