from collections import OrderedDict
from typing import Dict, Optional

import pytest
from devtools import debug

from pepperbot.core.event.handle import handle_event
from pepperbot.core.message.segment import Text
from pepperbot.extensions.command import as_command, sub_command
from pepperbot.extensions.command.sender import CommandSender
from pepperbot.initial import PepperBot
from pepperbot.store.command import ClassCommandStatus, CLIArgument, CLIOption
from pepperbot.store.meta import BotRoute
from tests.conftest import results
from tests.utils import fake_group_event


@as_command(
    need_prefix=True,
    prefixes=["/"],
    include_class_name=True,
)
class NestCommand:
    async def initial(self, sender: CommandSender):
        await sender.send_message(Text("initial"))

    @sub_command()
    async def b(self, sender: CommandSender):
        await sender.send_message(Text("b"))

    @sub_command(b)
    async def d(self, sender: CommandSender):
        await sender.send_message(Text("d"))

    @sub_command(b)
    async def e(self, sender: CommandSender):
        await sender.send_message(Text("e"))

    @sub_command()
    async def c(self, sender: CommandSender):
        await sender.send_message(Text("c"))

    @sub_command(c)
    async def f(self, sender: CommandSender):
        await sender.send_message(Text("f"))

    @sub_command(c)
    async def g(self, sender: CommandSender):
        await sender.send_message(Text("g"))


@as_command(
    need_prefix=True,
    prefixes=["/"],
    include_class_name=True,
)
class NestCommandAliasName:
    async def initial(self, sender: CommandSender):
        await sender.send_message(Text("initial"))

    @sub_command(name="b_command")
    async def b(self, sender: CommandSender):
        await sender.send_message(Text("b"))

    @sub_command(b, name="d_command")
    async def d(self, sender: CommandSender):
        await sender.send_message(Text("d"))

    @sub_command(b, name="e_command")
    async def e(self, sender: CommandSender):
        await sender.send_message(Text("e"))

    @sub_command(name="c_command")
    async def c(self, sender: CommandSender):
        await sender.send_message(Text("c"))

    @sub_command(c, name="f_command")
    async def f(self, sender: CommandSender):
        await sender.send_message(Text("f"))

    @sub_command(c, name="g_command")
    async def g(self, sender: CommandSender):
        await sender.send_message(Text("g"))


relations = {
    "b": ["d", "e"],
    "c": ["f", "g"],
}

alias_relations = {
    "b_command": ["d_command", "e_command"],
    "c_command": ["f_command", "g_command"],
}

multi_top_level_relations = OrderedDict(
    initial={"b": {"c": {}}},
    second={"d": {"e": {}}},
    third={"f": {"g": {}}},
)


global_context = {}


@pytest.fixture(scope="function")
def reset_global_context():
    yield

    global_context.clear()


@as_command(
    need_prefix=True,
    prefixes=["/"],
    include_class_name=True,
)
class NestCommandWithArgumentsOnly3:
    async def initial(
        self,
        sender: CommandSender,
    ):
        await sender.send_message(Text("initial"))

    @sub_command()
    async def b(
        self,
        sender: CommandSender,
    ):
        await sender.send_message(Text("b"))

    @sub_command(b)
    async def d(
        self,
        sender: CommandSender,
        context: Dict,
        d_positional: str = CLIArgument(),
        d_optional: Optional[str] = CLIOption(),
    ):
        await sender.send_message(Text("d"))
        global_context.update(context)
        global_context["injected"] = {
            "d_positional": d_positional,
            "d_optional": d_optional,
        }


