# from typing import Literal, Optional, Union, cast

# from pepperbot.adapters.keaimao.api import KeaimaoGroupBot, KeaimaoPrivateBot
# from pepperbot.adapters.onebot.api import OnebotV11GroupBot, OnebotV11PrivateBot
# from pepperbot.core.bot.universal import UniversalGroupBot
# from pepperbot.exceptions import EventHandleError
# from pepperbot.store.meta import RouteMapping, get_bot_id
# from pepperbot.types import BaseBot, T_BotProtocol, T_RouteMode


# def get_bot_instance(
#     protocol: T_BotProtocol,
#     mode: T_RouteMode,
#     identifier: str,
#     universal=False,
# ) -> BaseBot:
#     """这里只创建非universal的bot_instance"""

#     instances_dict = RouteMapping.bot_instances

#     if universal:
#         key = ("universal", mode, identifier)
#     else:
#         key = (protocol, mode, identifier)

#     bot_instance: Optional[BaseBot] = None

#     if key not in instances_dict:
#         if universal:
#             bot_instance = UniversalGroupBot(protocol, mode, identifier)

#         else:
#             bot_id = get_bot_id(protocol)

#             if mode == "group":
#                 if protocol == "onebot":
#                     bot_instance = OnebotV11GroupBot(bot_id, identifier)
#                 elif protocol == "keaimao":
#                     bot_instance = KeaimaoGroupBot(bot_id, identifier)
#                 # elif protocol == "telegram":
#                 #     bot_instance = TelegramGroupBot(bot_id, identifier)

#             elif mode == "private":
#                 if protocol == "onebot":
#                     bot_instance = OnebotV11PrivateBot(bot_id, identifier)
#                 elif protocol == "keaimao":
#                     bot_instance = KeaimaoPrivateBot(bot_id, identifier)
#                 # elif protocol == "telegram":
#                 #     bot_instance = TelegramPrivateBot(bot_id, identifier)

#         if not bot_instance:
#             raise EventHandleError(f"未能创建bot实例 {protocol} {mode} {identifier}")

#         instances_dict[key] = bot_instance

#     else:
#         bot_instance = instances_dict[key]

#     return bot_instance
