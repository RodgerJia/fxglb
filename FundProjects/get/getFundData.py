# -*- coding: utf-8 -*-

"""
@author: zzj

@contact: QQ:10996784

@Created on: 2020/10/13 007 11:28
"""

from django.core.paginator import Paginator
from django.http import JsonResponse

from FundProjects.models import fundBasicInfo, fundPnlInfo, tradeInfo, totalAmountInfo, fundNetValueInfo, \
    confirmNetValueInfo
from django.db.models import Sum
from datetime import datetime
import pandas as pd

hisSpecialProductList = ['钢铁1号', '星光璀璨1号', '和誉3号', '银河期货大宗商品1号', '权银河旗舰3/4号', '银河人保安心盛世1号', '融宝16号', '华澳臻智稳健1期',
                         '权银河恒星1号']
nonInvestProductList = ['权银河旗舰3/4号', '银河人保安心盛世1号', '融宝16号', '华澳臻智稳健1期', '权银河恒星1号']


# 产品数据，获取数据库数据
def getTradeInfo(request):
    today = datetime.today()
    project_date = today.strftime("%Y-%m-%d")
    # 倒序查询全部数据
    productName = request.POST.get('productName', "")
    queryset = tradeInfo.objects.order_by("-index").values()
    results = {
        "total": 0,
        "data": [],
        "tradeInfo": []

    }
    tradeInfoData = []
    for query in queryset:
        dicts = {
            "date": project_date,
            "productName": "",
            "applyDate": project_date,
            "confirmDate": project_date,
            "tradeType": "",
            "tradeShare": 0,
            "unitNet": 0,
            "fee": 0,
            "tradeAmount": 0,
            "cost": 0,
        }
        dicts['date'] = query.get('date').strftime("%Y-%m-%d")
        dicts['productName'] = query.get('productName')
        dicts['applyDate'] = query.get('applyDate').strftime("%Y-%m-%d")
        dicts['confirmDate'] = query.get('confirmDate').strftime("%Y-%m-%d")
        dicts['tradeType'] = query.get('tradeType')
        dicts['tradeShare'] = query.get('tradeShare')
        dicts['unitNet'] = query.get('unitNet')
        dicts['fee'] = query.get('fee')
        dicts['tradeAmount'] = query.get('tradeAmount')
        dicts['cost'] = query.get('cost')
        # 将数据添加到返回给前端的列表中
        tradeInfoData.append(dicts)

    pageIndex = request.GET.get('page', 1)
    pageSize = request.GET.get('limit', 10)
    pageInator = Paginator(tradeInfoData, pageSize)
    contacts = pageInator.page(pageIndex)
    results['data'] = contacts.object_list
    results['total'] = len(tradeInfoData)
    results['tradeInfoData'] = tradeInfoData
    return JsonResponse({
        "code": 0,
        "msg": "成功",
        "data": results,
        "total": 0
    })


