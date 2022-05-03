import os
import time
from typing import Dict, cast

from devtools import debug
from pepperbot import PepperBot
from pepperbot.adapters.keaimao.api import KeaimaoGroupBot
from pepperbot.adapters.onebot.api import OnebotV11GroupBot
from pepperbot.adapters.onebot.event import OnebotV11GroupEvent
from pepperbot.adapters.telegram.api import TelegramGroupBot, TelegramPrivateBot
from pepperbot.core.bot.universal import UniversalGroupBot
from pepperbot.core.message.chain import MessageChain
from pepperbot.core.message.segment import Image, Music, Text, Video, OnebotFace
from pepperbot.core.route import BotRoute
from pepperbot.extensions.command import PatternArg, as_command
from pepperbot.extensions.command.handle import CommandSender
from pyrogram.client import Client
from pyrogram.types import (
    InlineQuery,
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InlineQueryResultArticle,
    InputTextMessageContent,
    Message,
    ReplyKeyboardMarkup,
)

# class DefaultConfig_Logger:
#     level: str = "debug"
#     write_to_log: bool = True


# class Logger:
#     plugin_name: str = "Logger"
#     config = DefaultConfig_Logger()
#     """ 默认配置 """

# loggerConfig = DefaultConfig_Logger()

# loggerConfig.level = "debug"
# loggerConfig.write_to_log = True

# bot.update_plugin(Logger, loggerConfig)
# bot.register_plugin(scheduler)


bot = PepperBot(
    port=53521,
    debug=True,
)

# bot.register_adapter(
#     bot_protocol="onebot",
#     receive_protocol="websocket",
#     backend_protocol="http",
#     backend_host="127.0.0.1",
#     backend_port=5700,
# )
# bot.register_adapter(
#     bot_protocol="keaimao",
#     receive_protocol="http",
#     backend_protocol="http",
#     backend_host="192.168.1.107",
#     backend_port=8090,
# )
bot.register_telegram(
    "telegram",
    api_id=16355308,
    api_hash="e54d4b8ffdb632f290bd97fd2c530602",
    bot_token="5349474918:AAHS7rk0cAkHZp6Ete5VvDflWftEG84XmMA",
    proxy={
        "scheme": "http",
        "hostname": "127.0.0.1",
        "port": 1080,
    },
)


# str_arg = PatternArg(str)  # type:ignore


@as_command(
    timeout=10,
)
class 指令1:
    async def initial(
        self,
        raw_event: Dict,
        sender: CommandSender,
        name: str = PatternArg(),
        age: int = PatternArg(),
        male: bool = PatternArg(),
        # test_invalid: None = PatternArg(),
        # test_Text: Text = PatternArg(),
        test_segment: OnebotFace = PatternArg(),
    ):
        await sender.send_message(Text(f"收到了你发送的消息 {name} {age} {male}"), test_segment)
        await sender.send_message(Text(f"{name}是个{age}岁的{'男' if male else '女'}人"))

        return self.second

    async def second(self, sender: CommandSender, nonsense: str = PatternArg()):
        await sender.send_message(Text(f"{nonsense}"))

    async def timeout(self, sender: CommandSender):
        await sender.send_message(Text("用户超时未响应"))


@as_command()
class 指令2:
    async def initial(self, raw_event):
        debug("in 指令2")


class 指令3:
    __command_kwargs__ = {}
    pass


class 指令4:
    __command_kwargs__ = {}
    pass


