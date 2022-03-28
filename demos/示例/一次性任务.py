import asyncio

from pepperbot import PepperBot
from pepperbot.core.bot.universal import ArbitraryApi
from pepperbot.core.message.segment import Text

bot = PepperBot(
    port=53521,
    debug=True,
)

bot.register_adapter(
    bot_protocol="onebot",
    receive_protocol="websocket",
    backend_protocol="http",
    backend_host="127.0.0.1",
    backend_port=5700,
)
# bot.register_adapter(
#     bot_protocol="keaimao",
#     receive_protocol="http",
#     backend_protocol="http",
#     backend_host="192.168.0.109",
#     backend_port=8090,
# )

api = ArbitraryApi


async def main():
    await api.onebot.group_message("1041902989", Text("消息测试"))


asyncio.run(main())
