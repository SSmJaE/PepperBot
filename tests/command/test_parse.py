from devtools import debug
from pepperbot.adapters.onebot.message.segment import OnebotFace
from pepperbot.core.message.segment import At, Image, Text
from pepperbot.extensions.command.pattern import (
    merge_text_of_segments,
    merge_text_of_patterns,
)


def test_merge_text_of_segments():
    result = merge_text_of_segments([])
    assert result == []

    result = merge_text_of_segments(
        [
            Text("123"),
        ]
    )
    assert result == [
        Text("123"),
    ]

    result = merge_text_of_segments(
        [
            At("123"),
        ]
    )
    assert result == [
        At("123"),
    ]

    result = merge_text_of_segments(
        [
            Text("123"),
            Text("456"),
        ]
    )
    assert result == [
        Text("123 456"),
    ]

    result = merge_text_of_segments(
        [
            Text("123"),
            At("456"),
        ]
    )
    assert result == [
        Text("123"),
        At("456"),
    ]

    result = merge_text_of_segments(
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
    ]

    result = merge_text_of_segments(
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
    ]

    result = merge_text_of_segments(
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
    ]

    result = merge_text_of_segments(
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
    ]


def test_merge_text_of_patterns():
    result = merge_text_of_patterns([])
    assert result == []

    # only one Text pattern
    result = merge_text_of_patterns(
        [
            ("a", str),
        ]
    )
    assert result == [
        [
            ("a", str),
        ]
    ]

    # only one No Text pattern
    result = merge_text_of_patterns(
        [
            ("a", Image),
        ]
    )
    assert result == [
        ("a", Image),
    ]

    # all Text pattern
    result = merge_text_of_patterns(
        [
            ("a", str),
            ("a", str),
        ]
    )
    assert result == [
        [
            ("a", str),
            ("a", str),
        ]
    ]

    # no str Text pattern
    result = merge_text_of_patterns(
        [
            ("a", str),
            ("a", int),
        ]
    )
    assert result == [
        [
            ("a", str),
            ("a", int),
        ]
    ]

    # str and not Text
    result = merge_text_of_patterns(
        [
            ("a", str),
            ("a", Image),
        ]
    )
    assert result == [
        [
            ("a", str),
        ],
        ("a", Image),
    ]

    result = merge_text_of_patterns(
        [
            ("a", str),
            ("a", Image),
            ("a", str),
        ]
    )
    assert result == [
        [
            ("a", str),
        ],
        ("a", Image),
        [
            ("a", str),
        ],
    ], "str and not Text and str"

    result = merge_text_of_patterns(
        [
            ("a", str),
            ("a", Image),
            ("a", Image),
        ]
    )
    assert result == [
        [
            ("a", str),
        ],
        ("a", Image),
        ("a", Image),
    ], "str and not Text and not Text"

    # str and not Text and not Text
    result = merge_text_of_patterns(
        [
            ("a", str),
            ("a", Image),
            ("a", At),
        ]
    )
    assert result == [
        [
            ("a", str),
        ],
        ("a", Image),
        ("a", At),
    ]

    # str and not Text and not Text
    result = merge_text_of_patterns(
        [
            ("a", At),
            ("a", str),
            ("a", Image),
        ]
    )
    assert result == [
        ("a", At),
        [
            ("a", str),
        ],
        ("a", Image),
    ]

    # str and not Text and not Text
    result = merge_text_of_patterns(
        [
            ("a", At),
            ("a", str),
            ("a", int),
            ("a", Image),
        ]
    )
    assert result == [
        ("a", At),
        [
            ("a", str),
            ("a", int),
        ],
        ("a", Image),
    ]

    result = merge_text_of_patterns(
        [
            ("a", At),
            ("a", Image),
            ("a", str),
            ("a", float),
        ]
    )
    assert result == [
        ("a", At),
        ("a", Image),
        [
            ("a", str),
            ("a", float),
        ],
    ]
