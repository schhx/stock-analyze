#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import calendar


def is_last_day_of_month():
    """判断当天是否当月最后一天"""
    # 获取当前年份
    year = datetime.date.today().year
    # 获取当前月份
    month = datetime.date.today().month
    # 获取当前日
    day = datetime.date.today().day
    return day == calendar.monthrange(year, month)[1]


def is_friday():
    """判断是否是周五"""
    return datetime.date.today().weekday() == 4
