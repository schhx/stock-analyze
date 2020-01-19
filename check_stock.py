#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time

import pandas as pd
import stock


def dispatch(row):
    if 'watch' == row['status']:
        return handle_watch(row)
    elif 'pre_buy' == row['status']:
        return handle_pre_buy(row)
    elif 'buy' == row['status']:
        return handle_buy(row)


def handle_watch(row):
    status = row['status']
    if watch_to_pre_buy(row):
        status = 'pre_buy'
    return status


def handle_pre_buy(row):
    status = row['status']
    if pre_buy_to_buy(row):
        status = 'buy'
    return status


def handle_buy(row):
    status = row['status']
    if buy_to_watch(row):
        status = 'watch'
    return status


def watch_to_pre_buy(row):
    year = time.localtime().tm_year
    pre_year = year - 3
    start_date = str(pre_year) + time.strftime("-%m-%d", time.localtime())
    end_date = time.strftime("%Y-%m-%d", time.localtime())

    df = stock.MACD(row['code'], start_date, end_date, 'm').tail(3)

    condition = (df['MACD'][1] < df['MACD'][0]) and (df['MACD'][1] < df['MACD'][2])
    condition2 = (df['MACD'][1] < 0) and (0 < df['MACD'][2])
    return condition or condition2


def pre_buy_to_buy(row):
    if row['price'] <= 0:
        return False

    year = time.localtime().tm_year
    pre_year = year - 1
    start_date = str(pre_year) + time.strftime("-%m-%d", time.localtime())
    end_date = time.strftime("%Y-%m-%d", time.localtime())
    df = stock.MACD(row['code'], start_date, end_date, 'd').tail(1)
    return float(df['close']) > row['price']


def buy_to_watch(row):
    year = time.localtime().tm_year
    pre_year = year - 1
    start_date = str(pre_year) + time.strftime("-%m-%d", time.localtime())
    end_date = time.strftime("%Y-%m-%d", time.localtime())
    df = stock.MACD(row['code'], start_date, end_date, 'w').tail(1)
    return float(df['close']) < row['price']


if __name__ == '__main__':
    stock_list = pd.read_csv("stock_list.csv", converters={'price': float})
    stock_list['status'] = stock_list.apply(lambda row: dispatch(row), axis=1)
    stock_list.to_csv("stock_list.csv", index=False)
    print(stock_list)