@as_command(
    need_prefix=True,
    prefixes=["/"],
    include_class_name=True,
)
class NestCommandWithArgumentsWith3:
    async def initial(
        self,
        sender: CommandSender,
        a_positional: str = CLIArgument(),
        a_optional: Optional[str] = CLIOption(),
    ):
        await sender.send_message(Text("initial"))

    @sub_command()
    async def b(
        self,
        sender: CommandSender,
        b_positional: str = CLIArgument(),
        b_optional: Optional[str] = CLIOption(),
    ):
        await sender.send_message(Text("b"))

    @sub_command(b)
    async def d(
        self,
        sender: CommandSender,
        context: Dict,
        d_positional: str = CLIArgument(),
        d_optional: Optional[str] = CLIOption(),
    ):
        await sender.send_message(Text("d"))
        global_context.update(context)
        global_context["injected"] = {
            "d_positional": d_positional,
            "d_optional": d_optional,
        }


@as_command(
    need_prefix=True,
    prefixes=["/"],
    include_class_name=True,
)
class NestCommandWithArgumentsWithout3:
    async def initial(
        self,
        sender: CommandSender,
        a_positional: str = CLIArgument(),
        a_optional: Optional[str] = CLIOption(),
    ):
        await sender.send_message(Text("initial"))
        global_context["parsed"] = {
            "a_positional": a_positional,
            "a_optional": a_optional,
        }

    @sub_command()
    async def b(
        self,
        sender: CommandSender,
        b_positional: str = CLIArgument(),
        b_optional: Optional[str] = CLIOption(),
    ):
        await sender.send_message(Text("b"))
        global_context["parsed"]["b_positional"] = b_positional
        global_context["parsed"]["b_optional"] = b_optional

    @sub_command(b)
    async def d(
        self,
        sender: CommandSender,
        context: Dict,
    ):
        await sender.send_message(Text("d"))
        global_context.update(context)
        global_context["injected"] = {}


@as_command(
    need_prefix=True,
    prefixes=["/"],
    include_class_name=True,
)
class MultiTopLevel:
    async def initial(
        self,
        sender: CommandSender,
        initial_optional: Optional[str] = CLIOption(),
    ):
        await sender.send_message(Text("initial"))

        global_context["injected"] = {
            "initial_optional": initial_optional,
        }

        # 因为同时测试了root command的sub command调度能力，此时要返回自身，不然会直接结束指令
        return self.initial

    @sub_command()
    async def b(
        self,
        sender: CommandSender,
        context: Dict,
        b_optional: Optional[str] = CLIOption(),
    ):
        await sender.send_message(Text("b"))

        global_context.update(context)
        global_context["injected"] = {
            "b_optional": b_optional,
        }

        return self.initial

    @sub_command(b)
    async def c(
        self,
        sender: CommandSender,
        context: Dict,
        c_optional: Optional[str] = CLIOption(),
    ):
        await sender.send_message(Text("c"))

        global_context.update(context)
        global_context["injected"] = {
            "c_optional": c_optional,
        }

        return self.second

    async def second(
        self, sender: CommandSender, second_optional: Optional[str] = CLIOption()
    ):
        await sender.send_message(Text("second"))

        global_context["injected"] = {
            "second_optional": second_optional,
        }

        return self.second

    @sub_command(second)
    async def d(
        self,
        sender: CommandSender,
        context: Dict,
        d_optional: Optional[str] = CLIOption(),
    ):
        await sender.send_message(Text("d"))

        global_context.update(context)
        global_context["injected"] = {
            "d_optional": d_optional,
        }

        return self.second

    @sub_command(d)
    async def e(
        self,
        sender: CommandSender,
        context: Dict,
        e_optional: Optional[str] = CLIOption(),
    ):
        await sender.send_message(Text("e"))

        global_context.update(context)
        global_context["injected"] = {
            "e_optional": e_optional,
        }

        return self.third

    async def third(
        self, sender: CommandSender, third_optional: Optional[str] = CLIOption()
    ):
        await sender.send_message(Text("third"))

        global_context["injected"] = {
            "third_optional": third_optional,
        }

        return self.third

    @sub_command(third)
    async def f(
        self,
        sender: CommandSender,
        context: Dict,
        f_optional: Optional[str] = CLIOption(),
    ):
        await sender.send_message(Text("f"))

        global_context.update(context)
        global_context["injected"] = {
            "f_optional": f_optional,
        }

        return self.third

    @sub_command(f)
    async def g(
        self,
        sender: CommandSender,
        context: Dict,
        g_optional: Optional[str] = CLIOption(),
    ):
        global_context.update(context)
        global_context["injected"] = {
            "g_optional": g_optional,
        }

        await sender.send_message(Text("g"))


