from os import path
import sys 
BASE_DIR = path.dirname(path.dirname(path.abspath(__file__)))
sys.path.append(BASE_DIR)


from textwrap import dedent

from pydantic.tools import parse_obj_as

from pepperbot.command import as_command, pattern, with_command
from pepperbot.main import *
from pepperbot.models.sender import Sender



class TestModel(BaseModel):
    order: Text
    face: Face

    class Config:
        arbitrary_types_allowed = True


# items = parse_obj_as(List[Face], [Text("1234")])
items = parse_obj_as(TestModel, [Text("1234")])
debug(items)
