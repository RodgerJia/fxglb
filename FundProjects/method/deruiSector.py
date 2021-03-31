# -*- coding: utf-8 -*-
"""
Created on Mon Jul 13 17:24:59 2020

@author: zhuzi
"""

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


def getData(date):
    year = date[:4] + '0101'
    dataConfig = {'host': '10.10.9.237', 'port': 3306, 'user': 'root', 'password': '123456', 'db': 'djangotest'}
    sql = "select * from deruisectordata where date >= '" + year + "' and date <= '" + date + "' order by date;"
    data = readSql(dataConfig, sql)
    return data

# 回撤开始日期、回撤结束日期、开始回撤时盈亏、限额、最大回撤
def maxdrawdown(df):
    data = df.pnl.tolist()[1:]
    index_j = np.argmax(np.maximum.accumulate(data) - data)  # 结束位置
    endDate = df.iloc[index_j].date
    if len(data[:index_j]) == 0:
        index_i = index_j
        begDate = endDate
    else:
        index_i = np.argmax(data[:index_j])  # 开始位置
        begDate = df.iloc[index_i].date
    d = data[index_j] - data[index_i]  # 最大回撤
    begCumPnl = df.iloc[index_i].pnl
    limit = max(1000, df.iloc[index_i].pnl * 0.2)
    return begDate, endDate, begCumPnl, limit, d


def total(data):
    totalDf = pd.DataFrame()
    totalDf['date'] = data.date
    totalDf['pnl'] = data.totalPnl
    totalDf['cashDelta'] = data.totalCashDelta
    totalDf['var'] = data.totalVar
    totalDf['stressLoss'] = data.totalLoss
    begDate, endDate, begCumPnl, limit, d = maxdrawdown(totalDf)
    return begDate, endDate, begCumPnl, limit, d, totalDf


def omm(data):
    ommDf = pd.DataFrame()
    ommDf['date'] = data.date
    ommDf['amt'] = data.ommAmt
    ommDf['pnl'] = data.ommPnl
    ommDf['cashDelta'] = data.ommCashDelta
    ommDf['var'] = data.ommVar
    begDate, endDate, begCumPnl, limit, d = maxdrawdown(ommDf)
    return begDate, endDate, begCumPnl, limit, d, ommDf

def otc(data):
    otcDf = pd.DataFrame()
    otcDf['date'] = data.date
    otcDf['amt'] = data.otcAmt
    otcDf['pnl'] = data.otcPnl
    otcDf['cashDelta'] = data.otcCashDelta
    otcDf['var'] = data.otcVar
    begDate, endDate, begCumPnl, limit, d = maxdrawdown(otcDf)
    return begDate, endDate, begCumPnl, limit, d, otcDf

def c(data):
    cDf = pd.DataFrame()
    cDf['date'] = data.date
    cDf['amt'] = data.cAmt
    cDf['pnl'] = data.cPnl
    cDf['cashDelta'] = data.cCashDelta
    cDf['var'] = data.cVar
    begDate, endDate, begCumPnl, limit, d = maxdrawdown(cDf)
    return begDate, endDate, begCumPnl, limit, d, cDf

def sigma(data):
    sigmaDf = pd.DataFrame()
    sigmaDf['date'] = data.date
    sigmaDf['amt'] = data.sigmaAmt
    sigmaDf['pnl'] = data.sigmaPnl
    sigmaDf['cashDelta'] = data.sigmaCashDelta
    sigmaDf['var'] = data.sigmaVar
    begDate, endDate, begCumPnl, limit, d = maxdrawdown(sigmaDf)
    return begDate, endDate, begCumPnl, limit, d, sigmaDf

