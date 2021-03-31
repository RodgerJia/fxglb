# -*- coding: utf-8 -*-

"""
@author: zzj

@contact: QQ:10996784

@Created on: 2020/10/13 007 11:28
"""

from django.http import JsonResponse

from FundProjects.models import fundBasicInfo, confirmNetValueInfo
from datetime import datetime
import pandas as pd

import FundProjects.method.fundpnlConfirm as fundpnlConfirm
import FundProjects.method.calcBroker as calcBroker
import FundProjects.method.investAmount as investAmount

hisSpecialProductList = ['钢铁1号', '星光璀璨1号', '和誉3号', '银河期货大宗商品1号', '权银河旗舰3/4号', '银河人保安心盛世1号', '融宝16号', '华澳臻智稳健1期',
                         '权银河恒星1号']
nonInvestProductList = ['权银河旗舰3/4号', '银河人保安心盛世1号', '融宝16号', '华澳臻智稳健1期', '权银河恒星1号']


from sqlalchemy import create_engine

# 上传经纪业务数据
def postBrokerData(request):
    """批量导入数据"""
    # if request.method == "POST":
    f = request.FILES.get('file')
    data = pd.read_excel(f)
    data.columns = data.iloc[0]
    data = data.drop(0, axis=0)
    data = data.drop('报表开始日期', axis=1)
    data = data.drop('报表结束日期', axis=1)

    data.columns = ['date', 'acId', 'investName', 'manager', 'left', 'netLeft', 'begDate', 'endDate', 'intIncome',
                    'intBack', 'netIntIncome', 'tradeValue', 'tradeAmount', 'endPos', 'endEquity', 'avgEquity']

    # data['actualNetLeft'] = data['left'] - data['tradeValue'] * 6 / 100000000

    engine = create_engine("mysql+pymysql://root:123456@localhost/djangotest", encoding="utf8")
    pd.io.sql.to_sql(data.reset_index(drop=True), 'brokagebasicinfo', engine, schema='djangotest', if_exists='replace')

    return JsonResponse({
        "code": 0,
        "msg": "成功",
        "data": {}
    })


