#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import stock


def check(code, start_date=None, end_date=None, frequency='m'):
    if start_date is None or end_date is None:
        year = time.localtime().tm_year
        pre_year = year - 3
        start_date = str(pre_year) + time.strftime("-%m-%d", time.localtime())
        end_date = time.strftime("%Y-%m-%d", time.localtime())

    df = stock.MACD(code, start_date, end_date, frequency).tail(3)

    buy = (df['MACD'][1] < df['MACD'][0]) and (df['MACD'][1] < df['MACD'][2])
    buy2 = (df['MACD'][1] < 0) and (0 < df['MACD'][2])
    sell = (df['MACD'][1] > df['MACD'][0]) and (df['MACD'][1] > df['MACD'][2])

    if buy or buy2:
        return 1
    elif sell:
        return -1
    else:
        return 0


if __name__ == '__main__':
    result = check("sz.002028")
    print(result)
