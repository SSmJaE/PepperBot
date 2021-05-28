import asyncio
import time

from pepperbot.action import *
from pepperbot.action.chain import *


async def test():

    chain = ActionChain()

    group = chain.select_group(1041902989)

    lastTime = time.time()

    while True:
        currentTime = time.time()
        if currentTime - lastTime > 10:
            await group.send_message(
                Text(f"每10秒发送一次"),
            )
            await asyncio.sleep(10)
            lastTime = currentTime


asyncio.run(test())
