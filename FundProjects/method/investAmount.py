import pandas as pd
import os
import pymysql
from sqlalchemy import create_engine
import numpy as np
from datetime import datetime
def readSql(configDic, sql):

    conn = pymysql.connect(host=configDic['host'], port=configDic['port'], user=configDic['user'],
                           passwd=configDic['password'], db=configDic['db'])
    cursor = conn.cursor()
    data = pd.read_sql(sql, conn, )
    df = pd.DataFrame(data)
    return df


def getInvestAmount(date, product):
    dataConfig = {'host': '10.10.9.237', 'port': 3306, 'user': 'root', 'password': '123456', 'db': 'djangotest'}
    sql = "select * from tradeinfo where productName = '"+product+"' and confirmDate <= '"+date+"';"
    data = readSql(dataConfig, sql)
    investAmount = 0
    buyCashAmount = 0
    if len(data) != 0:
        buyCashAmount = data.loc[data.tradeType == '申购'].tradeAmount.sum()
        sellCost = data.loc[data.tradeType == '赎回'].cost.sum()
        investAmount = buyCashAmount - sellCost
    return buyCashAmount, investAmount

# 多次调用数据库 卡卡卡 替换为下一个方法
# def getInvestAmountList(begDate, endDate, productList):
#     dataConfig = {'host': '127.0.0.1', 'port': 3306, 'user': 'root', 'password': '123456', 'db': 'djangotest'}
#     sql = "select * from fundpnlinfo where date <= '"+endDate+"' and date >= '"+begDate+"';"
#     dateList = list(set(readSql(dataConfig, sql).date.tolist()))
#     dateList.sort()
#     result = []
#     totalResult = []
#     for date in dateList:
#         date = date.strftime("%Y-%m-%d")
#         dicts = {'date': date}
#         totalInvestAmount = 0
#         for product in productList:
#             dic = {'date': date, 'product':product}
#             dic['investAmount'] = getInvestAmount(date, product)
#             result.append(dic)
#             totalInvestAmount = totalInvestAmount + dic['investAmount']
#         dicts['totalInvestAmount'] = totalInvestAmount
#         totalResult.append(dicts)
#     return result, totalResult

# 一次性调出productList对应的数据，根据日期循环加总
def getInvestAmountList(begDate, endDate, productList):
    dataConfig = {'host': '10.10.9.237', 'port': 3306, 'user': 'root', 'password': '123456', 'db': 'djangotest'}
    sql = "select * from fundpnlinfo where date <= '"+endDate+"' and date >= '"+begDate+"';"
    dateList = list(set(readSql(dataConfig, sql).date.tolist()))
    dateList.sort()
    totalResult = []
    sql = "select * from tradeinfo where productName in ("+str(productList)[1:-1]+") and confirmDate <= '"+endDate+"';"
    data = readSql(dataConfig, sql)

    for date in dateList:
        date = date.strftime("%Y-%m-%d")
        dicts = {'date': date}
        investAmount = 0
        dailyData = data.loc[data.confirmDate <= date]
        if len(data) != 0:
            buyCashAmount = dailyData.loc[dailyData.tradeType == '申购'].tradeAmount.sum()
            sellCost = dailyData.loc[dailyData.tradeType == '赎回'].cost.sum()
            investAmount = buyCashAmount - sellCost

        dicts['totalInvestAmount'] = investAmount
        totalResult.append(dicts)
    return totalResult