class homepage:
    async def onebot_group_message(
        self,
        bot: OnebotV11GroupBot,
        chain: MessageChain,
    ):
        debug("in group_message")
        debug(bot)

    async def keaimao_group_message(self, bot: KeaimaoGroupBot):
        debug(bot)

    async def group_message(
        self,
        bot: UniversalGroupBot,
        raw_event: Dict,
        chain: MessageChain,
        # test,
    ):

        debug(chain.segments)
        if chain.pure_text == "芜湖":
            await chain.onebot_reply(Text("直接回复消息链"))
            # await bot.group_message(
            #     Text("起飞"),
            #     # Video(
            #     #     # "https://vd4.bdstatic.com/mda-ndanb298u2300y8k/sc/cae_h264_delogo/1649692023013941959/mda-ndanb298u2300y8k.mp4?v_from_s=hkapp-haokan-nanjing&auth_key=1649858900-0-0-bc4b573bb34a510ee61f7de7c9bd76b3&bcevod_channel=searchbox_feed&pd=1&cd=0&pt=3&logid=2300806737&vid=782171143428199568&abtest=100815_2-101454_5-17451_2&klogid=2300806737"
            #     #     r"file:///F:\wx\WeChat Files\wxid_opwzinl7jovm21\FileStorage\Video\2022-04\f945d6043bed5d72283f882e43ca092c.mp4"
            #     # ),
            #     Music("28949129", "qq"),
            # )

            # await bot.arbitrary.keaimao.group_message(
            #     "19521241254@chatroom",
            #     Music("28949129", "163"),
            #     # Image(
            #     # "http://pic.5tu.cn/uploads/allimg/1901/pic_5tu_big_201901170106566711.jpg"
            #     # r"C:\Users\16939201\Desktop\download.jpg"
            #     # ),
            #     # Video(
            #     #     "https://vd4.bdstatic.com/mda-ndanb298u2300y8k/sc/cae_h264_delogo/1649692023013941959/mda-ndanb298u2300y8k.mp4?v_from_s=hkapp-haokan-nanjing&auth_key=1649858900-0-0-bc4b573bb34a510ee61f7de7c9bd76b3&bcevod_channel=searchbox_feed&pd=1&cd=0&pt=3&logid=2300806737&vid=782171143428199568&abtest=100815_2-101454_5-17451_2&klogid=2300806737"
            #     # ),
            # )
        # debug(bot)
        # # debug(raw_event)
        # debug(chain)
        # # debug(bot.onebot)
        # # debug(bot.keaimao)

        # # await bot.group_message(
        # #     Text("一条跨平台消息"),
        # # )

        # if bot.onebot:
        #     #     await bot.arbitrary.keaimao.group_message(
        #     #         "19521241254@chatroom", *chain.segments
        #     #     )
        #     await bot.arbitrary.keaimao.group_message(
        #         "19521241254@chatroom",
        #         # Image(
        #         # "http://pic.5tu.cn/uploads/allimg/1901/pic_5tu_big_201901170106566711.jpg"
        #         # r"C:\Users\16939201\Desktop\download.jpg"
        #         # ),
        #         # Video(
        #         #     "https://vd4.bdstatic.com/mda-ndanb298u2300y8k/sc/cae_h264_delogo/1649692023013941959/mda-ndanb298u2300y8k.mp4?v_from_s=hkapp-haokan-nanjing&auth_key=1649858900-0-0-bc4b573bb34a510ee61f7de7c9bd76b3&bcevod_channel=searchbox_feed&pd=1&cd=0&pt=3&logid=2300806737&vid=782171143428199568&abtest=100815_2-101454_5-17451_2&klogid=2300806737"
        #         # ),
        #     )

        # if bot.keaimao:
        #     await bot.arbitrary.onebot.group_message("1041902989", *chain.segments)

        # if bot.keaimao:
        #     await bot.keaimao.group_message("一条跨平台消息")

    async def telegram_private_message(
        self,
        raw_event: Dict,
        client: Client,
        message: Message,
        chain: MessageChain,
        bot: TelegramPrivateBot,
    ):
        debug(raw_event)
        debug(client, message)
        debug(chain.segments)

        await bot.private_message(
            Text("test"),
            Text("test2"),
        )

        # await message.reply(message.text)

        # await bot.group_message(Text("hello telegram"))

    async def telegram_group_message(
        self,
        raw_event: Dict,
        client: Client,
        message: Message,
    ):
        debug(raw_event)
        debug(client, message)

        # await message.reply(message.text)
        await client.send_message(
            message.from_user.id,  # Edit this
            "This is a InlineKeyboardMarkup example",
            reply_markup=InlineKeyboardMarkup(
                [
                    [  # First row
                        InlineKeyboardButton(  # Generates a callback query when pressed
                            "Button", callback_data="data"
                        ),
                        InlineKeyboardButton(  # Opens a web URL
                            "URL", url="https://docs.pyrogram.org"
                        ),
                    ],
                    [  # Second row
                        InlineKeyboardButton(  # Opens the inline interface
                            "Choose chat", switch_inline_query="pyrogram"
                        ),
                        InlineKeyboardButton(  # Opens the inline interface in the current chat
                            "Inline here", switch_inline_query_current_chat="pyrogram"
                        ),
                    ],
                ]
            ),
        )

        # await bot.group_message(Text("hello telegram"))

    async def telegram_callback_query(
        self,
        raw_event: Dict,
        client: Client,
        callback_query: CallbackQuery,
    ):
        await callback_query.answer(
            f"Button contains: '{callback_query.data}'",
            show_alert=True,
        )

    async def telegram_inline_query(
        self,
        raw_event: Dict,
        client: Client,
        inline_query: InlineQuery,
    ):
        debug(raw_event)
        debug(client, inline_query)

        await inline_query.answer(
            results=[
                InlineQueryResultArticle(
                    title="Installation",
                    input_message_content=InputTextMessageContent(
                        "Here's how to install **Pyrogram**"
                    ),
                    url="https://docs.pyrogram.org/intro/install",
                    description="How to install Pyrogram",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(
                                    "Open website",
                                    url="https://docs.pyrogram.org/intro/install",
                                )
                            ]
                        ]
                    ),
                ),
                InlineQueryResultArticle(
                    title="Usage",
                    input_message_content=InputTextMessageContent(
                        "Here's how to use **Pyrogram**"
                    ),
                    url="https://docs.pyrogram.org/start/invoking",
                    description="How to use Pyrogram",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(
                                    "Open website",
                                    url="https://docs.pyrogram.org/start/invoking",
                                )
                            ]
                        ]
                    ),
                ),
            ],
            cache_time=1,
        )