# 计算经纪业务数据
def getBrokerData(request):
    results = {
        "pnlTotal": 0,
        "pnlTableInfo": [],
    }
    params = request.GET
    dateRange = params.get("date")  # 前端传入的时间
    investPurposeCheck = params.get("investPurpose")  # 前端传入的参数：投资目的
    sectorCheck = params.get("sector")  # 前端传入的参数：负责部门
    managerCheck = params.get("manager")  # 前端传入的参数：管理人
    strategyCheck = params.get("strategy")
    # 对传参进行处理，非空值
    if investPurposeCheck == '' or investPurposeCheck is None:
        investPurposeCheck = '全部'
    if sectorCheck == '' or sectorCheck is None:
        sectorCheck = '全部'
    if managerCheck == '' or managerCheck is None:
        managerCheck = '全部'
    if strategyCheck == '' or strategyCheck is None:
        strategyCheck = '全部'
    if dateRange == '' or dateRange is None:
        return JsonResponse({
            "code": 0,
            "msg": "成功",
            "data": results,
            "total": 0
        })
    else:
        begDate = dateRange[:10]
        endDate = dateRange[-10:]

    print(investPurposeCheck, sectorCheck, managerCheck, begDate, endDate)

    # 计算经纪业务数据
    fundBrokeInfo, dailyDf = calcBroker.calc(begDate, endDate)

    fundBrokeDf = pd.DataFrame(fundBrokeInfo)
    pnlTableInfo = []
    pnlTableList = []
    queryset = fundBasicInfo.objects.filter(confirmDate2__lte=endDate).values()
    if investPurposeCheck != '全部':
        queryset = queryset.filter(investPurpose=investPurposeCheck).values()
    if sectorCheck != '全部':
        queryset = queryset.filter(sector=sectorCheck).values()
    if managerCheck != '全部':
        queryset = queryset.filter(manager=managerCheck).values()
    if strategyCheck != '全部':
        queryset = queryset.filter(strategy=strategyCheck).values()
    for query in queryset:
        dicts = {}
        productName = query.get('productName')
        manager = query.get('manager')
        dicts['manager'] = manager
        dicts['productName'] = query.get('productName')
        dicts['sector'] = query.get('sector')
        dicts['investPurpose'] = query.get('investPurpose')
        confirmDate2 = query.get('confirmDate2')
        dicts['productType1'] = query.get('productType1')
        dicts['strategy'] = query.get('strategy')

        buyCashAmountResult, investAmountResult = investAmount.getInvestAmount(endDate, productName)
        dicts['buyCashAmount'] = buyCashAmountResult
        dicts['cost'] = investAmountResult
        nv = confirmNetValueInfo.objects.filter(productName=productName, date__lte=endDate).order_by("-date").first()

        if productName not in nonInvestProductList:
            begDate_dur, endDate_dur, durPnl, yearPnl, cumPnl = fundpnlConfirm.allPnl(productName, begDate, endDate)
            if endDate_dur <= begDate:
                dicts['status'] = '早于期间结束'
                dicts['todayNetValue'] = ''
            else:
                if investAmountResult == 0:
                    dicts['status'] = '已结束'
                    dicts['todayNetValue'] = ''
                    if nv is None and productName not in hisSpecialProductList:
                        dicts['status'] = '已审批未投'
                else:
                    dicts['status'] = '在投'
                    if nv is None:
                        dicts['todayNetValue'] = '无净值数据'
                    else:
                        dicts['todayNetValue'] = nv.netValue
            dicts['yearPnl'] = round(yearPnl, 2)
            dicts['cumPnl'] = round(cumPnl, 2)
            dicts['durPnl'] = round(durPnl, 2)
            dicts['date'] = endDate_dur
            dicts['begDate'] = begDate_dur
        else:
            dicts['status'] = '取消投资'
            dicts['todayNetValue'] = ''
            dicts['yearPnl'] = 0
            dicts['cumPnl'] = 0
            dicts['durPnl'] = 0
            dicts['date'] = confirmDate2
            dicts['begDate'] = confirmDate2


        if manager not in pnlTableList:
            pnlTableList.append(manager)
            if len(fundBrokeDf) == 0:
                dicts['account'] = ''
                dicts['his'] = ''
                dicts['netInt'] = ''
                dicts['netLeft'] = ''
                dicts['brokerIncome'] = ''
                dicts['endEquity'] = ''
                dicts['avgEquity'] = ''
                dicts['maxEquity'] = ''
            else:
                # df.loc 失效?
                def findManager(df, value):
                    dfNew = pd.DataFrame()
                    for i in range(len(df)):
                        df1 = df.iloc[i]
                        manager = df1.manager
                        if manager == value:
                            dfNew = dfNew.append(df1)
                    return dfNew

                managerDf = findManager(fundBrokeDf, manager)
                if len(managerDf) == 0:
                    dicts['account'] = ''
                    dicts['his'] = ''
                    dicts['netInt'] = ''
                    dicts['netLeft'] = ''
                    dicts['brokerIncome'] = ''
                    dicts['endEquity'] = ''
                    dicts['avgEquity'] = ''
                    dicts['maxEquity'] = ''
                else:
                    dicts['account'] = str(managerDf.acc.tolist())[1:-1]
                    dicts['his'] = round(managerDf.his.sum(), 2)
                    dicts['netInt'] = round(managerDf.netInt.sum(), 2)
                    dicts['netLeft'] = round(managerDf.netLeft.sum(), 2)
                    dicts['brokerIncome'] = round(managerDf.broIncome.sum(), 2)
                    dicts['endEquity'] = round(managerDf.endEquity.sum(), 2)
                    dicts['avgEquity'] = round(managerDf.avgEquity.sum(), 2)
                    dicts['maxEquity'] = round(managerDf.maxEquity.sum(), 2)

        dicts['demo'] = ''
        pnlTableInfo.append(dicts)

    dicts = {}
    totalTableInfo = []
    df = pd.DataFrame(pnlTableInfo)
    df = df.replace('', 0)
    df = df.fillna(0)
    dicts['begDate'] = begDate
    dicts['date'] = endDate
    dicts['investPurpose'] = investPurposeCheck
    if len(df) == 0:
        dicts['manager'] = '0'
        dicts['productName'] = '0'
        dicts['cost'] = '0'
        dicts['durPnl'] = '0'
        dicts['yearPnl'] = '0'
        dicts['cumPnl'] = '0'
        dicts['his'] = '0'
        dicts['netInt'] = '0'
        dicts['netLeft'] = '0'
        dicts['brokerIncome'] = '0'
        dicts['endEquity'] = '0'
        dicts['avgEquity'] = '0'
        dicts['maxEquity'] = '0'
    else:
        dfFilter = df.loc[df.status != '早于期间结束']
        dfFilter = dfFilter.loc[dfFilter.status != '取消投资']
        dicts['manager'] = str(len(list(set(dfFilter.loc[dfFilter.status != '已审批未投'].manager.tolist()))))
        productList = list(set(dfFilter.loc[dfFilter.status != '已审批未投'].productName.tolist()))
        dicts['productName'] = str(len(productList))
        dicts['manager2'] = str(len(list(set(dfFilter.loc[dfFilter.status == '在投'].manager.tolist()))))
        productList2 = list(set(dfFilter.loc[dfFilter.status == '在投'].productName.tolist()))
        dicts['productName2'] = str(len(productList2))

        dicts['buyCashAmount'] = str(round(dfFilter.buyCashAmount.sum()/100000000, 2))
        dicts['cost'] = str(round(dfFilter.cost.sum()/100000000, 2))
        dicts['durPnl'] = str(round(df.durPnl.sum()/10000, 2))
        dicts['yearPnl'] = str(round(df.yearPnl.sum()/10000, 2))
        dicts['cumPnl'] = str(round(df.cumPnl.sum()/10000, 2))
        dicts['his'] = str(round(df.his.sum()/10000, 2))
        dicts['netInt'] = str(round(df.netInt.sum()/10000, 2))
        dicts['netLeft'] = str(round(df.netLeft.sum()/10000, 2))
        dicts['brokerIncome'] = str(round(df.brokerIncome.sum()/10000, 2))
        dicts['endEquity'] = str(round(df.endEquity.sum()/10000, 2))
        dicts['avgEquity'] = str(round(df.avgEquity.sum()/10000, 2))
        dicts['maxEquity'] = str(round(df.maxEquity.sum()/100000000, 2))

    totalTableInfo.append(dicts)

    results['fundBrokeInfo'] = fundBrokeInfo
    results['pnlTableInfo'] = pnlTableInfo
    results['totalTableInfo'] = totalTableInfo
    return JsonResponse({
        "code": 0,
        "msg": "成功",
        "data": results
    })


