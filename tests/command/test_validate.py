class NoInitial:
    pass


class ReturnSubCommand:
    pass


class TestValidate:
    async def test_no_initial(self):
        pass

    async def test_non_exist_parameter(self):
        """non_exist，或者说wrong

        TODO 看看能不能通过自动寻找最接近的参数名，还要搞个阈值，偏差太远就算了
        """
        pass

    async def test_without_type_annotation(self):
        pass

    async def test_depends_argument(self):
        """可以正常解析depends参数，而不是认为使错误的参数"""
        pass
