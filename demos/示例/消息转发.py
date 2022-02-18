class WhateverNameYouWant:
    async def group_message(self, bot: UniversalGroupBot, chain: MessageChain):
        if bot.onebot: # 转发qq消息至微信
            await bot.arbitrary.keaimao.group_message("19521241254@chatroom", *chain.segments)

        if bot.keaimao: # 转发微信消息至qq
            await bot.arbitrary.onebot.group_message("1041902989", *chain.segments)