def getBasicInfo(request):
    today = datetime.today()
    project_date = today.strftime("%Y-%m-%d")
    # 倒序查询全部数据
    queryset = fundBasicInfo.objects.order_by("-index").values()
    results = {
        "total": 0,
        "data": [],
        "fundBasicInfo": []

    }
    fundBasicInfoData = []
    for query in queryset:
        dicts = {
            "date": project_date,
            "confirmDate1": project_date,
            "confirmDate2": project_date,
            "productName": "",
            "productFullName": "",

            "productType1": "",
            "productType2": "",
            "productType3": "",
            "strategy": "",
            "senior": "",
            "redeemLimit": "",
            "manager": "",
            "status": "",
            "sector": "",

            "alertLimit": 0,
            "cleanLimit": 0,
            "investableAmount": 0,
            "totalAmount": 0,
            "redeemCost": 0,

            "preProvideFundDate": "",
            "preInvestDuration": "",
            "openDay": "",
            "temporaryOpen": "",

            "rmAlertLimit": 0,
            "rmCleanLimit": 0,

            "rmRules": "",
            "investPurpose": "",
            "selfManage": "",
            "investAdvisor": "",
            "synergy": "",
            "thirdParty": "",
            "synergyAmount": 0,

            "demo": ''
        }
        dicts['date'] = query.get('date').strftime("%Y-%m-%d")
        dicts['confirmDate1'] = query.get('confirmDate1').strftime("%Y-%m-%d")
        dicts['confirmDate2'] = query.get('confirmDate2').strftime("%Y-%m-%d")
        dicts['productName'] = query.get('productName')
        dicts['productFullName'] = query.get('productFullName')

        dicts['productType1'] = query.get('productType1')
        dicts['productType2'] = query.get('productType2')
        dicts['productType3'] = query.get('productType3')
        dicts['strategy'] = query.get('strategy')
        dicts['senior'] = query.get('senior')
        dicts['redeemLimit'] = query.get('redeemLimit')
        dicts['manager'] = query.get('manager')
        dicts['status'] = query.get('status')
        dicts['sector'] = query.get('sector')

        dicts['alertLimit'] = query.get('alertLimit')
        dicts['cleanLimit'] = query.get('cleanLimit')
        dicts['investableAmount'] = query.get('investableAmount')
        dicts['totalAmount'] = query.get('totalAmount')
        dicts['redeemCost'] = query.get('redeemCost')

        dicts['preProvideFundDate'] = query.get('preProvideFundDate')
        dicts['preInvestDuration'] = query.get('preInvestDuration')
        dicts['openDay'] = query.get('openDay')
        dicts['temporaryOpen'] = query.get('temporaryOpen')

        dicts['rmAlertLimit'] = query.get('rmAlertLimit')
        dicts['rmCleanLimit'] = query.get('rmCleanLimit')

        dicts['rmRules'] = query.get('rmRules')
        dicts['investPurpose'] = query.get('investPurpose')
        dicts['selfManage'] = query.get('selfManage')
        dicts['investAdvisor'] = query.get('investAdvisor')
        dicts['synergy'] = query.get('synergy')
        dicts['thirdParty'] = query.get('thirdParty')
        dicts['synergyAmount'] = query.get('synergyAmount')

        dicts['demo'] = query.get('demo')
        # 将数据添加到返回给前端的列表中
        fundBasicInfoData.append(dicts)

    pageIndex = request.GET.get('page', 1)
    pageSize = request.GET.get('limit', 10)
    pageInator = Paginator(fundBasicInfoData, pageSize)
    contacts = pageInator.page(pageIndex)
    results['data'] = contacts.object_list
    results['total'] = len(fundBasicInfoData)
    results['fundBasicInfoData'] = fundBasicInfoData
    print(queryset)
    return JsonResponse({
        "code": 0,
        "msg": "成功",
        "data": results,
        "total": 0
    })


def getTotalAmountInfo(request):
    today = datetime.today()
    project_date = today.strftime("%Y-%m-%d")
    # 倒序查询全部数据
    queryset = totalAmountInfo.objects.order_by("-index").values()
    results = {
        "total": 0,
        "data": [],
        "fundBasicInfo": []

    }
    totalAmountData = []
    for query in queryset:
        dicts = {
            "date": project_date,
            "confirmDate": project_date,

            "totalAmount": 0,
            "newUsed": 0,
            "usedAmount": 0,
            "newBack": 0,
            "usableAmount": 0,

            "demo": ''
        }
        dicts['date'] = query.get('date').strftime("%Y-%m-%d")
        dicts['confirmDate'] = query.get('confirmDate').strftime("%Y-%m-%d")
        dicts['totalAmount'] = query.get('totalAmount')
        dicts['newUsed'] = query.get('newUsed')
        dicts['usedAmount'] = query.get('usedAmount')
        dicts['newBack'] = query.get('newBack')
        dicts['usableAmount'] = query.get('usableAmount')
        dicts['demo'] = query.get('demo')
        # 将数据添加到返回给前端的列表中
        totalAmountData.append(dicts)
    basicInfo = fundBasicInfo.objects.order_by("-index").all()
    totalAmount = basicInfo.aggregate(Sum('totalAmount')).get('totalAmount__sum')
    redeemCost = basicInfo.aggregate(Sum('redeemCost')).get('redeemCost__sum')

    pageIndex = request.GET.get('page', 1)
    pageSize = request.GET.get('limit', 10)
    pageInator = Paginator(totalAmountData, pageSize)
    contacts = pageInator.page(pageIndex)
    results['data'] = contacts.object_list
    results['total'] = len(totalAmountData)
    results['totalAmountData'] = totalAmountData
    results['availableAmount'] = 350000000 - totalAmount + redeemCost

    return JsonResponse({
        "code": 0,
        "msg": "成功",
        "data": results,
        "total": 0
    })


