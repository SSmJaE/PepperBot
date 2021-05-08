import asyncio
import sys
from os import path

BASE_DIR = path.dirname(path.dirname(path.abspath(__file__)))
sys.path.append(BASE_DIR)

from src.Action.Bot import *
# from src.Action.main import *


async def test():

    api = APICaller(port=5700)
    await api.group_msg(1041902989, Face(123))


asyncio.run(test())
