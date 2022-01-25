from pepperbot.store.meta import BotRoute
from pepperbot.initial import PepperBot

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
    backend_port=8080,
)
bot.register_adapter(
    bot_protocol="keaimao",
    receive_protocol="http",
    backend_protocol="http",
    backend_port=12345,
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
    pass


class HandlerForDynamicGroup:
    pass


def whether_available(mode, source_id):
    return True


bot.apply_routes(
    [
        # 为所有消息渠道注册的commands
        BotRoute(
            groups="*",
            friends="*",
            commands=[指令2, 指令3, 指令4],
        ),
        BotRoute(
            handler=homepage,
            groups="*",
            friends={"keaimao": [99999]},
        ),
        BotRoute(
            groups={
                "onebot": "*",
                "keaimao": [12345, 67890],
            },
            friends=None,
            commands=[指令2, 指令3, 指令4],
        ),
        # 指定消息渠道
        BotRoute(
            handler=homepage,
            protocols=["onebot"],
            groups={"onebot": [123, 456]},
            friends={"onebot": ["friend123", "friend456"]},
            commands=[指令1],
        ),
        # 动态判断消息渠道
        BotRoute(
            handler=HandlerForDynamicGroup,
            protocols=["onebot"],
            groups=whether_available,
            friends=None,
        ),
    ]
)

bot.run()


# def test():
#     bot.group_msg()

#     if bot.from_onebot:
#         bot.onebot.group_poke()

#     else:
#         bot.keaimao.hongbao()
