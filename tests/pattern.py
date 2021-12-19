import sys
from os import path

from pydantic.class_validators import VALIDATOR_CONFIG_KEY, Validator
from pydantic.main import create_model
from pydantic import Field


BASE_DIR = path.dirname(path.dirname(path.abspath(__file__)))
sys.path.append(BASE_DIR)


from pepperbot.exceptions import PatternFormotError, PatternValidateError
from pepperbot.command import pattern
from pepperbot.main import *
from pydantic import validator

mockEvent = {
    "message_id": 12345,
    "message": [],
}

chain = MessageChain(mockEvent, 1234, None)

chain.chain = [
    Text("游戏名"),
    Text("10"),
    Text("True"),
    # Text("asdfsd"),
    Text("-200.0"),
    Face(11),
    Text("asdf"),
]

# chain.chain = [
#     Face(50),
#     Text("游戏名"),
#     Face(11),
#     Text("asdf"),
# ]

test_float_parse = re.search(r"\d", "2.3")
debug(test_float_parse)


class TestComplexText(BaseModel):
    游戏名: str
    装备数: int
    加强: bool
    价格: float
    表情: Face
    另一个字符: str

    snap: int = Field(
        42,
        title="The Snap",
        description="this is the value of snap",
        gt=30,
        lt=50,
    )

    class Config:
        arbitrary_types_allowed = True

    @validator("装备数")
    def check_装备数(cls, value):
        if value not in [11, 12, 13]:
            raise PatternFormotError("请输入有效序号")


class Order(BaseModel):
    order: int

    @validator("order")
    def check_order(cls, value):
        if value not in [11, 12, 13]:
            raise PatternFormotError("请输入有效序号")


# create_model(
#     "OrderModel",
#     order=(int, ...),
#     __validators__={"username_validator": validator("username")(username_alphanumeric)},
# )


def extract_validators(pattern_model: object):
    validators: Dict[str, List[Validator]] = {}
    validator_config = getattr(pattern_model, VALIDATOR_CONFIG_KEY, None)
    if validator_config:
        fields, v = validator_config
        for field in fields:
            if field in validators:
                validators[field].append(v)
            else:
                validators[field] = [v]
    return validators


class TestFirstFieldNotText(BaseModel):
    第一个表情: Face
    价格: float
    表情: Face
    另一个字符: str

    class Config:
        arbitrary_types_allowed = True


class TestSignedIntAndInteger:
    pass


class GroupCommonBot:
    async def group_msg(self, *args):
        debug(args)


class Mock:
    kwargs = {}

    @pattern(TestComplexText)
    # @pattern(TestFirstFieldNotText)
    async def deliver(
        self,
        bot: GroupCommonBot,
        chain: MessageChain,
        context: Dict,
    ):
        pass


mock = Mock()

asyncio.run(mock.deliver(bot=GroupCommonBot(), chain=chain, context={}))
# debug(extract_validators(TestComplexText))

# debug(dir(TestComplexText))

# debug(TestComplexText.__validators__)
# debug(dir(TestComplexText.__validators__["装备数"][0]))
# debug(TestComplexText.__validators__["装备数"][0].func)
# debug(
#     TestComplexText.__validators__["装备数"][0].func(
#         TestComplexText.__validators__["装备数"][0].func.__class__, 10
#     )
# )
