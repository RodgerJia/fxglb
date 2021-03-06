# -*- coding: utf-8 -*-
"""
Created on Thu Nov 12 16:15:08 2020

@author: zhuzi
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Jun  1 10:48:15 2020

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

def begData(productName, begDate):
    dataConfig = {'host': '10.10.9.237', 'port': 3306, 'user': 'root', 'password': '123456', 'db': 'djangotest'}
    sql = "select * from tradeinfo where productName = '" + productName + "' and confirmDate < '" + str(
        begDate) + "' order by confirmDate;"
    trade = readSql(dataConfig, sql).drop('index', axis=1).fillna(0)

    sql = "select date, netValue from confirmNetValueInfo where productName = '" + productName + "'and date < '" + str(
        begDate) + "' order by date desc limit 1;"
    begNetValue = readSql(dataConfig, sql).netValue
    if len(begNetValue) == 0:
        nvBegDate = ''
    else:
        nvBegDate = readSql(dataConfig, sql).date.values[0]
    return trade, begNetValue, nvBegDate

def endData(productName, endDate):
    dataConfig = {'host': '10.10.9.237', 'port': 3306, 'user': 'root', 'password': '123456', 'db': 'djangotest'}
    sql = "select * from tradeinfo where productName = '" + productName + "' and confirmDate <= '" + str(
        endDate) + "' order by confirmDate;"
    trade = readSql(dataConfig, sql).drop('index', axis=1).fillna(0)

    sql = "select date, netValue from confirmNetValueInfo where productName = '" + productName + "'and date <= '" + str(
        endDate) + "' order by date desc limit 1;"
    endNetValue = readSql(dataConfig, sql).netValue
    if len(endNetValue) == 0:
        nvEndDate = ''
    else:
        nvEndDate = readSql(dataConfig, sql).date.values[0]
    return trade, endNetValue, nvEndDate

def calPnl(date, trade, netValue, nvDate):
    #??????????????????????????????????????????
    if len(trade) == 0:
        pnl = 0.
        return date, pnl

    #????????????????????????????????????????????????????????????????????????
    nv = trade.iloc[-1].unitNet
    date = trade.iloc[-1].confirmDate

    #??????????????????????????????????????????????????????
    if len(netValue) != 0 and nvDate >= date:
        nv = netValue.values[0]
        date = nvDate

    # ??????????????????????????????????????????
    acBuyAmount = 0
    # ??????????????????
    acSellAmount = 0
    # ?????????????????????????????????????????????
    buyCashAmount = 0
    # ??????????????????
    sellCashAmount = 0
    # ????????????
    sellCost = 0
    # ????????????
    cashDiv = 0

    # ????????????????????????????????????????????????
    if len(trade) != 0:
        trade = trade.sort_values('confirmDate', ascending=True)
        for i in range(len(trade)):
            tradeInfo = trade.iloc[i]
            if tradeInfo.tradeType == '??????':
                acBuyAmount = acBuyAmount + tradeInfo.tradeShare
                buyCashAmount = buyCashAmount + tradeInfo.tradeAmount
            elif tradeInfo.tradeType == '????????????':
                acBuyAmount = acBuyAmount + tradeInfo.tradeShare
            elif tradeInfo.tradeType == '????????????':
                cashDiv = cashDiv + tradeInfo.tradeAmount
            elif tradeInfo.tradeType == '??????':
                acSellAmount = acSellAmount + tradeInfo.tradeShare
                sellCashAmount = sellCashAmount + tradeInfo.tradeAmount
                sellCost = sellCost + tradeInfo.cost


    pnl = (acBuyAmount - acSellAmount) * nv - buyCashAmount + sellCashAmount + cashDiv
    return date, pnl

def durPnl(productName, begDate, endDate):
    if begDate == '':
        begPnl = 0
    else:
        begTrade, begNetValue, nvBegDate = begData(productName, begDate)
        begDate,begPnl = calPnl(begDate, begTrade, begNetValue, nvBegDate)

    endTrade, endNetValue, nvEndDate = endData(productName, endDate)
    endDate, endPnl = calPnl(endDate, endTrade, endNetValue, nvEndDate)

    pnl = endPnl - begPnl
    if type(begDate) != str:
        if type(begDate) == np.datetime64:
            begDate = np.datetime_as_string(begDate, unit='D')
        else:
            begDate = begDate.strftime("%Y-%m-%d")
    if type(endDate) != str:
        if type(endDate) == np.datetime64:
            endDate = np.datetime_as_string(endDate, unit='D')
        else:
            endDate = endDate.strftime("%Y-%m-%d")
    return begDate,endDate,pnl

def allPnl(productName, begDate, endDate):
    year = str(datetime.strptime(endDate, "%Y-%m-%d").year) + '0101'
    begTrade, begNetValue, nvBegDate = begData(productName, begDate)
    begDate,begPnl = calPnl(begDate, begTrade, begNetValue, nvBegDate)

    endTrade, endNetValue, nvEndDate = endData(productName, endDate)
    endDate, endPnl = calPnl(endDate, endTrade, endNetValue, nvEndDate)

    yearTrade, yearNetValue, nvYearDate = begData(productName, year)
    yearDate,yearPnl = calPnl(year, yearTrade, yearNetValue, nvYearDate)

    durPnl = endPnl - begPnl
    yearCumPnl = endPnl - yearPnl
    cumPnl = endPnl
    if type(begDate) != str:
        if type(begDate) == np.datetime64:
            begDate = np.datetime_as_string(begDate, unit='D')
        else:
            begDate = begDate.strftime("%Y-%m-%d")
    if type(endDate) != str:
        if type(endDate) == np.datetime64:
            endDate = np.datetime_as_string(endDate, unit='D')
        else:
            endDate = endDate.strftime("%Y-%m-%d")
    return begDate,endDate,durPnl,yearCumPnl,cumPnl

