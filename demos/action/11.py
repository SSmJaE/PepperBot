import asyncio
import sys
from os import path
import base64

BASE_DIR = path.dirname(path.dirname(path.dirname(path.abspath(__file__))))
sys.path.append(BASE_DIR)

from src.Action.Bot import *
from src.Action.main import *

import requests


# from src.Message.PokeTypes import PokeTypes

import os
from os import path
import random


def get_random_pic():
    basePath = r"C:\Users\16939201\Documents\Tencent Files\1269266841\FileRecv\质量图1"

    file = random.choice(os.listdir(basePath))

    return path.join(basePath, file)


async def test():

    chain = ActionChain()
    # group = chain.select_group(1057809143)
    group = chain.select_group(1041902989)
    # group = chain.select_group(819441084)

    for i in range(3):

        # binaryString = requests.get(
        #     "http://www.api66.cn/api/tts.php",
        #     headers={
        #         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"
        #     },
        #     timeout=10,
        #     params={"txt": "测试消息"},
        # )
        # debug(binaryString)
        # b = base64.b64decode(f)

        await group.send_message(Poke(2539593814)).sleep(1)
        await group.send_message(
            Image(
                f"file:///{get_random_pic()}",
                mode="flash",
            )
        ).sleep(1)
        await group.send_message(
            Audio(
                "https://www.api66.cn/api/tts.php?txt=%E6%B5%8B%E8%AF%95%E6%B6%88%E6%81%AF"
            )
        ).sleep(1)
        await group.send_message(
            Video(
                "http://txmov2.a.yximgs.com/upic/2020/10/10/18/BMjAyMDEwMTAxODU4NDZfMTA0ODU2MjBfMzc0OTEyMjEwNTNfMV8z_b_Ba205f57dc9804c52ffd81377c94a02d8.mp4"
            )
        ).sleep(1)

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
