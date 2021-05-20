import sys
from os import path

BASE_DIR = path.dirname(path.dirname(path.abspath(__file__)))
sys.path.append(BASE_DIR)


from pepperbot.main import *

mockEvent = {
    "message_id": 12345,
    "message": [
        {"type": "face", "data": {"id": 123}},
        {"type": "text", "data": {"text": "word word"}},
        {"type": "text", "data": {"text": "word word2"}},
    ],
}
mockEvent2 = {"message_id": 7238908, "message": []}

chain = MessageChain(mockEvent, 1234, None)
chain2 = MessageChain(mockEvent2, 1234, None)

assert chain != chain2

#
assert chain.pure_text == "word wordword word2", "pure_text应只包含Text类型的内容"
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
assert chain.has(Face(123)) == True
assert chain.has(Face(124)) == False
assert chain.has(Face("123")) == True, "如果从后端传入的数据未经过Pydantic类型转换"
# 快捷方式
assert chain.has_and_first(Text) == (True, Text("word word"))
assert chain.has_and_last(Text) == (True, Text("word word2"))
assert chain.has_and_all(Text) == (True, [Text("word word"), Text("word word2")])
# 获取所有指定类型实例
assert chain.faces == [Face(123)]
assert chain.text == [Text("word word"), Text("word word2")]
# 按index取Segment
assert chain[1] == Text("word word")

# 可以直接判断实例
assert Text("word word") == Text("word word")
assert Text("word word") != Text("word word2")
