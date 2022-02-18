from apscheduler.triggers.interval import IntervalTrigger
from pepperbot import PepperBot
from pepperbot.core.bot.universal import ArbitraryApi
from pepperbot.core.message.segment import Text
from pepperbot.extensions.scheduler import async_scheduler

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
    await api.onebot.group_message("1041902989", Text("定时消息测试"))


async_scheduler.add_job(main, IntervalTrigger(seconds=10))

bot.run()
