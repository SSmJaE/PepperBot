from typing import Any, List, Optional

import pytest

from pepperbot.core.event.handle import handle_event
from pepperbot.core.message.segment import Image, Text
from pepperbot.extensions.command import as_command
from pepperbot.extensions.command.sender import CommandSender
from pepperbot.initial import PepperBot
from pepperbot.store.command import CLIArgument
from pepperbot.store.meta import BotRoute
from tests.conftest import results
from tests.utils import fake_group_event


@as_command(
    need_prefix=True,
    prefixes=["/"],
    include_class_name=True,
)
class PositionalBaseType:
    async def initial(self, sender: CommandSender, test: str = CLIArgument()):
        await sender.send_message(Text(test))


@as_command(
    need_prefix=True,
    prefixes=["/"],
    include_class_name=True,
)
class PositionalSegmentType:
    async def initial(self, sender: CommandSender, test: Image = CLIArgument()):
        await sender.send_message(Text(test.file_path))


@as_command(
    need_prefix=True,
    prefixes=["/"],
    include_class_name=True,
)
class PositionalAnyType:
    async def initial(self, sender: CommandSender, test: Any = CLIArgument()):
        await sender.send_message(Text(test.__class__.__name__))


@as_command(
    need_prefix=True,
    prefixes=["/"],
    include_class_name=True,
)
class MultiPositionalBaseType:
    async def initial(self, sender: CommandSender, test: List[str] = CLIArgument()):
        await sender.send_message(Text(" ".join(test)))


@as_command(
    need_prefix=True,
    prefixes=["/"],
    include_class_name=True,
)
class MultiPositionalSegmentType:
    async def initial(self, sender: CommandSender, test: List[Image] = CLIArgument()):
        await sender.send_message(Text(" ".join([i.file_path for i in test])))


@as_command(
    need_prefix=True,
    prefixes=["/"],
    include_class_name=True,
)
class OptionalPositionalSingle:
    async def initial(self, sender: CommandSender, test: Optional[str] = CLIArgument()):
        await sender.send_message(Text(f"{test}"))


@as_command(
    need_prefix=True,
    prefixes=["/"],
    include_class_name=True,
)
class OptionalPositionalMulti:
    async def initial(
        self, sender: CommandSender, test: Optional[List[str]] = CLIArgument()
    ):
        await sender.send_message(Text(" ".join(test) if test else "None"))


@as_command(
    need_prefix=True,
    prefixes=["/"],
    include_class_name=True,
)
class DefaultPositionalSingle:
    async def initial(
        self, sender: CommandSender, test: str = CLIArgument(default="1")
    ):
        await sender.send_message(Text(f"{test}"))


