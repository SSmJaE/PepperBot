import asyncio
import sys
from os import path

BASE_DIR = path.dirname(path.dirname(path.dirname(path.abspath(__file__))))
sys.path.append(BASE_DIR)

from src.Action.Bot import *
from src.Action.main import *


async def test():

    chain = ActionChain()
    # group = chain.select_group(1057809143)
    group = chain.select_group(1041902989)
    # group = chain.select_group(819441084)

    for i in range(10):
        await group.send_message(Text(f"第{100+i}个表情"), Face(100 + i)).sleep(1)
        # await asyncio.sleep(1)
    # with open("members.json", encoding="utf8", mode="a") as f:

    #     f.write("[")
    # async for member in group.members():
    #         debug(member)
    #         f.write(json.dumps(member.dict(), ensure_ascii=False) + ",")
    #         member.action_test()
    #     f.write("]")
    # await group.info()


asyncio.run(test())