# 计算经纪业务数据分布图，时间序列
def getBrokerDataSeries(request):
    results = {
        "pnlTotal": 0,
        "pnlTableInfo": [],
    }
    params = request.GET
    dateRange = params.get("date")  # 前端传入的时间
    investPurposeCheck = params.get("investPurpose")  # 前端传入的参数：投资目的
    sectorCheck = params.get("sector")  # 前端传入的参数：负责部门
    managerCheck = params.get("manager")  # 前端传入的参数：管理人
    strategyCheck = params.get("strategy")
    # 对传参进行处理，非空值
    if investPurposeCheck == '' or investPurposeCheck is None:
        investPurposeCheck = '全部'
    if sectorCheck == '' or sectorCheck is None:
        sectorCheck = '全部'
    if managerCheck == '' or managerCheck is None:
        managerCheck = '全部'
    if strategyCheck == '' or strategyCheck is None:
        strategyCheck = '全部'
    if dateRange == '' or dateRange is None:
        return JsonResponse({
            "code": 0,
            "msg": "成功",
            "data": results,
            "total": 0
        })
    else:
        begDate = dateRange[:10]
        endDate = dateRange[-10:]

    print(investPurposeCheck, sectorCheck, managerCheck, begDate, endDate)

    # 计算经纪业务数据
    dailyDf = calcBroker.getDailyDf(begDate, endDate)
    if len(dailyDf) == 0:
        return JsonResponse({
            "code": 1,
            "msg": "无经纪业务数据",
            "data": '无经纪业务数据',
            "total": 0
        })

    queryset = fundBasicInfo.objects.filter(confirmDate2__lte=endDate).values()
    dailyData = pd.DataFrame()
    if investPurposeCheck != '全部':
        queryset = queryset.filter(investPurpose=investPurposeCheck).values()
    if sectorCheck != '全部':
        queryset = queryset.filter(sector=sectorCheck).values()
    if managerCheck != '全部':
        queryset = queryset.filter(manager=managerCheck).values()
    if strategyCheck != '全部':
        queryset = queryset.filter(strategy=strategyCheck).values()
    for query in queryset:
        manager = query.get('manager')
        if len(dailyData) == 0:
            dailyData = dailyData.append(dailyDf.loc[dailyDf.manager == manager])
        else:
            if manager not in dailyData.manager.tolist():
                dailyData = dailyData.append(dailyDf.loc[dailyDf.manager == manager])

    dateList = []
    totalEndEquityList = []
    totalBrokerIncomeList = []

    dateList = list(set(dailyData.date.tolist()))
    dateList.sort()
    for d in dateList:
        totalEndEquity = 0
        totalNetLeft = 0
        totalNetIntIncome = 0
        for endEquity in dailyData.loc[dailyData.date == d].endEquity:
            totalEndEquity = totalEndEquity + float(endEquity)
        for netLeft in dailyData.loc[dailyData.date == d].netLeft:
            totalNetLeft = totalNetLeft + float(netLeft)
        for netIntIncome in dailyData.loc[dailyData.date == d].netIntIncome:
            totalNetIntIncome = totalNetIntIncome + float(netIntIncome)
        if totalEndEquity == 0:
            if len(totalEndEquityList) != 0:
                totalEndEquityList.append(totalEndEquityList[-1])
            else:
                totalEndEquityList.append(0)
        else:
            totalEndEquityList.append(round(totalEndEquity / 10000, 2))
        totalBrokerIncomeList.append(round(totalNetIntIncome + totalNetLeft, 2))

    results['dateList'] = dateList
    results['totalEndEquityList'] = totalEndEquityList
    results['totalBrokerIncomeList'] = totalBrokerIncomeList
    return JsonResponse({
        "code": 0,
        "msg": "成功",
        "data": results,
        "total": 0
    })


