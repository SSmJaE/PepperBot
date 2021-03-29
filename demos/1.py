import inspect
import sys
from os import path
from time import time

from inflection import humanize

import random

from queue import Queue

BASE_DIR = path.dirname(path.dirname(path.abspath(__file__)))
sys.path.append(BASE_DIR)


from src.main import *

# todo 实现抽象基类，或者模板，或者说ts中的inherit的interface
# 以实现检测子类是否实现了指定的方法，和实例属性


def get_current_function_name():
    return inspect.currentframe().f_back.f_code.co_name


def is_command(): pass

# todo 指令模块，作为与事件监听和出发模块完全解耦的一个工具函数
# 可以放在utils里面，其实就是对字符串的处理


@register(groupId=1041902989)
class WhateverNameYouWant:

    async def before_group_message(*args):
        print(humanize(get_current_function_name()))

    async def group_message(self, bot: GroupMessageBot, chain: MessageChain, sender: Sender):

        if "撤回我" == chain.pure_text:
            await chain.withdraw()

        if "踢出我" == chain.pure_text:
            await sender.kickout()

        # if "禁言我" == chain.pure_text:
        #     await sender.ban(10)

        if chain.regex("请?禁言我?"):
            await sender.ban(10)

        hasFace, face = chain.has_and_last(Face)
        if hasFace:
            await bot.group_msg(face)

        if chain.regex("有人(在|吗|嘛|在吗).?"):
            await bot.group_msg(Text("没人"))

        if chain.any("能", "可以") and chain.any("考试", "测试"):
            await chain.reply(
                Text("支持班级测试，不过题目收录不完整\n"),
                Text("为什么不自己试一试呢？"),
            )

        if chain.any("无", "无法", "不能", "怎么", "没用") and chain.any("时长", "换页"):
            await chain.reply(
                Text("通过左上角的设置按钮开启设置面板，开启刷时长之后保存\n"),
                Text("部分课程可能需要Ctrl + F5，或者重启浏览器才行\n"),
                Text("建议将切换间隔切换至0.2，即12秒，看一下是否正常切换\n"),
                Text("如果还是无法运行，检查下自己使用的是否是最新版本的chrome, temper monkey, 和本脚本"),
            )

        if chain.any("无", "无法", "不能", "怎么", "没用") and chain.any("题", "答案"):
            await chain.reply(
                Text("有些课程只能显示答案，有的课程可以自动作答某些类型的题目\n"),
                Text("比较主流的课程都做了适配，至少可以显示答案\n"),
                Text("一些比较冷门的课程未做适配"),
            )

        if chain.any("怎么", "可以", "能") and chain.any("自动提交"):
            await chain.reply(
                Text("不支持自动提交，也不打算开发此功能，因为需要给每种课程都做适配，很耗时间"),
            )

    async def after_group_message(*args):
        print(humanize(get_current_function_name()))

    async def add_group(self, bot: GroupRequestBot, event):
        print(humanize(get_current_function_name()))

        if "加入我" in event["comment"]:
            await bot.resolve()
        else:
            await bot.reject()


lastTime = None
# messageTimeQueue = Queue(maxsize=3)
messageTimeQueue = []


@register(groupId=1057809143)
class 交流群:

    async def add_group(self, bot: GroupRequestBot, event):
        print(humanize(get_current_function_name()))

        if re.search("(油猴)|(网页)|(temper)|(交流群)|(greasy)|(助手)", event["comment"], re.IGNORECASE):
            await bot.resolve()
        # else:
        #     await bot.reject()

    async def group_message(self, bot: GroupMessageBot, chain: MessageChain, sender: Sender):

        if sender.userId == 2927753279:
            if chain.regex_any("赞助", "赞", "助", "zan", "zhu"):
                await bot.group_msg(Text("不允许直接在群中刷屏索要赞助，想要赞助请私聊"))
                await chain.withdraw()

            else:

                # 两分钟允许发三条消息
                global messageTimeQueue

                currentTime = time()

                if len(messageTimeQueue) == 3:
                    firstTime = messageTimeQueue[0]

                    if (currentTime - firstTime) < 120:
                        await bot.group_msg(Text("机器人发言频率过高，暂时封禁2分钟"))
                        await chain.withdraw()
                        await sender.ban(2)

                    messageTimeQueue.pop(0)

                messageTimeQueue.append(currentTime)

        # hasFace, face = chain.has_and_last(Face)
        # if hasFace:
        #     await bot.group_msg(face)

        if chain.has(Face):
            await bot.group_msg(Face(random.randint(1, 300)))

        if chain.regex("有人(在|吗|嘛|在吗).?"):
            await bot.group_msg(Text("没人"))

        if chain.any("能", "可以") and chain.any("考试", "测试"):
            await chain.reply(
                Text("支持班级测试，不过题目收录不完整\n"),
                Text("为什么不自己试一试呢？"),
            )

        if chain.any("无", "无法", "不能", "怎么", "没用") and chain.any("时长", "换页"):
            await chain.reply(
                Text("通过左上角的设置按钮开启设置面板，开启刷时长之后保存\n"),
                Text("部分课程可能需要Ctrl + F5，或者重启浏览器才行\n"),
                Text("建议将切换间隔切换至0.2，即12秒，看一下是否正常切换\n"),
                Text("如果还是无法运行，检查下自己使用的是否是最新版本的chrome, temper monkey, 和本脚本"),
            )

        if chain.any("无", "无法", "不能", "怎么", "没用") and chain.any("题", "答案"):
            await chain.reply(
                Text("有些课程只能显示答案，有的课程可以自动作答某些类型的题目\n"),
                Text("比较主流的课程都做了适配，至少可以显示答案\n"),
                Text("一些比较冷门的课程未做适配"),
            )

        if chain.any("怎么", "可以", "能") and chain.any("自动提交"):
            await chain.reply(
                Text("不支持自动提交，也不打算开发此功能，因为需要给每种课程都做适配，很耗时间"),
            )


if __name__ == "__main__":
    run(debug=True, port=53521)
