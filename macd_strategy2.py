#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import stock
import pandas as pd


def buy(code, start_date=None, end_date=None, frequency='m'):
    if start_date is None or end_date is None:
        year = time.localtime().tm_year
        pre_year = year - 3
        start_date = str(pre_year) + time.strftime("-%m-%d", time.localtime())
        end_date = time.strftime("%Y-%m-%d", time.localtime())

    df = stock.MACD(code, start_date, end_date, frequency)
    print(df)

    result = pd.DataFrame(columns=['date', 'buy', 'price'])
    j = 0

    datenumber = int(df.shape[0])
    for i in range(1, datenumber - 1):
        buy = (df['MACD'][i] < df['MACD'][i - 1]) and (df['MACD'][i] < df['MACD'][i + 1])
        buy2 = (df['MACD'][i] < 0) and (0 < df['MACD'][i + 1])
        sell = (df['MACD'][i] > df['MACD'][i - 1]) and (df['MACD'][i] > df['MACD'][i + 1])

        price = round(float(df['close'][i + 1]), 2)

        if buy or buy2:
            result.loc[j] = [df.index[i + 1], 1, price]
            j = j + 1
        elif sell:
            result.loc[j] = [df.index[i + 1], -1, price]
            j = j + 1

    return result


if __name__ == '__main__':
    result = buy("sh.600009", '2014-04-01', '2021-01-01')
    print(result)
    cang = 0
    money = 100000

    size = int(result.shape[0])
    for i in range(0, size):
        if result['buy'][i] > 0:
            price = result['price'][i]
            cang = money // (price * 100)
            money = money - cang * price * 100
        elif cang > 0:
            price = result['price'][i]
            money = money + cang * price * 100
            cang = 0

    print(money + cang * result['price'][size - 1] * 100)