def getFundNetValueInfo(request):
    today = datetime.today()
    project_date = today.strftime("%Y-%m-%d")
    # 倒序查询全部数据
    queryset = fundNetValueInfo.objects.order_by("-date").values()
    results = {
        "total": 0,
        "data": [],
        "fundNetValueData": []

    }
    fundNetValueData = []
    for query in queryset:
        dicts = {
            "date": project_date,
            "lastUpdateDate": project_date,

            "productName": '',
            "netValue": 0,
            "acNetValue": 0,

            "demo": ''
        }
        dicts['date'] = query.get('date').strftime("%Y-%m-%d")
        dicts['lastUpdateDate'] = query.get('lastUpdateDate').strftime("%Y-%m-%d")
        dicts['productName'] = query.get('productName')
        dicts['netValue'] = round(query.get('netValue'), 6)
        dicts['acNetValue'] = round(query.get('acNetValue'), 6)
        dicts['demo'] = query.get('demo')
        # 将数据添加到返回给前端的列表中
        fundNetValueData.append(dicts)

    pageIndex = request.GET.get('page', 1)
    pageSize = request.GET.get('limit', 10)
    pageInator = Paginator(fundNetValueData, pageSize)
    contacts = pageInator.page(pageIndex)
    results['data'] = contacts.object_list
    results['total'] = len(fundNetValueData)
    results['fundNetValueData'] = fundNetValueData

    return JsonResponse({
        "code": 0,
        "msg": "成功",
        "data": results,
        "total": 0
    })


def getConfirmNetValueInfo(request):
    today = datetime.today()
    project_date = today.strftime("%Y-%m-%d")
    # 倒序查询全部数据
    queryset = confirmNetValueInfo.objects.order_by("-date").values()
    results = {
        "total": 0,
        "data": [],
        "fundNetValueData": []

    }
    fundNetValueData = []
    for query in queryset:
        dicts = {
            "date": project_date,
            "lastUpdateDate": project_date,

            "productName": '',
            "netValue": 0,
            "acNetValue": 0,

            "demo": ''
        }
        dicts['date'] = query.get('date').strftime("%Y-%m-%d")
        dicts['lastUpdateDate'] = query.get('lastUpdateDate').strftime("%Y-%m-%d")
        dicts['productName'] = query.get('productName')
        dicts['netValue'] = round(query.get('netValue'), 6)
        dicts['acNetValue'] = round(query.get('acNetValue'), 6)
        dicts['demo'] = query.get('demo')
        # 将数据添加到返回给前端的列表中
        fundNetValueData.append(dicts)

    pageIndex = request.GET.get('page', 1)
    pageSize = request.GET.get('limit', 10)
    pageInator = Paginator(fundNetValueData, pageSize)
    contacts = pageInator.page(pageIndex)
    results['data'] = contacts.object_list
    results['total'] = len(fundNetValueData)
    results['fundNetValueData'] = fundNetValueData

    return JsonResponse({
        "code": 0,
        "msg": "成功",
        "data": results,
        "total": 0
    })


