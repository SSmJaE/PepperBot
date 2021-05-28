import asyncio
import random

from pepperbot.action import *
from pepperbot.action.chain import *
from pepperbot.main import *
from pepperbot.models.sender import Sender


def randomMessage():
    return [
        Face(random.randint(1, 100)),
        Face(random.randint(1, 100)),
        Face(random.randint(1, 100)),
    ]


welcomeMessage = [Text("欢迎"), Face(150), Image("url")]


async def test():

    chain = ActionChain()

    group = chain.select_group(1041902989)

    await group.send_message(
        # Share(f"https://www.zhihu.com/", title="分享", content="123"),
        # Music(id="001LuLtP1LqITK", source="qq"),
        Music(id="1807708605", source="163")
    )


asyncio.run(test())


# @register(groupId=1041902989)
# class WhateverNameYouWant:
#     async def group_message(
#         self, bot: GroupCommonBot, chain: MessageChain, sender: Sender
#     ):

#         await bot.group_msg(*welcomeMessage)
#         await bot.group_msg(*randomMessage())
