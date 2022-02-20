from typing import Dict

from devtools import debug
from pepperbot import PepperBot
from pepperbot.adapters.keaimao.api import KeaimaoGroupBot
from pepperbot.adapters.onebot.api import OnebotV11GroupBot
from pepperbot.adapters.onebot.event.event import OnebotV11GroupEvent
from pepperbot.adapters.onebot.message.segment import OnebotFace
from pepperbot.core.bot.universal import UniversalGroupBot
from pepperbot.core.message.chain import MessageChain
from pepperbot.core.message.segment import Image, Text
from pepperbot.core.route import BotRoute
from pepperbot.extensions.command import PatternArg, as_command
from pepperbot.extensions.command.handle import CommandSender

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


# str_arg = PatternArg(str)  # type:ignore


@as_command(
    timeout=10,
)
class 指令1:
    async def initial(
        self,
        raw_event,
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
        pass
        # debug(bot)
        # # debug(raw_event)
        # debug(chain)
        # # debug(bot.onebot)
        # # debug(bot.keaimao)

        # # await bot.group_message(
        # #     Text("一条跨平台消息"),
        # # )

        # if bot.onebot:
        #     await bot.arbitrary.keaimao.group_message(
        #         "19521241254@chatroom", *chain.segments
        #     )
        #     # await bot.arbitrary.keaimao.group_message(
        #     #     "19521241254@chatroom",
        #     #     Image(
        #     #         "http://pic.5tu.cn/uploads/allimg/1901/pic_5tu_big_201901170106566711.jpg"
        #     #     ),
        #     # )

        # if bot.keaimao:
        #     await bot.arbitrary.onebot.group_message("1041902989", *chain.segments)

        # if bot.keaimao:
        #     await bot.keaimao.group_message("一条跨平台消息")


class HandlerForDynamicGroup:
    pass


def whether_available(mode, source_id):
    return True


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
            commands=[指令1],
            groups={
                "onebot": ["1041902989"],
                "keaimao": ["19521241254@chatroom"],
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