def getFundPnlReportData(request):
    today = datetime.today()
    project_date = today.strftime("%Y-%m-%d")
    params = request.GET
    date = params.get("date")
    productNameCheck = params.get("productNameCheck", "全部")
    if date is None or date == "":
        today = datetime.today()
        project_date = today.strftime("%Y-%m-%d")
    else:
        project_date = datetime.strptime(date, "%Y-%m-%d").strftime("%Y-%m-%d")
    if productNameCheck is None or productNameCheck == "":
        productNameCheck = '全部'
    print(project_date, productNameCheck)
    queryset = fundPnlInfo.objects.filter(date__lte=project_date).order_by("-date").values()
    results = {
        "total": 0,
        "data": [],
        "fundNetValueData": [],
        "fundTotalData": []
    }
    fundTotalData = []
    fundPnlReportData = []
    for query in queryset:
        dicts = {
            "date": project_date,
            "productName": '',

            "acBuyAmount": 0,
            "acSellAmount": 0,
            "buyCashAmount": 0,
            "sellCashAmount": 0,
            "sellCost": 0,
            "cashDiv": 0,

            "todayNetValue": 0,
            "todayPnl": 0,
            "cumPnl": 0,
            "var": 0,
        }
        dicts['productName'] = query.get('productName')
        if productNameCheck != '全部':
            if dicts['productName'] != productNameCheck:
                continue
        dicts['date'] = query.get('date').strftime("%Y-%m-%d")
        dicts['acBuyAmount'] = query.get('acBuyAmount')
        dicts['acSellAmount'] = query.get('acSellAmount')
        dicts['buyCashAmount'] = query.get('buyCashAmount')
        dicts['sellCashAmount'] = query.get('sellCashAmount')
        dicts['sellCost'] = query.get('sellCost')
        dicts['cashDiv'] = query.get('cashDiv')
        dicts['todayNetValue'] = query.get('todayNetValue')

        todayPnl = query.get('todayPnl')
        dicts['todayPnl'] = round(todayPnl, 2)
        cumPnl = query.get('cumPnl')
        dicts['cumPnl'] = round(cumPnl, 2)
        var = query.get('var')
        if var is None or var == '':
            var = 0.
        dicts['var'] = round(var, 6)
        # 将数据添加到返回给前端的列表中
        fundPnlReportData.append(dicts)
        if dicts['date'] == project_date:
            fundTotalData.append(dicts)
    fundTotalData = pd.DataFrame(fundTotalData)
    if len(fundTotalData) == 0:
        fundTotalData = [{'date': project_date,
                          'productName': len(fundTotalData),
                          'acBuyAmount': 0,
                          'acSellAmount': 0,
                          'buyCashAmount': 0,
                          'sellCashAmount': 0,
                          'sellCost': 0,
                          'cashDiv': 0,
                          'todayPnl': 0,
                          'cumPnl': 0,
                          'var': 0
                          }]
    else:
        fundTotalData = [{'date': project_date,
                          'productName': len(fundTotalData),
                          'acBuyAmount': round(fundTotalData.acBuyAmount.sum(), 2),
                          'acSellAmount': round(fundTotalData.acSellAmount.sum(), 2),
                          'buyCashAmount': fundTotalData.buyCashAmount.sum(),
                          'sellCashAmount': fundTotalData.sellCashAmount.sum(),
                          'sellCost': fundTotalData.sellCost.sum(),
                          'cashDiv': fundTotalData.cashDiv.sum(),
                          'todayPnl': round(fundTotalData.todayPnl.sum(), 2),
                          'var': round(fundTotalData['var'].sum(), 2)
                          }]
    pageIndex = request.GET.get('page', 1)
    pageSize = request.GET.get('limit', 10)
    pageInator = Paginator(fundPnlReportData, pageSize)
    contacts = pageInator.page(pageIndex)
    results['data'] = contacts.object_list
    results['total'] = len(fundPnlReportData)
    results['fundNetValueData'] = fundPnlReportData
    results['fundTotalData'] = fundTotalData
    return JsonResponse({
        "code": 0,
        "msg": "成功",
        "data": results,
        "total": 0
    })


def availableProductName(request):
    today = datetime.today()
    project_date = today.strftime("%Y-%m-%d")
    # queryset = fundBasicInfo.objects.filter(status__in=['未结束', '在投']).values()
    queryset = fundBasicInfo.objects.values()
    results = {
        "total": 0,
        "data": [],
        "productNameData": [],
    }
    dataList = []
    sectorList = []
    managerList = []
    for query in queryset:
        dicts = {
            "date": project_date,
            "lastUpdateDate": project_date,
            "productName": '',
            "sector": '',
            "manager": '',
        }
        dicts['date'] = query.get('date')
        dicts['lastUpdateDate'] = query.get('lastUpdateDate')
        dicts['productName'] = query.get('productName')
        sector = query.get('sector')
        if sector not in sectorList:
            dicts['sector'] = sector
            sectorList.append(sector)
        manager = query.get('manager')
        if manager not in managerList:
            dicts['manager'] = manager
            managerList.append(manager)
        # 将数据添加到返回给前端的列表中
        dataList.append(dicts)

    results['productNameData'] = dataList

    return JsonResponse({
        "code": 0,
        "msg": "成功",
        "data": results,
        "total": 0
    })