# -*- coding: utf-8 -*-

"""
@author: zzj

@contact: QQ:10996784

@Created on: 2020/10/13 007 11:28
"""

from django.core.paginator import Paginator
from django.http import JsonResponse

from FundProjects.models import fundBasicInfo, fundPnlInfo, tradeInfo, fundNetValueInfo, \
    deruisectordata, dailyFinanceData
from django.db.models import Sum
from datetime import datetime

hisSpecialProductList = ['钢铁1号', '星光璀璨1号', '和誉3号', '银河期货大宗商品1号', '权银河旗舰3/4号', '银河人保安心盛世1号', '融宝16号', '华澳臻智稳健1期',
                         '权银河恒星1号']
nonInvestProductList = ['权银河旗舰3/4号', '银河人保安心盛世1号', '融宝16号', '华澳臻智稳健1期', '权银河恒星1号']


# 集团并表
def getCombinedStat(request):
    params = request.GET
    print(params)
    date = params.get("date", None)

    dataList = []
    if date:
        dic = {}

        query = deruisectordata.objects.filter(date=date).first()
        dic['totalCashDelta'] = round(query.totalCashDelta, 4)
        dic['totalVar'] = round(query.totalVar, 4)
        dic['totalPnl'] = round(query.totalPnl, 4)
        if query.totalLoss is None:
            dic['totalLoss'] = ''
        else:
            dic['totalLoss'] = round(query.totalLoss, 4)

        dic['otcAmt'] = round(query.otcAmt, 4)
        dic['totalInvestPnl'] = round(-query.totalPnl, 4)
        dic['ommAmt'] = round(query.ommAmt, 4)

        dic['equityCashDelta'] = round(query.equityCashDelta, 4)
        dic['equityVar'] = round(query.equityVar, 4)
        dic['equityPnl'] = round(query.equityPnl, 4)
        if query.equityLoss is None:
            dic['equityLoss'] = ''
        else:
            dic['equityLoss'] = round(query.equityLoss, 4)
        dic['nonEquityCashDelta'] = round(query.nonEquityCashDelta, 4)
        dic['nonEquityVar'] = round(query.nonEquityVar, 4)
        dic['nonEquityPnl'] = round(query.nonEquityPnl, 4)
        if query.nonEquityLoss is None:
            dic['nonEquityLoss'] = ''
        else:
            dic['nonEquityLoss'] = round(query.nonEquityLoss, 4)

        financeData = dailyFinanceData.objects.filter(date=date).first()
        dic['netEquity'] = round(financeData.netEquity, 4)
        dic['netAsset'] = round(financeData.netAsset, 4)
        dic['netEAratio'] = round(financeData.netEAratio * 100, 4)
        dic['riskCapital'] = round(financeData.riskCapital, 4)
        dic['coverRatio'] = round(financeData.coverRatio * 100, 4)

        dic['productAmt_rm'] = financeData.productAmt
        dic['productNum_rm'] = financeData.productNum
        dic['productYearPnl_rm'] = round(financeData.productYearPnl, 2)
        dic['productCumPnl_rm'] = round(financeData.productCumPnl, 2)


        year = datetime.strptime(date, "%Y-%m-%d").year
        pnl = fundPnlInfo.objects.filter(date=date).all()
        dic['productAmt'] = round(
            (pnl.aggregate(Sum('buyCashAmount')).get('buyCashAmount__sum') - pnl.aggregate(
                Sum('sellCost')).get('sellCost__sum')) / 10000 , 4)
        amtList = []
        for p in pnl:
            amt = p.buyCashAmount - p.sellCost
            amtList.append(amt)
        dic['productSingleAmt'] = round(max(amtList) / 10000,4)
        dic['productVaR'] = round(
            (-pnl.aggregate(Sum('var')).get('var__sum')), 4)

        pnlSum = pnl.aggregate(Sum('todayPnl'))
        if pnlSum.get('todayPnl__sum') is not None:
            dic['dailyPnl'] = round(pnlSum.get('todayPnl__sum') / 10000, 2)
        else:
            dic['dailyPnl'] = 0.

        pnl = fundPnlInfo.objects.filter(date__lte=date).all()
        pnlSum = pnl.aggregate(Sum('todayPnl'))
        if pnlSum.get('todayPnl__sum') is not None:
            dic['cumPnl'] = round(pnlSum.get('todayPnl__sum') / 10000, 2)
        else:
            dic['cumPnl'] = 0.

        pnl = fundPnlInfo.objects.filter(date__lte=date).order_by("-date").all()
        pnlYear = pnl.filter(date__year=year).aggregate(Sum('todayPnl'))
        if pnlYear.get('todayPnl__sum') is None:
            dic['yearPnl'] = 0.
        else:
            dic['yearPnl'] = round(pnlYear.get('todayPnl__sum') / 10000, 2)


        dataList.append(dic)
        if query:
            result = {
                "code": 2000,
                "msg": "查询成功",
                "data": dataList
            }
        else:
            result = {
                "code": 0,
                "msg": "无数据",
                "data": None
            }
    else:
        result = {
            "code": 0,
            "msg": "无数据",
            "data": None
        }
    return JsonResponse(result)


