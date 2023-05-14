import pytest


class TestRouteParse:
    async def test_direct_any(self):
        """groups="*"的情况"""
        pass

    # @pytest.mark.parametrize("protocol", ["onebot", "telegram", "keaimao"])
    async def test_protocol_any(self):
        """groups={
            "protocol": "*"
        }的情况"""
        pass

    # @pytest.mark.parametrize("protocol", ["onebot", "telegram", "keaimao"])
    async def test_protocol_specific(self):
        """ """

    async def test_validate_validator(self):
        """检查函数签名"""
        pass

    async def test_direct_validator(self):
        """测试根验证器

        groups=validator
        """
        pass

    # @pytest.mark.parametrize("protocol", ["onebot", "telegram", "keaimao"])
    async def test_protocol_validator(self):
        """测试根验证器

        groups={
            "protocol": validator
        }
        """
        pass

    # @pytest.mark.parametrize(
    #     "commands",
    #     [
    #         [
    #             # one_command
    #             # multi command
    #             # one command multi config(as_command)
    #             # one command in multi BotRoute
    #         ],
    #     ],
    # )
    async def test_parse_commands(self):
        pass

    async def test_parse_handlers(self):
        pass
