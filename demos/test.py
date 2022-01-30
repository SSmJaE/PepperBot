from typing import Dict
from pepperbot.adapters.onebot.api import OnebotV11GroupBot
from pepperbot.core.bot.universal import UniversalGroupBot
from pepperbot.core.message.segment import Text
from pepperbot.store.meta import BotRoute
from pepperbot.initial import PepperBot
from devtools import debug

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


from pepperbot.adapters.onebot.event.event import OnebotV11GroupEvent

debug(dir(OnebotV11GroupEvent))
debug(vars(OnebotV11GroupEvent))

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
bot.register_adapter(
    bot_protocol="keaimao",
    receive_protocol="http",
    backend_protocol="http",
    backend_host="192.168.0.109",
    backend_port=8090,
)


class 指令1:
    __command_kwargs__ = {}

    pass


class 指令2:
    __command_kwargs__ = {}
    pass


class 指令3:
    __command_kwargs__ = {}
    pass


class 指令4:
    __command_kwargs__ = {}
    pass


class homepage:
    async def onebot_group_message(self, bot: OnebotV11GroupBot):
        debug("in group_message")
        debug(bot)

    async def group_message(
        self,
        bot: UniversalGroupBot,
        # chain:MessageChain,
        raw_event: Dict,
    ):
        debug(bot)
        # debug(bot.onebot)
        # debug(bot.keaimao)
        # debug(raw_event)

        await bot.group_message(
            Text("一条跨平台消息"),
        )

        if bot.onebot:
            await bot.arbitrary.keaimao.group_message("123", Text("转发消息"))

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
            handler=homepage,
            groups={
                "onebot": ["1041902989"],
                "keaimao": ["19521241254@chatroom"],
            },
            friends=None,
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