# 证券报告
def getProductReportSec(request):
    today = datetime.today()  # 获取当前日期
    params = request.GET
    date = params.get("date")  # 前端传入的时间
    ''':param
        1.判断前端是否传入时间
        2.如果没有传入时间,则使用今天
        3.传入时间,就根据传入时间查询
    '''
    if date is None or date == "":
        year = today.year
        project_date = today.strftime("%Y-%m-%d")
        queryset = fundBasicInfo.objects.values()
    else:
        year = datetime.strptime(date, "%Y-%m-%d").year
        project_date = datetime.strptime(date, "%Y-%m-%d").strftime("%Y-%m-%d")
        queryset = fundBasicInfo.objects.filter(confirmDate2__lte=date).values()

    results = {
        "total": 0,
        "data": [],
        "projectList": []

    }
    fundReportData = []
    for query in queryset:
        dicts = {
            "date": project_date,
            "productFullName": '',
            "confirmDate2": project_date,
            "status": '',
            "productType1": '',
            "productType2": '',
            "productType3": '',
            "senior": '',
            "redeemLimit": '',

            "netValue": '',
            "acNetValue": '',

            "investAmount": '',
            "buyAmount": '',
            "sellAmount": '',
            "sellCashAmount": '',
            "todayPnl": '',

            "cashDividend": '',
            "yearPnlSec": '',
        }
        productName = query.get('productName')
        dicts['date'] = project_date
        dicts['productFullName'] = query.get('productFullName')
        dicts['confirmDate2'] = query.get('confirmDate2').strftime("%Y-%m-%d")
        dicts['status'] = query.get('status')
        dicts['productType1'] = query.get('productType1')
        dicts['productType2'] = query.get('productType2')
        dicts['productType3'] = query.get('productType3')
        dicts['senior'] = query.get('senior')
        dicts['redeemLimit'] = query.get('redeemLimit')

        # 获取数据库中原始数据
        netValue = fundNetValueInfo.objects.filter(productName=productName, date=project_date).order_by(
            "lastUpdateDate").first()
        if netValue is not None:
            dicts['acNetValue'] = round(netValue.acNetValue, 6)
            dicts['netValue'] = round(netValue.netValue, 6)

        pnl = fundPnlInfo.objects.filter(productName=productName, date=project_date).first()
        if pnl is not None:
            dicts['investAmount'] = round((pnl.acBuyAmount - pnl.acSellAmount), 2)
            dicts['investCost'] = round((pnl.buyCashAmount - pnl.sellCost), 2)
            dicts['todayPnl'] = round(pnl.todayPnl, 2)

        # 当日申购份额
        trade = tradeInfo.objects.filter(productName=productName, confirmDate=project_date, tradeType='申购').all()
        tradeSum = trade.aggregate(Sum('tradeShare'))
        if tradeSum.get('tradeShare__sum') is not None:
            dicts['buyAmount'] = tradeSum.get('tradeShare__sum')
        else:
            dicts['buyAmount'] = 0

        # 当日赎回款
        trade = tradeInfo.objects.filter(productName=productName, confirmDate=project_date, tradeType='赎回').all()
        tradeSum = trade.aggregate(Sum('tradeAmount'))
        if tradeSum.get('tradeAmount__sum') is not None:
            dicts['sellCashAmount'] = tradeSum.get('tradeAmount__sum')
        else:
            dicts['sellCashAmount'] = 0
        # 当日赎回份额
        tradeSum = trade.aggregate(Sum('tradeShare'))
        if tradeSum.get('tradeShare__sum') is not None:
            dicts['sellAmount'] = tradeSum.get('tradeShare__sum')
        else:
            dicts['sellAmount'] = 0

        # 当日现金分红
        trade = tradeInfo.objects.filter(productName=productName, confirmDate=project_date, tradeType='现金分红').all()
        tradeSum = trade.aggregate(Sum('tradeAmount'))
        if tradeSum.get('tradeAmount__sum') is not None:
            dicts['cashDividend'] = tradeSum.get('tradeAmount__sum')
        else:
            dicts['cashDividend'] = 0

        lists = fundPnlInfo.objects.filter(productName=productName).filter(date__lte=project_date).order_by(
            "-date").all()
        pnl_securityalgorithm_year = lists.filter(date__year=year).aggregate(Sum('todayPnl'))
        if pnl_securityalgorithm_year.get('todayPnl__sum') is None:
            dicts['yearPnlSec'] = 0.
        else:
            yearPnlSec = pnl_securityalgorithm_year.get('todayPnl__sum')
            dicts['yearPnlSec'] = round(yearPnlSec/10000, 2)

        lists = fundPnlInfo.objects.filter(productName=productName).filter(date__lte=project_date).order_by(
            "-date").all()
        pnl_securityalgorithm_cum = lists.aggregate(Sum('todayPnl'))
        if pnl_securityalgorithm_cum.get('todayPnl__sum') is None:
            dicts['cumPnlSec'] = 0.
        else:
            cumPnlSec = pnl_securityalgorithm_cum.get('todayPnl__sum')
            dicts['cumPnlSec'] = round(cumPnlSec/10000, 2)

        # 将数据添加到返回给前端的列表中
        fundReportData.append(dicts)

    pageIndex = request.GET.get('page', 1)
    pageSize = request.GET.get('limit', 10)
    pageInator = Paginator(fundReportData, pageSize)
    contacts = pageInator.page(pageIndex)
    results['data'] = contacts.object_list
    results['total'] = len(fundReportData)
    results['projectList'] = fundReportData
    return JsonResponse({
        "code": 0,
        "msg": "成功",
        "data": results,
        "total": 0
    })