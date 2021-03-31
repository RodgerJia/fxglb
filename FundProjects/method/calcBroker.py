# -*- coding: utf-8 -*-
"""
Created on Thu Nov 26 11:29:25 2020

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


def calc(begDate, endDate):
    dataConfig = {'host': '10.10.9.237', 'port': 3306, 'user': 'root', 'password': '123456', 'db': 'djangotest'}
    sql = "select distinct manager from fundbasicinfo;"
    managerList = readSql(dataConfig, sql).manager.tolist()

    dailyDf = pd.DataFrame()
    result = []
    for manager in managerList:
        sql = "select * from brokagebasicinfo where manager = '"+manager+"' and date <= '"+endDate+"' and date >= '"+begDate+"';"
        data = readSql(dataConfig, sql).sort_values('date', ascending=True)
        account = list(set(data.acId))
        for acc in account:
            managerDict = {}
            managerDict['begDate'] = begDate
            managerDict['endDate'] = endDate
            managerDict['manager'] = manager
            managerDict['acc'] = acc
            #期末留存
            accData = data.loc[data.acId == acc]
            intBegDate = accData.begDate.iloc[0]
            
            sql = "select * from brokagebasicinfo where acId = '"+acc+"' and date < '"+intBegDate+"' order by date desc limit 1;"
            hisData = readSql(dataConfig, sql)
            if len(hisData) == 0:
                hisData = 0
            else:
                hisData = float(hisData.endEquity.iloc[0])
            managerDict['his'] = hisData
            #
            if intBegDate > begDate:
                #利息收入早于查询日，直接加总, 利息收入日期开始
                accData = accData.loc[accData.date >= intBegDate]
            dailyDf = dailyDf.append(accData)
            #净利息收入
            netIntTotal = 0
            for num in accData.netIntIncome.tolist():
                netIntTotal = netIntTotal + float(num)
            netIntTotal = round(netIntTotal,2)
            #净留存
            netLeftTotal = 0
            for num in accData.netLeft.tolist():
                netLeftTotal = netLeftTotal + float(num)
            netLeftTotal = round(netLeftTotal,2)    
            #经纪收入
            broIncome = round(netIntTotal + netLeftTotal,2)
            
            #期末权益
            if len(accData) == 0:
                endEquity = 0.
            else:
                endEquity = float(accData.endEquity.iloc[-1])
            
            #日均权益（德索数据为字符串格式）
            endEquityTotal = 0
            maxEquity = 0
            for num in accData.endEquity.tolist():
                endEquityTotal = endEquityTotal + float(num)
                if float(num) > maxEquity:
                    maxEquity = float(num)

            if len(accData) == 0:
                avgEquity = 0
            else:
                avgEquity = round(endEquityTotal/len(accData.endEquity.tolist()),2)



            managerDict['netInt'] = netIntTotal
            managerDict['netLeft'] = netLeftTotal
            managerDict['broIncome'] = broIncome
            managerDict['endEquity'] = endEquity
            managerDict['avgEquity'] = avgEquity
            managerDict['maxEquity'] = maxEquity
            
            result.append(managerDict)
            # managerResult = pd.DataFrame(result)
    return result,dailyDf


def getDailyDf(begDate, endDate):
    dataConfig = {'host': '10.10.9.237', 'port': 3306, 'user': 'root', 'password': '123456', 'db': 'djangotest'}
    sql = "select distinct manager from fundbasicinfo;"
    managerList = readSql(dataConfig, sql).manager.tolist()

    dailyDf = pd.DataFrame()
    for manager in managerList:
        sql = "select * from brokagebasicinfo where manager = '" + manager + "' and date <= '" + endDate + "' and date >= '" + begDate + "';"
        data = readSql(dataConfig, sql).sort_values('date', ascending=True)
        account = list(set(data.acId))
        for acc in account:
            # 期末留存
            accData = data.loc[data.acId == acc]
            intBegDate = accData.begDate.iloc[0]
            if intBegDate > begDate:
                # 利息收入早于查询日，直接加总, 利息收入日期开始
                accData = accData.loc[accData.date >= intBegDate]
            dailyDf = dailyDf.append(accData)
    return dailyDf