@as_command(
    need_prefix=True,
    prefixes=["/"],
    include_class_name=True,
)
class DefaultPositionalMulti:
    async def initial(
        self,
        sender: CommandSender,
        test: List[str] = CLIArgument(default=["1", "2", "3"]),
    ):
        await sender.send_message(Text(f"{' '.join(test)}"))


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
                    PositionalBaseType,
                    PositionalSegmentType,
                    PositionalAnyType,
                    MultiPositionalBaseType,
                    MultiPositionalSegmentType,
                    OptionalPositionalSingle,
                    OptionalPositionalMulti,
                    DefaultPositionalSingle,
                    DefaultPositionalMulti,
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
class TestCommandArgument:
    async def test_positional_base_type(self):
        """测试基本类型的位置参数"""

        await handle_event(
            "onebot",
            await fake_group_event(
                {
                    "type": "text",
                    "data": {
                        "text": "/PositionalBaseType test",
                    },
                },
            ),
        )

        # debug(results)

        action = results[0][0]
        content = results[0][1]["message"][0]["data"]["text"]

        assert action == "send_group_msg" and content == "test"

    async def test_positional_segment_type(self):
        """测试segment类型的位置参数"""

        file_path = "https://i0.hdslb.com/1.jpg"

        await handle_event(
            "onebot",
            await fake_group_event(
                {
                    "type": "text",
                    "data": {
                        "text": "/PositionalSegmentType",
                    },
                },
                Image(file_path),
            ),
        )

        action = results[0][0]
        content = results[0][1]["message"][0]["data"]["text"]

        assert action == "send_group_msg" and content == file_path

    async def test_positional_any_type_base(self):
        """测试Any类型的位置参数"""

        await handle_event(
            "onebot",
            await fake_group_event(
                {
                    "type": "text",
                    "data": {
                        "text": "/PositionalAnyType test",
                    },
                },
            ),
        )

        # debug(results)

        action = results[0][0]
        content = results[0][1]["message"][0]["data"]["text"]

        assert action == "send_group_msg" and content == "str"

    async def test_positional_any_type_segment(self):
        file_path = "https://i0.hdslb.com/1.jpg"

        await handle_event(
            "onebot",
            await fake_group_event(
                {
                    "type": "text",
                    "data": {
                        "text": "/PositionalAnyType",
                    },
                },
                Image(file_path),
            ),
        )

        action = results[0][0]
        content = results[0][1]["message"][0]["data"]["text"]

        assert action == "send_group_msg" and content == "Image"

    async def test_positional_wrong_type(self):
        """测试错误类型的位置参数"""

        await handle_event(
            "onebot",
            await fake_group_event(
                {
                    "type": "text",
                    "data": {
                        "text": "/PositionalBaseType",
                    },
                },
                Image("https://i0.hdslb.com/1.jpg"),
            ),
        )

        action = results[0][0]
        content = results[0][1]["message"][0]["data"]["text"]

        assert action == "send_group_msg" and "参数解析失败" in content

    async def test_multi_positional_base_type(self):
        strings = ["1", "2", "3", "4", "5"]
        space_joined = " ".join(strings)

        await handle_event(
            "onebot",
            await fake_group_event(
                {
                    "type": "text",
                    "data": {
                        "text": f"/MultiPositionalBaseType {space_joined}",
                    },
                },
            ),
        )

        action = results[0][0]
        content = results[0][1]["message"][0]["data"]["text"]

        assert action == "send_group_msg" and content == space_joined

    async def test_multi_positional_segment_type(self):
        segments = [
            Image("https://i0.hdslb.com/1.jpg"),
            Image("https://i0.hdslb.com/2.jpg"),
            Image("https://i0.hdslb.com/3.jpg"),
            Image("https://i0.hdslb.com/4.jpg"),
            Image("https://i0.hdslb.com/5.jpg"),
        ]
        space_joined = " ".join([i.file_path for i in segments])

        await handle_event(
            "onebot",
            await fake_group_event(
                {
                    "type": "text",
                    "data": {
                        "text": f"/MultiPositionalSegmentType",
                    },
                },
                *segments,
            ),
        )

        action = results[0][0]
        content = results[0][1]["message"][0]["data"]["text"]

        assert action == "send_group_msg" and content == space_joined

    @pytest.mark.parametrize("argument", ["", "123"], ids=["empty", "not_empty"])
    async def test_optional_positional(self, argument):
        await handle_event(
            "onebot",
            await fake_group_event(
                {
                    "type": "text",
                    "data": {
                        "text": f"/OptionalPositionalSingle {argument}",
                    },
                },
            ),
        )

        action = results[0][0]
        content = results[0][1]["message"][0]["data"]["text"]

        assert (
            action == "send_group_msg" and content == "None"
            if argument == ""
            else argument
        )

    @pytest.mark.parametrize(
        "argument", [[""], ["1", "2", "3", "4", "5"]], ids=["empty", "not_empty"]
    )
    async def test_optional_positional_multi(self, argument):
        space_joined = " ".join(argument)

        await handle_event(
            "onebot",
            await fake_group_event(
                {
                    "type": "text",
                    "data": {
                        "text": f"/OptionalPositionalMulti {space_joined}",
                    },
                },
            ),
        )

        # debug(results)

        action = results[0][0]
        content = results[0][1]["message"][0]["data"]["text"]

        assert (
            action == "send_group_msg" and content == "None"
            if argument == [""]
            else space_joined
        )

    @pytest.mark.parametrize(
        "argument, default",
        (("", "1"), ("test", "1")),
        ids=["empty", "not_empty"],
    )
    async def test_default_positional(self, argument, default):
        await handle_event(
            "onebot",
            await fake_group_event(
                {
                    "type": "text",
                    "data": {
                        "text": f"/DefaultPositionalSingle {argument}",
                    },
                },
            ),
        )

        action = results[0][0]
        content = results[0][1]["message"][0]["data"]["text"]

        assert (
            action == "send_group_msg" and content == default
            if argument == ""
            else argument
        )

    @pytest.mark.parametrize(
        "argument, default",
        (("", ["1", "2", "3"]), (["4", "5", "6"], ["1", "2", "3"])),
        ids=["empty", "not_empty"],
    )
    async def test_default_positional_multi(self, argument, default):
        space_joined = " ".join(argument if argument else default)

        await handle_event(
            "onebot",
            await fake_group_event(
                {
                    "type": "text",
                    "data": {
                        "text": f"/DefaultPositionalMulti {space_joined}",
                    },
                },
            ),
        )

        action = results[0][0]
        content = results[0][1]["message"][0]["data"]["text"]

        assert action == "send_group_msg" and content == space_joined

    # single multi empty not_empty
    async def test_required_optional(self):
        pass

    async def test_optional_optional(self):
        pass

    async def test_default_optional(self):
        pass

    async def test_optional_action_store_true(self):
        """这种情况，类型只能是bool

        需要检查一下非法情况
        """
        pass