class HandlerForDynamicGroup:
    pass


def whether_available(mode, source_id):
    return True


from bot.faq import 常见问题

from demos.示例.查询装备 import 查询装备

bot.apply_routes(
    [
        # 为所有消息渠道注册的commands
        # BotRoute(
        #     groups="*",
        #     friends="*",
        #     commands=[指令2, 指令3, 指令4],
        # ),
        # BotRoute(
        #     handler=homepage,
        #     groups="*",
        #     # friends={"keaimao": [99999]},
        # ),
        BotRoute(
            handlers=[homepage],
            commands=[指令1, 常见问题, 查询装备],
            groups={
                "onebot": ["1041902989"],
                "keaimao": ["19521241254@chatroom"],
                "telegram": "*",
            },
            friends="*",
        ),
        # BotRoute(
        #     groups={
        #         "onebot": "*",
        #         "keaimao": [12345, 67890],
        #     },
        #     friends=None,
        #     commands=[指令2, 指令3, 指令4],
        # ),
        # 指定消息渠道
        # BotRoute(
        #     handler=homepage,
        #     protocols=["onebot"],
        #     groups={"onebot": [123, 456]},
        #     friends={"onebot": ["friend123", "friend456"]},
        #     commands=[指令1],
        # ),
        # 动态判断消息渠道
        # BotRoute(
        #     handler=HandlerForDynamicGroup,
        #     protocols=["onebot"],
        #     groups=whether_available,
        #     friends=None,
        # ),
    ]
)

bot.run()


# def test():
#     bot.group_msg()

#     if bot.from_onebot:
#         bot.onebot.group_poke()

#     else:
#         bot.keaimao.hongbao()
