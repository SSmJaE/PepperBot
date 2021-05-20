from pepperbot.main import *
import random

welcomeMessage = [
    Text("欢迎"),
    Face(150),
    Image("url")
]


def randomMessage():
    return [
        Face(random.randint(1, 100)),
        Face(random.randint(1, 100)),
        Face(random.randint(1, 100)),
    ]


@register(groupId=12223331)
class WhateverNameYouWant:

    async def group_message(self, bot: GroupMessageBot, chain: MessageChain, sender: Sender):

        await bot.group_msg(*welcomeMessage)
        await bot.group_msg(*randomMessage())
