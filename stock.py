import baostock as bs
import pandas as pd
import talib as ta


def MACD(code, startdate, enddate, frequency='d'):
    df = get_k_data(code, startdate, enddate, frequency)
    # 获取 diff,dea,hist，它们的数据类似是 tuple，且跟 df 的 date 日期一一对应
    # 记住了 diff,dea,hist 前 33 个为 Nan，所以推荐用于计算的数据量一般为你所求日期之间数据量的3倍
    # 这里计算的 hist 就是 diff-dea,而很多证券商计算的 MACD = hist * 2 = (diff - dea) * 2
    diff, dea, hist = ta.MACD(df['close'].astype(float).values, fastperiod=12, slowperiod=26, signalperiod=9)

    macddf = pd.DataFrame(
        {'open': df['open'].values, 'close': df['close'].values, 'DIFF': diff, 'DEA': dea, 'MACD': hist * 2},
        index=df['date'], columns=['open', 'close', 'DIFF', 'DEA', 'MACD'])
    macddf = macddf.dropna()

    return macddf


def EMA(code, startdate, enddate, frequency='d'):
    df = get_k_data(code, startdate, enddate, frequency)

    EMA12 = ta.EMA(df['close'].astype(float).values, timeperiod=12)  # 调用talib 计算12日移动移动平均线的值
    EMA26 = ta.EMA(df['close'].astype(float).values, timeperiod=26)
    # 获取 diff,dea,hist，它们的数据类似是 tuple，且跟 df 的 date 日期一一对应
    # 记住了 diff,dea,hist 前 33 个为 Nan，所以推荐用于计算的数据量一般为你所求日期之间数据量的3倍
    # 这里计算的 hist 就是 diff-dea,而很多证券商计算的 MACD = hist * 2 = (diff - dea) * 2
    diff, dea, hist = ta.MACD(df['close'].astype(float).values, fastperiod=12, slowperiod=26, signalperiod=9)
    macddf = pd.DataFrame(
        {'DIFF': diff[33:], 'DEA': dea[33:], 'MACD': hist[33:] * 2, 'EMA12': EMA12[33:], 'EMA26': EMA26[33:]},
        index=df['date'][33:], columns=['DIFF', 'DEA', 'MACD', 'EMA12', 'EMA26'])
    return macddf


def get_k_data(code, startdate, enddate, frequency='d'):
    #### 登陆系统 ####
    bs.login()

    if frequency == 'd':
        fields = "date,open,close,tradeStatus"
    else:
        fields = "date,open,close"

    # 获取股票日 K 线数据
    rs = bs.query_history_k_data(code,
                                 fields,
                                 start_date=startdate,
                                 end_date=enddate,
                                 frequency=frequency, adjustflag="2")

    # 打印结果集
    result_list = []
    while (rs.error_code == '0') & rs.next():
        # 获取一条记录，将记录合并在一起
        result_list.append(rs.get_row_data())
    df = pd.DataFrame(result_list, columns=rs.fields)

    bs.logout()

    # 剔除停盘数据
    if frequency == 'd':
        return df[df['tradeStatus'] == '1']
    else:
        return df


if __name__ == '__main__':
    code = 'sh.600009'
    startdate = '2016-05-01'
    enddate = '2019-05-01'
    frequency = 'm'
    MACD(code, startdate, enddate, frequency)
