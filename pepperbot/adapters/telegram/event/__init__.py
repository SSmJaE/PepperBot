# https://www.kancloud.cn/yangtaott/dsaw/1179271


class TelegramMetaEvent:
    raw_update = "raw_update"


class TelegramCommonEvent:
    chosen_inline_result = "chosen_inline_result"
    callback_query = "callback_query"
    inline_query = "inline_query"
    edited_message = "edited_message"


class TelegramGroupEvent:
    group_message = "group_message"


class TelegramPrivateEvent:
    private_message = "private_message"
