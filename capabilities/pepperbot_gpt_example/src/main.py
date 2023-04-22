from typing import Any, Dict, List

from apscheduler.triggers.cron import CronTrigger
from httpx import AsyncClient
from src.config import gpt_example_setting
from src.models import GPTInfo
from src.utils import rate_limit

from pepperbot import async_scheduler, logger
from pepperbot.core.message.chain import MessageChain
from pepperbot.core.message.segment import At, Text
from pepperbot.core.route import available
from pepperbot.extensions.command.sender import CommandSender


async def gpt_proxy_by_token(messages: List[Dict], token: str, proxy_token: str) -> str:
    async with AsyncClient(timeout=60) as client:
        response = await client.post(
            "http://45.63.82.234/gpt",
            json={
                "proxy_token": proxy_token,
                "token": token,
                "path": "v1/chat/completions",
                "data": {
                    "model": "gpt-3.5-turbo",
                    "max_tokens": 500,
                    "messages": messages,
                },
            },
        )

        try:
            completion = response.json()["data"]["choices"][0]["message"]["content"]

            return completion
        except KeyError:
            logger.error(response.json())
            raise Exception("gpt返回数据格式错误")


class GPTExample:
    @available(rate_limit)
    async def initial(
        self, sender: CommandSender, chain: MessageChain, config: Any, context: dict
    ):
        context.setdefault("history", [])

        # logger.info(chain.pure_text)
        without_prefix = chain.pure_text.replace("/gpt", "").strip()
        context["history"].append({"role": "user", "content": without_prefix})

        if gpt_example_setting.token and gpt_example_setting.proxy_token:
            logger.info("将使用代理，进行GPT查询")
            completion = await gpt_proxy_by_token(
                context["history"],
                gpt_example_setting.token,
                gpt_example_setting.proxy_token,
            )

        elif config.proxy_call:
            logger.info("通过自己实现的方法，进行GPT查询")
            completion = await config.proxy_call(context["history"])

        else:
            logger.error("未设置查询方式，无法进行GPT查询")
            return None

        context["history"].append({"role": "assistant", "content": completion})

        await sender.send_message(
            At(chain.user_id),
            Text(completion),
        )

        return self.initial

    async def exit(self, sender: CommandSender):
        await sender.send_message(
            At(sender.user_id),
            Text("用户主动退出\n"),
            Text("解答完成，欢迎再来😀\n"),
            Text("本机器人基于PepperBot，https://github.com/SSmJaE/PepperBot"),
        )

    async def timeout(self, sender: CommandSender):
        await sender.send_message(
            At(sender.user_id),
            Text("用户超时未响应，自动退出会话\n"),
            Text("解答完成，欢迎再来😀\n"),
            Text("本机器人基于PepperBot，https://github.com/SSmJaE/PepperBot"),
        )

    async def cleanup(self, sender: CommandSender):
        pass


async def reset_gpt_count():
    await GPTInfo.objects.update(each=True, count=0)


async_scheduler.add_job(reset_gpt_count, CronTrigger(hour="2"))
