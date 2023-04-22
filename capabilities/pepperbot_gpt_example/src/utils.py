from devtools import debug
from src.config import gpt_example_setting
from src.models import GPTInfo

from pepperbot import logger
from pepperbot.core.message.chain import MessageChain
from pepperbot.core.message.segment import At, Text
from pepperbot.extensions.command.sender import CommandSender


async def rate_limit(chain: MessageChain, sender: CommandSender):
    """每天仅能调用指定次数，超过次数则返回错误信息

    数据持久化保存至数据库中"""

    gpt_info, created = await GPTInfo.objects.get_or_create(account=chain.user_id)

    logger.info(f"chain.user_id: {chain.user_id}, count: {gpt_info.count}")

    debug(gpt_example_setting)

    max_times = gpt_example_setting.times_per_user.get(sender.user_id)

    if not max_times:
        max_times = gpt_example_setting.times_per_group.get(chain.source_id)

    if not max_times:
        max_times = gpt_example_setting.default_times

    if (
        chain.source_id in gpt_example_setting.super_groups
        or chain.user_id in gpt_example_setting.super_users
    ):
        logger.info("超级用户或超级群组，无次数限制")
        pass

    elif gpt_info.count >= max_times:
        await sender.send_message(
            At(chain.user_id),
            Text("今天已经超过最大调用次数了，明天再来吧\n"),
            Text("每人每天最多调用5次"),
        )

        return False

    gpt_info.count += 1
    await gpt_info.update()

    return True
