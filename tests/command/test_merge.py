from pepperbot.core.message.segment import At, Text
from pepperbot.extensions.command.utils import merge_adjacent_text_segments


def test_merge_text_of_segments():
    """只有用户组装的segments，可能存在连续的Text片段

    从event解析的话，几乎不存在
    """

    result = merge_adjacent_text_segments([])
    assert result == []

    result = merge_adjacent_text_segments(
        [
            Text("123"),
        ]
    )
    assert result == [
        Text("123"),
    ], "单个Text片段不应该被合并"

    result = merge_adjacent_text_segments(
        [
            At("123"),
        ]
    )
    assert result == [
        At("123"),
    ], "单个At片段不应该被合并"

    result = merge_adjacent_text_segments(
        [
            Text("123"),
            Text("456"),
        ]
    )
    assert result == [
        Text("123 456"),
    ], "连续的Text片段应该被合并"

    result = merge_adjacent_text_segments(
        [
            Text("123"),
            At("456"),
        ]
    )
    assert result == [
        Text("123"),
        At("456"),
    ], "Text片段和At片段不应该被合并"

    result = merge_adjacent_text_segments(
        [
            Text("123"),
            At("456"),
            Text("123"),
        ]
    )
    assert result == [
        Text("123"),
        At("456"),
        Text("123"),
    ], "可以正常处理尾缀的Text片段"

    result = merge_adjacent_text_segments(
        [
            Text("123"),
            At("456"),
            Text("123"),
            Text("123"),
        ]
    )
    assert result == [
        Text("123"),
        At("456"),
        Text("123 123"),
    ], "可以正常处理多个尾缀的Text片段"

    result = merge_adjacent_text_segments(
        [
            At("456"),
            At("456"),
            Text("123"),
            Text("123"),
        ]
    )
    assert result == [
        At("456"),
        At("456"),
        Text("123 123"),
    ], "可以处理没有前缀Text片段的情况"

    result = merge_adjacent_text_segments(
        [
            At("456"),
            At("456"),
            Text("123"),
            Text("123"),
            At("456"),
        ]
    )
    assert result == [
        At("456"),
        At("456"),
        Text("123 123"),
        At("456"),
    ], "可以处理没有前缀Text片段，也没有尾缀Text的情况"


# def test_merge_text_of_patterns():
#     result = merge_text_of_patterns([])
#     assert result == []

#     # only one Text pattern
#     result = merge_text_of_patterns(
#         [
#             ("a", str),
#         ]
#     )
#     assert result == [
#         [
#             ("a", str),
#         ]
#     ]

#     # only one No Text pattern
#     result = merge_text_of_patterns(
#         [
#             ("a", Image),
#         ]
#     )
#     assert result == [
#         ("a", Image),
#     ]

#     # all Text pattern
#     result = merge_text_of_patterns(
#         [
#             ("a", str),
#             ("a", str),
#         ]
#     )
#     assert result == [
#         [
#             ("a", str),
#             ("a", str),
#         ]
#     ]

#     # no str Text pattern
#     result = merge_text_of_patterns(
#         [
#             ("a", str),
#             ("a", int),
#         ]
#     )
#     assert result == [
#         [
#             ("a", str),
#             ("a", int),
#         ]
#     ]

#     # str and not Text
#     result = merge_text_of_patterns(
#         [
#             ("a", str),
#             ("a", Image),
#         ]
#     )
#     assert result == [
#         [
#             ("a", str),
#         ],
#         ("a", Image),
#     ]

#     result = merge_text_of_patterns(
#         [
#             ("a", str),
#             ("a", Image),
#             ("a", str),
#         ]
#     )
#     assert result == [
#         [
#             ("a", str),
#         ],
#         ("a", Image),
#         [
#             ("a", str),
#         ],
#     ], "str and not Text and str"

#     result = merge_text_of_patterns(
#         [
#             ("a", str),
#             ("a", Image),
#             ("a", Image),
#         ]
#     )
#     assert result == [
#         [
#             ("a", str),
#         ],
#         ("a", Image),
#         ("a", Image),
#     ], "str and not Text and not Text"

#     # str and not Text and not Text
#     result = merge_text_of_patterns(
#         [
#             ("a", str),
#             ("a", Image),
#             ("a", At),
#         ]
#     )
#     assert result == [
#         [
#             ("a", str),
#         ],
#         ("a", Image),
#         ("a", At),
#     ]

#     # str and not Text and not Text
#     result = merge_text_of_patterns(
#         [
#             ("a", At),
#             ("a", str),
#             ("a", Image),
#         ]
#     )
#     assert result == [
#         ("a", At),
#         [
#             ("a", str),
#         ],
#         ("a", Image),
#     ]

#     # str and not Text and not Text
#     result = merge_text_of_patterns(
#         [
#             ("a", At),
#             ("a", str),
#             ("a", int),
#             ("a", Image),
#         ]
#     )
#     assert result == [
#         ("a", At),
#         [
#             ("a", str),
#             ("a", int),
#         ],
#         ("a", Image),
#     ]

#     result = merge_text_of_patterns(
#         [
#             ("a", At),
#             ("a", Image),
#             ("a", str),
#             ("a", float),
#         ]
#     )
#     assert result == [
#         ("a", At),
#         ("a", Image),
#         [
#             ("a", str),
#             ("a", float),
#         ],
#     ]
