class TestDispatchGroup:
    async def test_priority(self):
        pass

    async def test_concurrency(self):
        """测试是否是并发执行的"""
        pass

    async def test_concurrency_false(self):
        """测试是否是串行执行的"""
        pass

    async def test_group(self):
        """测试是否成功分组"""
        pass

    async def test_group_concurrency(self):
        """测试group与group之间，是否是并发执行的"""
        pass

    async def test_stop_propagation(self):
        """测试stop_propagation是否生效"""
        pass

    async def test_stop_propagation_with_group(self):
        """测试stop_propagation是否生效，仅在group中生效"""
        pass

    async def no_pre_activate_command(self):
        """测试没有pre_activate_command的情况"""
        pass
