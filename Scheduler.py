#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time

from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.schedulers.background import BackgroundScheduler

# 创建定时任务的调度器对象
scheduler = BackgroundScheduler()
# 创建执行器
executors = {
    'default': ThreadPoolExecutor(5),
}


# 定义定时任务
def my_job():
    print(time.localtime())


# 向调度器中添加定时任务
scheduler.add_job(my_job, 'cron', second='0/10')

# 启动定时任务调度器工作
scheduler.start()

input()