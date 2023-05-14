import pytest
from pepperbot.core.message.chain import MessageChain
from pepperbot.core.message.segment import *


mock_event = {
    "message_id": 12345,
    "message": [
        {"type": "face", "data": {"id": 123}},
        {"type": "text", "data": {"text": "word word"}},
        {"type": "text", "data": {"text": "word word2"}},
    ],
}
mock_event2 = {"message_id": 7238908, "message": []}

chain = MessageChain("onebot", "group", mock_event, "123456789", "987654321")


chain2 = MessageChain("onebot", "group", mock_event2, "123456789", "987654321")


@pytest.fixture(scope="class")
async def construct_chain():
    await chain.construct()
    await chain2.construct()


@pytest.mark.usefixtures("construct_chain")
class TestMessageChain:
    async def test_chain_equal(self):
        assert chain != chain2

    async def test_pure_text(self):
        assert chain.pure_text == "word wordword word2", "pure_text应只包含Text类型的内容"

    async def test_has_item(self):
        # 字符串可以直接in
        assert "word" in chain
        # 只取pure_text
        assert "123" not in chain
        # 可以判断是否指定类型
        assert Text in chain
        assert chain.has(Text) == True
        # 可以判断是否指定类型的实例
        assert Text("word2") not in chain
        assert Text("word word") in chain
        assert chain.has(Text("word word")) == True
        assert chain.has(Text("word word1")) == False
        assert chain.has(OnebotFace(123)) == True
        assert chain.has(OnebotFace(124)) == False
        assert chain.has(OnebotFace(123)) == True, "如果从后端传入的数据未经过Pydantic类型转换"
        # 快捷方式
        assert chain.has_and_first(Text) == (True, Text("word word"))
        assert chain.has_and_last(Text) == (True, Text("word word2"))
        assert chain.has_and_all(Text) == (
            True,
            [Text("word word"), Text("word word2")],
        )

    async def test_get_items(self):
        # 获取所有指定类型实例
        assert chain.onebot_faces == [OnebotFace(123)]
        assert chain.text == [Text("word word"), Text("word word2")]
        # 按index取Segment
        assert chain[1] == Text("word word")
