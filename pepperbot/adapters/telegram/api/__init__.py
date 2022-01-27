from pepperbot.store.meta import get_telegram_caller
from pepperbot.types import BaseBot


class TelegramGroupApi(BaseBot):
    def __init__(self, bot_id: str, group_id: str):
        self.bot_id = bot_id
        self.group_id = group_id
        self.api_caller = get_telegram_caller()