@pytest.fixture(scope="class")
async def setup_routes():
    bot = PepperBot()

    bot.register_adapter(
        bot_protocol="onebot",
        receive_protocol="http",
        backend_protocol="http",
        backend_host="127.0.0.1",
        backend_port=5700,
    )

    bot.apply_routes(
        [
            BotRoute(
                commands=(
                    NestCommand,
                    NestCommandAliasName,
                    NestCommandWithArgumentsOnly3,
                    NestCommandWithArgumentsWith3,
                    NestCommandWithArgumentsWithout3,
                    MultiTopLevel,
                ),
                groups="*",
            )
        ]
    )

    yield


@pytest.mark.usefixtures(
    "reset_database",
    "patch_api_caller",
    "setup_routes",
    "reset_api_results",
)
class TestSubCommand:
    # single root, multi root
    async def test_relations(self):
        """测试通过@sub_command关联的command的缓存信息是否正确"""

    # single root, multi root
    async def test_build_command_tree(self):
        """"""

    # single root, multi root
    async def test_build_sub_parsers(self):
        """"""

    @pytest.mark.parametrize(
        "given_relations, command_class",
        [(relations, NestCommand), (alias_relations, NestCommandAliasName)],
        ids=["method_name", "alias_name"],
    )
    async def test_nest_dispatch(self, given_relations, command_class):
        """测试调度情况，单root command

        - a(initial)
            - b
                - d
                - e
            - c
                - f
                - g
        """

        await handle_event(
            "onebot",
            await fake_group_event(
                {
                    "type": "text",
                    "data": {
                        "text": f"/{command_class.__name__}",
                    },
                },
            ),
        )

        action = results[0][0]
        content = results[0][1]["message"][0]["data"]["text"]

        assert action == "send_group_msg" and content == "initial"

        results.clear()

        for command in given_relations.keys():
            await handle_event(
                "onebot",
                await fake_group_event(
                    {
                        "type": "text",
                        "data": {
                            "text": f"/{command_class.__name__} {command}",
                        },
                    },
                ),
            )

            action = results[0][0]
            content = results[0][1]["message"][0]["data"]["text"]

            assert action == "send_group_msg"
            assert content == (
                command
                if command_class == NestCommand
                else command.replace("_command", "")
            )

            results.clear()

            for sub_command in given_relations[command]:
                await handle_event(
                    "onebot",
                    await fake_group_event(
                        {
                            "type": "text",
                            "data": {
                                "text": f"/{command_class.__name__} {command} {sub_command}",
                            },
                        },
                    ),
                )

                action = results[0][0]
                content = results[0][1]["message"][0]["data"]["text"]

                assert action == "send_group_msg"
                assert content == (
                    sub_command
                    if command_class == NestCommand
                    else sub_command.replace("_command", "")
                )

                results.clear()

    async def test_multi_top_level_dispatch(self):
        """测试多个顶层command的情况

        对于MultiTopLevel来说，initial是最顶层，second也是

        测试多个root command的情况下，仍然可以调度sub command

        并且测试多个root command之间的状态切换能力(return self.second)
        """

        for root_command, level2_commands in multi_top_level_relations.items():
            await handle_event(
                "onebot",
                await fake_group_event(
                    {
                        "type": "text",
                        "data": {
                            "text": f"/MultiTopLevel",
                        },
                    },
                ),
            )

            # assert True == False

            debug(results)

            action = results[0][0]
            content = results[0][1]["message"][0]["data"]["text"]

            assert action == "send_group_msg" and content == root_command

            results.clear()

            for level2_command_name, level3_commands in level2_commands.items():
                await handle_event(
                    "onebot",
                    await fake_group_event(
                        {
                            "type": "text",
                            "data": {
                                "text": f"/MultiTopLevel {level2_command_name}",
                            },
                        },
                    ),
                )

                action = results[0][0]
                content = results[0][1]["message"][0]["data"]["text"]

                assert action == "send_group_msg"
                assert content == level2_command_name

                results.clear()

                for level3_command in level3_commands:
                    # 此时会触发调度，因为return了下一步的method name
                    await handle_event(
                        "onebot",
                        await fake_group_event(
                            {
                                "type": "text",
                                "data": {
                                    "text": f"/MultiTopLevel {level2_command_name} {level3_command}",
                                },
                            },
                        ),
                    )

                    action = results[0][0]
                    content = results[0][1]["message"][0]["data"]["text"]

                    assert action == "send_group_msg"
                    assert content == level3_command

                    results.clear()

    @pytest.mark.parametrize("help_command", ["-h", "--help"])
    async def test_help_trigger(self, help_command):
        """-h不应该使command进入running"""

        await handle_event(
            "onebot",
            await fake_group_event(
                {
                    "type": "text",
                    "data": {
                        "text": f"/NestCommand {help_command}",
                    },
                },
            ),
        )

        running_command = await ClassCommandStatus.objects.filter(
            running=True
        ).get_or_none()

        assert running_command is None

    @pytest.mark.parametrize("help_command", ["-h", "--help"])
    async def test_initial_help_message(self, help_command):
        """测试默认的帮助信息(单root command)"""

        await handle_event(
            "onebot",
            await fake_group_event(
                {
                    "type": "text",
                    "data": {
                        "text": f"/NestCommand {help_command}",
                    },
                },
            ),
        )

        action = results[0][0]
        content = results[0][1]["message"][0]["data"]["text"]

        assert action == "send_group_msg" and "Usage: NestCommand" in content

    @pytest.mark.parametrize("help_command", ["-h", "--help"])
    async def test_sub_command_help_message(self, help_command):
        """测试单个command的帮助信息"""

        for command in relations.keys():
            await handle_event(
                "onebot",
                await fake_group_event(
                    {
                        "type": "text",
                        "data": {
                            "text": f"/NestCommand {command} {help_command}",
                        },
                    },
                ),
            )

            action = results[0][0]
            content = results[0][1]["message"][0]["data"]["text"]

            assert action == "send_group_msg" and f"Usage: {command}" in content

            results.clear()

            for sub_command in relations[command]:
                await handle_event(
                    "onebot",
                    await fake_group_event(
                        {
                            "type": "text",
                            "data": {
                                "text": f"/NestCommand {command} {sub_command} {help_command}",
                            },
                        },
                    ),
                )

                action = results[0][0]
                content = results[0][1]["message"][0]["data"]["text"]

                assert action == "send_group_msg" and f"Usage: {sub_command}" in content

                results.clear()

    async def test_multi_top_level_help_message(self):
        """对于非initial的根command，可以正常显示帮助信息"""

    @pytest.mark.parametrize(
        "command_class, results, argument_string",
        [
            (
                NestCommandWithArgumentsOnly3,
                {
                    "cli_arguments": {},
                    "injected": {
                        "d_positional": "d_positional_result",
                        "d_optional": "d_optional_result",
                    },
                },
                "b d d_positional_result --d_optional d_optional_result",
            ),
            (
                NestCommandWithArgumentsWithout3,
                {
                    "cli_arguments": {
                        "a_positional": "a_positional_result",
                        "a_optional": "a_optional_result",
                        "b_positional": "b_positional_result",
                        "b_optional": "b_optional_result",
                    },
                    "injected": {},
                },
                "a_positional_result --a_optional a_optional_result b b_positional_result --b_optional b_optional_result d",
            ),
            (
                NestCommandWithArgumentsWith3,
                {
                    "cli_arguments": {
                        "a_positional": "a_positional_result",
                        "a_optional": "a_optional_result",
                        "b_positional": "b_positional_result",
                        "b_optional": "b_optional_result",
                    },
                    "injected": {
                        "d_positional": "d_positional_result",
                        "d_optional": "d_optional_result",
                    },
                },
                "a_positional_result --a_optional a_optional_result b b_positional_result --b_optional b_optional_result"
                + " d d_positional_result --d_optional d_optional_result",
            ),
        ],
        ids=[
            "NestCommandWithArgumentsOnly3",
            "NestCommandWithArgumentsWithout3",
            "NestCommandWithArgumentsWith3",
        ],
    )
    @pytest.mark.usefixtures("reset_global_context")
    async def test_nest_command_arguments(
        self, command_class, results, argument_string
    ):
        """测试嵌套command的参数解析，单root command

        - level 3带参数(positional(必选) + optional)，之前不带
        - level 3带参数，level 1、level 2都带参数(positional(必选) + optional)
        - level 1、level 2都带参数，level 3不带参数

        都是dispatch level 3，level 1、level 2的参数，应该可以在context中获取到
        """

        await handle_event(
            "onebot",
            await fake_group_event(
                {
                    "type": "text",
                    "data": {
                        "text": f"/{command_class.__name__} {argument_string}",
                    },
                },
            ),
        )

        debug(global_context)
        assert (
            results["cli_arguments"].items() <= global_context["cli_arguments"].items()
        )
        assert results["injected"].items() <= global_context["injected"].items()

    async def test_multi_top_level_arguments(self):
        """对于非initial的根command，也可以正常解析参数"""

        for root_command, level2_commands in multi_top_level_relations.items():
            await handle_event(
                "onebot",
                await fake_group_event(
                    {
                        "type": "text",
                        "data": {
                            "text": f"/MultiTopLevel --{root_command}_optional {root_command}_optional_result",
                        },
                    },
                ),
            )

            # assert True == False

            # debug(results)

            action = results[0][0]
            content = results[0][1]["message"][0]["data"]["text"]

            assert action == "send_group_msg" and content == root_command

            assert {
                f"{root_command}_optional": f"{root_command}_optional_result",
            }.items() <= global_context["injected"].items()

            results.clear()
            global_context.clear()

            for level2_command_name, level3_commands in level2_commands.items():
                await handle_event(
                    "onebot",
                    await fake_group_event(
                        {
                            "type": "text",
                            "data": {
                                "text": f"/MultiTopLevel  --{root_command}_optional {root_command}_optional_result"
                                + f" {level2_command_name} --{level2_command_name}_optional {level2_command_name}_optional_result",
                            },
                        },
                    ),
                )

                action = results[0][0]
                content = results[0][1]["message"][0]["data"]["text"]

                assert action == "send_group_msg"
                assert content == level2_command_name

                assert {
                    f"{root_command}_optional": f"{root_command}_optional_result",
                }.items() <= global_context["cli_arguments"].items()
                assert {
                    f"{level2_command_name}_optional": f"{level2_command_name}_optional_result",
                }.items() <= global_context["injected"].items()

                results.clear()
                global_context.clear()

                for level3_command in level3_commands:
                    # 此时会触发调度，因为return了下一步的method name
                    await handle_event(
                        "onebot",
                        await fake_group_event(
                            {
                                "type": "text",
                                "data": {
                                    "text": f"/MultiTopLevel  --{root_command}_optional {root_command}_optional_result"
                                    + f" {level2_command_name} --{level2_command_name}_optional {level2_command_name}_optional_result"
                                    + f" {level3_command} --{level3_command}_optional {level3_command}_optional_result",
                                },
                            },
                        ),
                    )

                    action = results[0][0]
                    content = results[0][1]["message"][0]["data"]["text"]

                    assert action == "send_group_msg"
                    assert content == level3_command

                    assert {
                        f"{root_command}_optional": f"{root_command}_optional_result",
                        f"{level2_command_name}_optional": f"{level2_command_name}_optional_result",
                    }.items() <= global_context["cli_arguments"].items()
                    assert {
                        f"{level3_command}_optional": f"{level3_command}_optional_result",
                    }.items() <= global_context["injected"].items()

                    results.clear()
                    global_context.clear()
