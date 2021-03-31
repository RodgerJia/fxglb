# -*- coding: utf-8 -*-
"""
Created on Thu Nov 12 16:15:08 2020

@author: zhuzi
"""


import pandas as pd
import pymysql
import numpy as np
from datetime import datetime


def readSql(configDic, sql):
    conn = pymysql.connect(host=configDic['host'], port=configDic['port'], user=configDic['user'],
                           passwd=configDic['password'], db=configDic['db'])
    cursor = conn.cursor()
    data = pd.read_sql(sql, conn, )
    df = pd.DataFrame(data)
    return df


def dailyPnl(productName, project_date, today, netValue):
    dataConfig = {'host': '10.10.9.237', 'port': 3306, 'user': 'root', 'password': '123456', 'db': 'djangotest'}

    # 今日更新的数据，日报数据不回滚，历史申赎的盈亏计在今日。
    sql = "select * from tradeinfo where productName = '" + productName + "' and confirmDate <= '" + str(
        project_date) + "' and date = '" + str(today) + "';"
    trade = readSql(dataConfig, sql).drop('index', axis=1).fillna(0)

    sql = "select * from fundpnlinfo where productName = '" + productName + "' order by date;"
    pnl = readSql(dataConfig, sql).drop('index', axis=1)

    if len(pnl) == 0:
        # 累计申购数量（包括分红再投）
        acBuyAmount = 0
        # 累计赎回数量
        acSellAmount = 0
        # 累计申购金额（申购款以成本计）
        buyCashAmount = 0
        # 累计赎回金额
        sellCashAmount = 0
        # 赎回成本
        sellCost = 0
        # 现金分红
        cashDiv = 0
        # 昨日累计盈亏
        yesCumPnl = 0
    else:
        acBuyAmount = float(pnl.acBuyAmount.iloc[-1])
        acSellAmount = float(pnl.acSellAmount.iloc[-1])
        buyCashAmount = float(pnl.buyCashAmount.iloc[-1])
        sellCashAmount = float(pnl.sellCashAmount.iloc[-1])
        sellCost = float(pnl.sellCost.iloc[-1])
        cashDiv = float(pnl.cashDiv.iloc[-1])
        yesCumPnl = float(pnl.cumPnl.iloc[-1])
    df = pd.DataFrame({'date': project_date, 'productName': productName}, index=[0])
    # 查询申赎表，根据确认日期匹配数据
    if len(trade) != 0:
        trade = trade.sort_values('confirmDate', ascending=True)
        for i in range(len(trade)):
            tradeInfo = trade.iloc[i]
            if tradeInfo.tradeType == '申购':
                acBuyAmount = acBuyAmount + tradeInfo.tradeShare
                buyCashAmount = buyCashAmount + tradeInfo.tradeAmount
            elif tradeInfo.tradeType == '分红再投':
                acBuyAmount = acBuyAmount + tradeInfo.tradeShare
            elif tradeInfo.tradeType == '现金分红':
                cashDiv = cashDiv + tradeInfo.tradeAmount
            elif tradeInfo.tradeType == '赎回':
                acSellAmount = acSellAmount + tradeInfo.tradeShare
                sellCashAmount = sellCashAmount + tradeInfo.tradeAmount
                sellCost = sellCost + tradeInfo.cost

    df['acBuyAmount'] = acBuyAmount
    df['acSellAmount'] = acSellAmount
    df['buyCashAmount'] = buyCashAmount
    df['sellCashAmount'] = sellCashAmount
    df['sellCost'] = sellCost
    df['cashDiv'] = cashDiv

    df['todayNetValue'] = float(netValue)
    df['cumPnl'] = (
                               df.acBuyAmount - df.acSellAmount) * df.todayNetValue - df.buyCashAmount + df.sellCashAmount + df.cashDiv
    df['todayPnl'] = df.cumPnl - yesCumPnl

    sql = "select * from confirmnetvalueinfo where productName = '" + productName + "' and date <= '" + str(
        project_date) + "' order by date;"
    nv = readSql(dataConfig, sql).drop('index', axis=1)

    nvList = []
    retList = []
    for date in nv.date.tolist():
        nvData = nv.loc[nv.date == date]
        if len(nvData) == 1:
            nvList.append(nvData.acNetValue.values[0])
        else:
            nvData = nvData.sort_values('lastUpdateDate', ascending=True)
            nvList.append(nvData.acNetValue.values[0])
        if len(nvList) == 1:
            retList.append(0)
        else:
            retList.append(np.log(nvList[-1] / nvList[-2]))

    avgRet = float(np.mean(retList))
    stdRet = float(np.std(retList))
    df['var'] = float((avgRet - 1.645 * stdRet) * (df.buyCashAmount - df.sellCost) / 10000.)
    return df