# 获取在投规模分布，时间序列
def getInvestAmountData(request):
    today = datetime.today()  # 获取当前日期
    params = request.GET
    dateRange = params.get("date")
    investPurposeCheck = params.get("investPurpose")  # 前端传入的参数：投资目的
    sectorCheck = params.get("sector")  # 前端传入的参数：负责部门
    managerCheck = params.get("manager")  # 前端传入的参数：管理人
    strategyCheck = params.get("strategy")
    # 对传参进行处理，非空值
    if investPurposeCheck == '' or investPurposeCheck is None:
        investPurposeCheck = '全部'
    if sectorCheck == '' or sectorCheck is None:
        sectorCheck = '全部'
    if managerCheck == '' or managerCheck is None:
        managerCheck = '全部'
    if strategyCheck == '' or strategyCheck is None:
        strategyCheck = '全部'
    if dateRange == '' or dateRange is None:
        begDate = str(today.year) + "-" + str(today.month) + "-01"
        endDate = today.strftime("%Y-%m-%d")
    else:
        begDate = dateRange[:10]  # 前端传入的时间
        endDate = dateRange[-10:]
    year = str(datetime.strptime(endDate, "%Y-%m-%d").year) + '0101'
    results = {
        "total": 0,
        "investAmountList": [],
    }
    productInfo = []
    queryset = fundBasicInfo.objects.filter(confirmDate2__lte=endDate).values()
    if investPurposeCheck != '全部':
        queryset = queryset.filter(investPurpose=investPurposeCheck).values()
    if sectorCheck != '全部':
        queryset = queryset.filter(sector=sectorCheck).values()
    if managerCheck != '全部':
        queryset = queryset.filter(manager=managerCheck).values()
    if strategyCheck != '全部':
        queryset = queryset.filter(strategy=strategyCheck).values()
    for query in queryset:
        dicts = {}
        dicts['productName'] = query.get('productName')
        dicts['investPurpose'] = query.get('investPurpose')
        productInfo.append(dicts)

    df = pd.DataFrame(productInfo)
    if len(df) == 0:
        totalInfo = ['无符合要求产品']
        dateList = [begDate, endDate]
        investAmountList = [0, 0]
    else:
        productList = list(set(df.productName.tolist()))

        totalInfo = investAmount.getInvestAmountList(begDate, endDate, productList)

        df = pd.DataFrame(totalInfo)
        dateList = df.date.tolist()
        investAmountList = df.totalInvestAmount.tolist()
    return JsonResponse({
        "code": 0,
        "msg": "成功",
        "totalInfo": totalInfo,
        "dateList": dateList,
        "investAmountList": investAmountList,
        "total": 0
    })