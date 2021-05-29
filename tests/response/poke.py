import sys
from os import path

BASE_DIR = path.dirname(path.dirname(path.dirname(path.abspath(__file__))))
sys.path.append(BASE_DIR)

import asyncio

from pepperbot.main import register
from pepperbot.message.segment import *
from pepperbot.models.user import GroupMember
from pepperbot.parse.bots import GroupCommonBot
from tests.response.fake_server import fakeApi, test_handler, test_run


@register(groupId=[1041902989, 819441084])
class WhateverNameYouWant:
    @test_handler
    async def been_group_poked(self, bot: GroupCommonBot, sender: GroupMember):
        await bot.group_msg(
            Text(f"收到来自{sender.user_id}的poke"),
        )


async def test():

    # test poke
    fakeApi.results.clear()
    results = await test_run(
        {
            "group_id": 1041902989,
            "notice_type": "notify",
            "post_type": "notice",
            "self_id": 1487877062,
            "sender_id": 1269266841,
            "sub_type": "poke",
            "target_id": 1487877062,
            "time": 1621244192,
            "user_id": 1269266841,
        }
    )

    debug(results)

    assert len(results) == 1
    assert results[0].action == "send_group_message", "应该发送了一条群消息"


asyncio.run(test())
