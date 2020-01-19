#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import stock


def pre_buy(code, start_date=None, end_date=None):
    if start_date is None or end_date is None:
        year = time.localtime().tm_year
        pre_year = year - 3
        start_date = str(pre_year) + time.strftime("-%m-%d", time.localtime())
        end_date = time.strftime("%Y-%m-%d", time.localtime())

    macddf = stock.MACD(code, start_date, end_date, 'm')
    print(macddf)

    datenumber = int(macddf.shape[0])
    for i in range(1, datenumber - 1):
        condition = macddf['MACD'][i] < 0 and macddf['MACD'][i + 1] > 0
        condition2 = (macddf['MACD'][i] > 0) and (macddf['MACD'][i] < macddf['MACD'][i - 1]) and (
                macddf['MACD'][i] < macddf['MACD'][i + 1])
        condition3 = (macddf['MACD'][i + 1] < macddf['DIFF'][i + 1]) or (macddf['MACD'][i + 1] < macddf['EDA'][i + 1])
        # condition = (macddf.iloc[i, 2] < 0) and (macddf.iloc[i + 1, 2] > 0)
        # condition2 = (macddf.iloc[i, 2] > 0) and (macddf.iloc[i, 2] < macddf.iloc[i - 1, 2]) and (
        #         macddf.iloc[i + 1, 2] > macddf.iloc[i, 2])
        # condition3 = (macddf.iloc[i + 1, 2] < macddf.iloc[i + 1, 0]) or (macddf.iloc[i + 1, 2] < macddf.iloc[i + 1, 1])

        if (condition or condition2) and condition3:
            print("状态A:" + macddf.index[i + 1])


if __name__ == '__main__':
    pre_buy("sh.600009", '2015-03-01', '2019-05-01')
