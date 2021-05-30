"""
直接使用ActionChain，结合apscheduler实现定时异步任务
"""

import asyncio
import datetime as dt
import logging
from datetime import datetime

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from pepperbot.action import *
from pepperbot.action.chain import *
from pydantic import BaseModel

logging.basicConfig(level=logging.DEBUG)

CONFIG = {
    # 教学周，设置哪一周为第0周
    "zeroWeek": dt.date(2021, 5, 31).isocalendar()[1]
    - 13
}


class MyBaseModel(BaseModel):
    def __hash__(self):
        return hash((type(self),) + tuple(self.__dict__.values()))


class Course(MyBaseModel):
    name: str
    weekday: int  # 从1开始
    classroom: str
    startHour: int
    startMinute: int
    endHour: int = 0
    endMinute: int = 0

    # 单双周/或者直接设置有效周，一个列表
    # 为列表时，从1开始，1为第一周
    weeks: Union[List[int], Literal["all", "odd", "even"]] = "all"


courses: List[Course] = [
    Course(
        name="诊断学Ⅱ",
        classroom="2111",
        weekday=1,
        startHour=8,
        startMinute=0,
        endHour=9,
        endMinute=20,
    ),
    Course(
        name="预防医学实验",
        classroom=" ",
        weekday=1,
        startHour=9,
        startMinute=40,
        endHour=12,
        endMinute=00,
    ),
    Course(
        name="诊断学Ⅱ实验",
        classroom=" ",
        weekday=1,
        startHour=15,
        startMinute=00,
        endHour=18,
        endMinute=10,
        weeks=[13, 14, 15, 16],
    ),
]


flags = {}

chain = ActionChain()
group = chain.select_group(1041902989)


async def main():

    today = datetime.now()

    currentWeek = today.isocalendar()[1] - CONFIG["zeroWeek"]
    # weekday = today.weekday() + 1
    weekday = 1

    for course in courses:
        if isinstance(course.weeks, list):
            if not currentWeek in course.weeks:
                logging.info("非本周课程")
                continue
        else:
            if course.weeks == "all":
                pass

            elif course.weeks == "odd":
                if not currentWeek % 2 == 1:
                    logging.info("非单周课程")
                    continue

            elif course.weeks == "even":
                if not currentWeek % 2 == 0:
                    logging.info("非双周课程")
                    continue

        if course.weekday == weekday:
            # currentMinutes = today.hour * 60 + today.minute
            currentMinutes = 7 * 60 + 50

            courseStartMinutes = course.startHour * 60 + course.startMinute

            if not flags.get(course):
                flags[course] = False

            if not flags[course]:
                if courseStartMinutes - currentMinutes < 30:
                    await group.send_message(
                        Text(
                            f"{course.name}将于{course.startHour:02}:{course.startMinute:02}至"
                            + f"{course.endHour:02}:{course.endMinute:02}在{course.classroom}上课"
                        )
                    )

                    flags[course] = True

        else:
            if flags.get(course):
                del flags[course]


scheduler = AsyncIOScheduler()
scheduler.add_job(main, IntervalTrigger(seconds=10))
scheduler.start()


try:
    asyncio.get_event_loop().run_forever()
except (KeyboardInterrupt, SystemExit):
    pass
