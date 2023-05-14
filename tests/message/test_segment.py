from pepperbot.core.message.segment import *


class TestMessageChain:
    async def test_segment_equal(self):
        # 可以直接判断实例
        assert Text("word word") == Text("word word")
        assert Text("word word") != Text("word word2")

    async def test_image_flash(self):
        assert (
            Image("https://i0.hdslb.com/1.jpg", mode="flash").onebot_is_flash() == True
        )
        assert Image("https://i0.hdslb.com/1.jpg").onebot_is_flash() == False
