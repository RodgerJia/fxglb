# -*- coding: utf-8 -*-

"""
@author: zzj

@contact: QQ:10996784

@Created on: 2020/10/13 007 11:28
"""

from django.http import JsonResponse

from FundProjects.models import fundBasicInfo, fundPnlInfo, deruiLimitData, deruisectordata, deruiCreditData, dailyFinanceData, productDailyReport, \
    rmDailyReport, rmDoubleWeeklyReport
from django.db.models import Sum
from datetime import datetime
from django.db.models import Q

hisSpecialProductList = ['钢铁1号', '星光璀璨1号', '和誉3号', '银河期货大宗商品1号', '权银河旗舰3/4号', '银河人保安心盛世1号', '融宝16号', '华澳臻智稳健1期',
                         '权银河恒星1号']
nonInvestProductList = ['权银河旗舰3/4号', '银河人保安心盛世1号', '融宝16号', '华澳臻智稳健1期', '权银河恒星1号']

def getDailyData(request):
    params = request.GET
    print(params)
    date = params.get("date", None)

    dataList = []
    if date:

        query = deruiLimitData.objects.filter(date=date).first()

        dic = {}
        dic['date'] = str(date[:4]) + '年' + str(int(date[5:7])) + '月' + str(int(date[8:])) + '日'
        dic['reportDate'] = str(datetime.today().year) + '年' + str(datetime.today().month) + '月' + str(
            datetime.today().day) + '日'

        dic['l1_assetAmt'] = round(query.l1_assetAmt * 100, 2)
        dic['l1_creditAmt_nonSecBank_usable'] = round(query.l1_creditAmt_nonSecBank_usable * 10000, 2)
        dic['l1_creditAmt_nonSecBank_used'] = round(query.l1_creditAmt_nonSecBank_used * 10000, 2)
        dic['l1_creditAmt_secBank_usable'] = round(query.l1_creditAmt_secBank_usable * 10000, 2)
        dic['l1_creditAmt_secBank_used'] = round(query.l1_creditAmt_secBank_used * 10000, 2)

        dic['l2_otc_creditAmt_nonSecBank'] = round(query.l2_otc_creditAmt_nonSecBank * 10000, 2)
        dic['l2_otc_creditAmt_secBank'] = round(query.l2_otc_creditAmt_secBank * 10000, 2)
        dic['l2_c_creditAmt_usable'] = round(query.l2_c_creditAmt_usable * 10000, 2)
        dic['l2_c_creditAmt_used'] = round(query.l2_c_creditAmt_used * 10000, 2)

        query = deruisectordata.objects.filter(date=date).first()
        queryLast = deruisectordata.objects.filter(date__lt=date).order_by('-date').first()
        dic['totalCashDelta'] = round(query.totalCashDelta, 2)
        dic['totalCashDeltaChange'] = round(round(query.totalCashDelta, 2) - round(queryLast.totalCashDelta, 2), 2)
        dic['totalVar'] = round(query.totalVar, 2)
        dic['totalVarChange'] = round(round(query.totalVar, 2) - round(queryLast.totalVar, 2), 2)
        dic['totalPnl'] = round(query.totalPnl, 2)
        dic['totalPnlChange'] = round(round(query.totalPnl, 2) - round(queryLast.totalPnl, 2), 2)
        dic['totalAmt'] = round(
            round(query.otcAmt, 2) + round(query.ommAmt, 2) + round(query.sigmaAmt, 2) + round(query.cAmt, 2), 2)
        dic['totalAmtChange'] = round(dic['totalAmt'] - (round(
            round(queryLast.otcAmt, 2) + round(queryLast.ommAmt, 2) + round(queryLast.sigmaAmt, 2) + round(
                queryLast.cAmt, 2), 2)), 2)

        dic['otcAmt'] = round(query.otcAmt, 2)
        dic['otcCashDelta'] = round(query.otcCashDelta, 2)
        dic['otcVar'] = round(query.otcVar, 2)
        dic['otcPnl'] = round(query.otcPnl, 2)
        dic['otcAmtChange'] = round(round(query.otcAmt, 2) - round(queryLast.otcAmt, 2), 2)
        dic['otcCashDeltaChange'] = round(round(query.otcCashDelta, 2) - round(queryLast.otcCashDelta, 2), 2)
        dic['otcVarChange'] = round(round(query.otcVar, 2) - round(queryLast.otcVar, 2), 2)
        dic['otcPnlChange'] = round(round(query.otcPnl, 2) - round(queryLast.otcPnl, 2), 2)

        dic['ommAmt'] = round(query.ommAmt, 2)
        dic['ommCashDelta'] = round(query.ommCashDelta, 2)
        dic['ommVar'] = round(query.ommVar, 2)
        dic['ommPnl'] = round(query.ommPnl, 2)
        dic['ommAmtChange'] = round(round(query.ommAmt, 2) - round(queryLast.ommAmt, 2), 2)
        dic['ommCashDeltaChange'] = round(round(query.ommCashDelta, 2) - round(queryLast.ommCashDelta, 2), 2)
        dic['ommVarChange'] = round(round(query.ommVar, 2) - round(queryLast.ommVar, 2), 2)
        dic['ommPnlChange'] = round(round(query.ommPnl, 2) - round(queryLast.ommPnl, 2), 2)

        dic['sigmaAmt'] = round(query.sigmaAmt, 2)
        dic['sigmaCashDelta'] = round(query.sigmaCashDelta, 2)
        dic['sigmaVar'] = round(query.sigmaVar, 2)
        dic['sigmaPnl'] = round(query.sigmaPnl, 2)
        dic['sigmaAmtChange'] = round(round(query.sigmaAmt, 2) - round(queryLast.sigmaAmt, 2), 2)
        dic['sigmaCashDeltaChange'] = round(round(query.sigmaCashDelta, 2) - round(queryLast.sigmaCashDelta, 2), 2)
        dic['sigmaVarChange'] = round(round(query.sigmaVar, 2) - round(queryLast.sigmaVar, 2), 2)
        dic['sigmaPnlChange'] = round(round(query.sigmaPnl, 2) - round(queryLast.sigmaPnl, 2), 2)

        dic['cAmt'] = round(query.cAmt, 2)
        dic['cCashDelta'] = round(query.cCashDelta, 2)
        dic['cVar'] = round(query.cVar, 2)
        if query.cPnl == None:
            dic['cPnl'] = ''
            dic['cPnlChange'] = ''
        else:
            dic['cPnl'] = round(query.cPnl, 2)
            if queryLast.cPnl is None:
                dic['cPnlChange'] = ''
            else:
                dic['cPnlChange'] = round(round(query.cPnl, 2) - round(queryLast.cPnl, 2), 2)
        dic['cAmtChange'] = round(round(query.cAmt, 2) - round(queryLast.cAmt, 2), 2)
        dic['cCashDeltaChange'] = round(round(query.cCashDelta, 2) - round(queryLast.cCashDelta, 2),2)
        dic['cVarChange'] = round(round(query.cVar, 2) - round(queryLast.cVar, 2), 2)


        if query.otcAmt_fin is None:
            dic['otcAmt_fin'] = '无数据'
            dic['otcAmt_fin_Change'] = ''
        else:
            dic['otcAmt_fin'] = round(query.otcAmt_fin, 2)
            dic['otcAmt_fin_Change'] = round(round(query.otcAmt_fin, 2) - round(queryLast.otcAmt_fin, 2), 2)
        dic['otcCashDelta_fin'] = round(query.otcCashDelta_fin, 2)
        dic['otcVar_fin'] = round(query.otcVar_fin, 2)
        dic['otcPnl_fin'] = round(query.otcPnl_fin, 2)
        dic['otcCashDelta_fin_Change'] = round(round(query.otcCashDelta_fin, 2) - round(queryLast.otcCashDelta_fin, 2),
                                               2)
        dic['otcVar_fin_Change'] = round(round(query.otcVar_fin, 2) - round(queryLast.otcVar_fin, 2), 2)
        dic['otcPnl_fin_Change'] = round(round(query.otcPnl_fin, 2) - round(queryLast.otcPnl_fin, 2), 2)

        if query.otcAmt_comm is None:
            dic['otcAmt_comm'] = '无数据'
            dic['otcAmt_comm_Change'] = ''
        else:
            dic['otcAmt_comm'] = round(query.otcAmt_comm, 2)
            dic['otcAmt_comm_Change'] = round(round(query.otcAmt_comm, 2) - round(queryLast.otcAmt_comm, 2), 2)
        dic['otcCashDelta_comm'] = round(query.otcCashDelta_comm, 2)
        dic['otcVar_comm'] = round(query.otcVar_comm, 2)
        dic['otcPnl_comm'] = round(query.otcPnl_comm, 2)
        dic['otcCashDelta_comm_Change'] = round(
            round(query.otcCashDelta_comm, 2) - round(queryLast.otcCashDelta_comm, 2), 2)
        dic['otcVar_comm_Change'] = round(round(query.otcVar_comm, 2) - round(queryLast.otcVar_comm, 2), 2)
        dic['otcPnl_comm_Change'] = round(round(query.otcPnl_comm, 2) - round(queryLast.otcPnl_comm, 2), 2)

        if query.otcAmt_other is None:
            dic['otcAmt_other'] = '无数据'
            dic['otcAmt_other_Change'] = ''
        else:
            dic['otcAmt_other'] = round(query.otcAmt_other, 2)
            dic['otcAmt_other_Change'] = round(round(query.otcAmt_other, 2) - round(queryLast.otcAmt_other, 2), 2)
        dic['otcCashDelta_other'] = round(query.otcCashDelta_other, 2)
        dic['otcVar_other'] = round(query.otcVar_other, 2)
        dic['otcPnl_other'] = round(query.otcPnl_other, 2)
        dic['otcCashDelta_other_Change'] = round(
            round(query.otcCashDelta_other, 2) - round(queryLast.otcCashDelta_other, 2), 2)
        dic['otcVar_other_Change'] = round(round(query.otcVar_other, 2) - round(queryLast.otcVar_other, 2), 2)
        dic['otcPnl_other_Change'] = round(round(query.otcPnl_other, 2) - round(queryLast.otcPnl_other, 2), 2)

        if query.ommAmt_fut is None:
            dic['ommAmt_fut'] = '无数据'
            dic['ommAmt_fut_Change'] = ''
        else:
            dic['ommAmt_fut'] = round(query.ommAmt_fut, 2)
            dic['ommAmt_fut_Change'] = round(round(query.ommAmt_fut, 2) - round(queryLast.ommAmt_fut, 2), 2)
        dic['ommCashDelta_fut'] = round(query.ommCashDelta_fut, 2)
        dic['ommVar_fut'] = round(query.ommVar_fut, 2)
        dic['ommPnl_fut'] = round(query.ommPnl_fut, 2)
        dic['ommCashDelta_fut_Change'] = round(round(query.ommCashDelta_fut, 2) - round(queryLast.ommCashDelta_fut, 2),
                                               2)
        dic['ommVar_fut_Change'] = round(round(query.ommVar_fut, 2) - round(queryLast.ommVar_fut, 2), 2)
        dic['ommPnl_fut_Change'] = round(round(query.ommPnl_fut, 2) - round(queryLast.ommPnl_fut, 2), 2)

        if query.ommAmt_opt is None:
            dic['ommAmt_opt'] = '无数据'
            dic['ommAmt_opt_Change'] = ''
        else:
            dic['ommAmt_opt'] = round(query.ommAmt_opt, 2)
            dic['ommAmt_opt_Change'] = round(round(query.ommAmt_opt, 2) - round(queryLast.ommAmt_opt, 2), 2)
        dic['ommCashDelta_opt'] = round(query.ommCashDelta_opt, 2)
        dic['ommVar_opt'] = round(query.ommVar_opt, 2)
        dic['ommPnl_opt'] = round(query.ommPnl_opt, 2)
        dic['ommCashDelta_opt_Change'] = round(round(query.ommCashDelta_opt, 2) - round(queryLast.ommCashDelta_opt, 2),
                                               2)
        dic['ommVar_opt_Change'] = round(round(query.ommVar_opt, 2) - round(queryLast.ommVar_opt, 2), 2)
        dic['ommPnl_opt_Change'] = round(round(query.ommPnl_opt, 2) - round(queryLast.ommPnl_opt, 2), 2)

        if query.ommBack is None:
            dic['ommBack'] = 0
            dic['ommBack_Change'] = 0
        else:
            dic['ommBack'] = round(query.ommBack/10000, 2)
            if queryLast.ommBack is None:
                dic['ommBack_Change'] = round(query.ommBack/10000, 2)
            else:
                dic['ommBack_Change'] = round((query.ommBack - queryLast.ommBack)/10000, 2)



        if query.sigmaAmt_pro is None:
            dic['sigmaAmt_pro'] = '无数据'
            dic['sigmaAmt_pro_Change'] = ''
        else:
            dic['sigmaAmt_pro'] = round(query.sigmaAmt_pro, 2)
            dic['sigmaAmt_pro_Change'] = round(round(query.sigmaAmt_pro, 2) - round(queryLast.sigmaAmt_pro, 2), 2)
        dic['sigmaCashDelta_pro'] = round(query.sigmaCashDelta_pro, 2)
        dic['sigmaVar_pro'] = round(query.sigmaVar_pro, 2)
        dic['sigmaPnl_pro'] = round(query.sigmaPnl_pro, 2)
        dic['sigmaCashDelta_pro_Change'] = round(
            round(query.sigmaCashDelta_pro, 2) - round(queryLast.sigmaCashDelta_pro, 2), 2)
        dic['sigmaVar_pro_Change'] = round(round(query.sigmaVar_pro, 2) - round(queryLast.sigmaVar_pro, 2), 2)
        dic['sigmaPnl_pro_Change'] = round(round(query.sigmaPnl_pro, 2) - round(queryLast.sigmaPnl_pro, 2), 2)

        if query.sigmaAmt_vol is None:
            dic['sigmaAmt_vol'] = '无数据'
            dic['sigmaAmt_vol_Change'] = ''
        else:
            dic['sigmaAmt_vol'] = round(query.sigmaAmt_vol, 2)
            dic['sigmaAmt_vol_Change'] = round(round(query.sigmaAmt_vol, 2) - round(queryLast.sigmaAmt_vol, 2), 2)
        dic['sigmaCashDelta_vol'] = round(query.sigmaCashDelta_vol, 2)
        dic['sigmaVar_vol'] = round(query.sigmaVar_vol, 2)
        dic['sigmaPnl_vol'] = round(query.sigmaPnl_vol, 2)
        dic['sigmaCashDelta_vol_Change'] = round(
            round(query.sigmaCashDelta_vol, 2) - round(queryLast.sigmaCashDelta_vol, 2), 2)
        dic['sigmaVar_vol_Change'] = round(round(query.sigmaVar_vol, 2) - round(queryLast.sigmaVar_vol, 2), 2)
        dic['sigmaPnl_vol_Change'] = round(round(query.sigmaPnl_vol, 2) - round(queryLast.sigmaPnl_vol, 2), 2)

        if query.cAmt_fund is None:
            dic['cAmt_fund'] = '无数据'
            dic['cAmt_fund_Change'] = ''
        else:
            dic['cAmt_fund'] = round(query.cAmt_fund, 2)
            dic['cAmt_fund_Change'] = round(round(query.cAmt_fund, 2) - round(queryLast.cAmt_fund, 2), 2)
        dic['cCashDelta_fund'] = round(query.cCashDelta_fund, 2)
        dic['cVar_fund'] = round(query.cVar_fund, 2)
        if query.cPnl_fund is None:
            dic['cPnl_fund'] = '无数据'
            dic['cPnl_fund_Change'] = ''
        else:
            dic['cPnl_fund'] = round(query.cPnl_fund, 2)
            if queryLast.cPnl_fund is None:
                dic['cPnl_fund_Change'] = round(round(query.cPnl_fund, 2) - 0.0)
            else:
                dic['cPnl_fund_Change'] = round(round(query.cPnl_fund, 2) - round(queryLast.cPnl_fund, 2), 2)
        dic['cCashDelta_fund_Change'] = round(round(query.cCashDelta_fund, 2) - round(queryLast.cCashDelta_fund, 2), 2)
        dic['cVar_fund_Change'] = round(round(query.cVar_fund, 2) - round(queryLast.cVar_fund, 2), 2)

        if query.cAmt_basic is None:
            dic['cAmt_basic'] = '无数据'
            dic['cAmt_basic_Change'] = ''
        else:
            dic['cAmt_basic'] = round(query.cAmt_basic, 2)
            dic['cAmt_basic_Change'] = round(round(query.cAmt_basic, 2) - round(queryLast.cAmt_basic, 2), 2)
        dic['cCashDelta_basic'] = round(query.cCashDelta_basic, 2)
        dic['cVar_basic'] = round(query.cVar_basic, 2)
        if query.cPnl_basic is None:
            dic['cPnl_basic'] = '无数据'
            dic['cPnl_basic_Change'] = ''
        else:
            dic['cPnl_basic'] = round(query.cPnl_basic, 2)
            if queryLast.cPnl_basic is None:
                dic['cPnl_basic_Change'] = round(query.cPnl_basic, 2)
            else:
                dic['cPnl_basic_Change'] = round(round(query.cPnl_basic, 2) - round(queryLast.cPnl_basic, 2), 2)
        dic['cCashDelta_basic_Change'] = round(round(query.cCashDelta_basic, 2) - round(queryLast.cCashDelta_basic, 2),
                                               2)
        dic['cVar_basic_Change'] = round(round(query.cVar_basic, 2) - round(queryLast.cVar_basic, 2), 2)
        financeData = dailyFinanceData.objects.filter(date=date).first()
        dic['netEquity'] = round(financeData.netEquity, 0)
        dic['netEAratio'] = round(financeData.netEAratio * 100, 2)
        dic['coverRatio'] = round(financeData.coverRatio * 100, 2)

        dic['cashAmt'] = financeData.cashAmt
        dic['cashNum'] = financeData.cashNum
        dic['cashQuartPnl'] = round(financeData.cashQuartPnl, 2)
        dic['cashYearPnl'] = round(financeData.cashYearPnl, 2)
        dic['cashCumPnl'] = round(financeData.cashCumPnl, 2)

        dic['productAmt_rm'] = financeData.productAmt
        dic['productNum_rm'] = financeData.productNum
        dic['productYearPnl_rm'] = round(financeData.productYearPnl, 2)
        dic['productCumPnl_rm'] = round(financeData.productCumPnl, 2)


        year = datetime.strptime(date, "%Y-%m-%d").year
        pnl = fundPnlInfo.objects.filter(date=date).all()
        dic['productNum'] = len(pnl)
        dic['productAmt'] = round(
            (pnl.aggregate(Sum('buyCashAmount')).get('buyCashAmount__sum') - pnl.aggregate(
                Sum('sellCost')).get('sellCost__sum')), 2) / 10000

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

        productData = productDailyReport.objects.filter(date=date).all()
        dic['totalAmount'] = round(productData.aggregate(Sum('totalEquity')).get('totalEquity__sum') / 10000, 2)
        dic['selfAmount'] = round(
            productData.filter(type__contains='主动管理').aggregate(Sum('totalEquity')).get('totalEquity__sum') / 10000, 2)
        dic['alertNum'] = len(productData.filter(~Q(alertRisk='正常')).all())
        dic['cleanNum'] = len(productData.filter(~Q(cleanRisk='正常')).all())

        reportData = rmDailyReport.objects.filter(date=date).first()
        dic['year'] = date[:4]
        dic['closePos'] = reportData.closePos
        dic['overLoss'] = reportData.overLoss
        dic['yearOverLoss'] = reportData.yearOverLoss
        dic['overRisk'] = reportData.overRisk
        dic['importantText'] = reportData.importantText
        dic['limitText'] = reportData.limitText
        dic['totalNum'] = reportData.totalNum
        dic['yearNum'] = reportData.yearNum
        if reportData.nonInvestAmount == '' or reportData.nonInvestAmount is None:
            dic['productAvailableAmount'] = '--'
        else:
            dic['productAvailableAmount'] = reportData.nonInvestAmount
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


def productEchartsView(request):
    params = request.GET
    print(params)
    page = params.get('page', 1)
    limit = params.get('limit', 10)
    date = params.get("date", None)

    dict = {}
    dateList = []
    exposureList = []
    pnlList = []
    fundList = []
    if date:
        dataList = deruisectordata.objects.filter(date__lte=date).order_by('-date').all()[:252]
        for data in dataList:
            dateList.append(data.date.strftime("%Y-%m-%d"))
            exposureList.append(data.totalCashDelta)
            pnlList.append(data.totalPnl)
            fundList.append(data.otcAmt + data.ommAmt + data.sigmaAmt + data.cAmt)
        dateList.reverse()
        exposureList.reverse()
        pnlList.reverse()
        fundList.reverse()
        dict['date'] = dateList
        dict['exposure'] = exposureList
        dict['pnl'] = pnlList
        dict['fund'] = fundList

        result = {
            "code": 2000,
            "msg": "查询成功",
            "data": dict
        }
    else:
        result = {
            "code": 0,
            "msg": "无数据",
            "data": None
        }
    return JsonResponse(result)


def getSpecialCreidtInfo(request):
    today = datetime.today()
    params = request.GET
    date = params.get("date")  # 前端传入的时间
    ''':param
        1.判断前端是否传入时间
        2.如果没有传入时间,则使用今天
        3.传入时间,就根据传入时间查询
    '''
    if date is None or date == "":
        project_date = today.strftime("%Y-%m-%d")
    else:
        project_date = datetime.strptime(date, "%Y-%m-%d").strftime("%Y-%m-%d")

    queryset = deruiCreditData.objects.filter(date=project_date).values()

    results = {
        "total": 0,
        "data": [],
        "specialCreditData": []

    }
    specialCreditData = []
    for query in queryset:
        dicts = {
            "date": project_date,
            "sector": '',
            "name": '',
            "amt": 0,
            "deadline": project_date,
        }
        dicts['date'] = query.get('date').strftime("%Y-%m-%d")
        dicts['sector'] = query.get('sector') + '业务'
        dicts['name'] = query.get('name').replace('-', '<br>')
        dicts['amt'] = round(query.get('amt') / 10000, 2)
        dicts['deadline'] = query.get('deadline').strftime("%Y-%m-%d")

        # 将数据添加到返回给前端的列表中
        specialCreditData.append(dicts)

    results['total'] = len(specialCreditData)
    results['specialCreditData'] = specialCreditData

    return JsonResponse({
        "code": 0,
        "msg": "成功",
        "data": results,
        "total": 0
    })


def getDoubleWeeklyData(request):
    params = request.GET
    print(params)
    date = params.get("date", None)

    dataList = []
    if date:

        query = deruiLimitData.objects.filter(date=date).first()

        dic = {}
        dic['date'] = str(date[:4]) + '年' + str(int(date[5:7])) + '月' + str(int(date[8:])) + '日'
        dic['reportDate'] = str(datetime.today().year) + '年' + str(datetime.today().month) + '月' + str(
            datetime.today().day) + '日'

        dic['l1_assetAmt'] = round(query.l1_assetAmt * 100, 2)
        dic['l1_creditAmt_nonSecBank_usable'] = round(query.l1_creditAmt_nonSecBank_usable * 10000, 2)
        dic['l1_creditAmt_nonSecBank_used'] = round(query.l1_creditAmt_nonSecBank_used * 10000, 2)
        dic['l1_creditAmt_secBank_usable'] = round(query.l1_creditAmt_secBank_usable * 10000, 2)
        dic['l1_creditAmt_secBank_used'] = round(query.l1_creditAmt_secBank_used * 10000, 2)

        dic['l2_otc_creditAmt_nonSecBank'] = round(query.l2_otc_creditAmt_nonSecBank * 10000, 2)
        dic['l2_otc_creditAmt_secBank'] = round(query.l2_otc_creditAmt_secBank * 10000, 2)
        dic['l2_c_creditAmt_usable'] = round(query.l2_c_creditAmt_usable * 10000, 2)
        dic['l2_c_creditAmt_used'] = round(query.l2_c_creditAmt_used * 10000, 2)

        query = deruisectordata.objects.filter(date=date).first()
        dic['totalCashDelta'] = round(query.totalCashDelta, 2)
        dic['totalVar'] = round(query.totalVar, 2)
        dic['totalPnl'] = round(query.totalPnl, 2)
        dic['totalAmt'] = round(
            round(query.otcAmt, 2) + round(query.ommAmt, 2) + round(query.sigmaAmt, 2) + round(query.cAmt, 2), 2)

        dic['otcAmt'] = round(query.otcAmt, 2)
        dic['otcCashDelta'] = round(query.otcCashDelta, 2)
        dic['otcVar'] = round(query.otcVar, 2)
        dic['otcPnl'] = round(query.otcPnl, 2)

        dic['ommAmt'] = round(query.ommAmt, 2)
        dic['ommCashDelta'] = round(query.ommCashDelta, 2)
        dic['ommVar'] = round(query.ommVar, 2)
        dic['ommPnl'] = round(query.ommPnl, 2)

        dic['productInvestAmt'] = round(query.sigmaAmt_pro, 2)
        dic['productCashDelta'] = round(query.sigmaCashDelta_pro, 2)
        dic['productVar'] = round(query.sigmaVar_pro, 2)
        dic['productPnl'] = round(query.sigmaPnl_pro, 2)

        dic['sigmaAmt'] = round(query.sigmaAmt_vol, 2)
        dic['sigmaCashDelta'] = round(query.sigmaCashDelta_vol, 2)
        dic['sigmaVar'] = round(query.sigmaVar_vol, 2)
        dic['sigmaPnl'] = round(query.sigmaPnl_vol, 2)

        dic['cAmt'] = round(query.cAmt, 2)
        dic['cCashDelta'] = round(query.cCashDelta, 2)
        dic['cVar'] = round(query.cVar, 2)
        dic['cPnl'] = round(query.cPnl, 2)

        if query.ommBack is None:
            dic['ommBack'] = 0
        else:
            dic['ommBack'] = round(query.ommBack, 2)

        financeData = dailyFinanceData.objects.filter(date=date).first()
        dic['netEquity'] = round(financeData.netEquity, 0)
        dic['netEAratio'] = round(financeData.netEAratio * 100, 2)
        dic['coverRatio'] = round(financeData.coverRatio * 100, 2)

        dic['cashAmt'] = financeData.cashAmt
        dic['cashNum'] = financeData.cashNum
        dic['cashYearPnl'] = round(financeData.cashYearPnl, 2)

        dic['productAmt_rm'] = financeData.productAmt
        dic['productNum_rm'] = financeData.productNum
        dic['productYearPnl_rm'] = round(financeData.productYearPnl, 2)
        dic['productCumPnl_rm'] = round(financeData.productCumPnl, 2)

        productData = fundBasicInfo.objects.all()
        dic['productAvailableAmount'] = round(
            productData.aggregate(Sum('investableAmount')).get('investableAmount__sum'), 2) / 10000

        year = datetime.strptime(date, "%Y-%m-%d").year
        pnl = fundPnlInfo.objects.filter(date=date).all()
        dic['productNum'] = len(pnl)
        dic['productAmt'] = round(
            (pnl.aggregate(Sum('buyCashAmount')).get('buyCashAmount__sum') - pnl.aggregate(
                Sum('sellCost')).get('sellCost__sum')), 2) / 10000

        pnl = fundPnlInfo.objects.filter(date__lte=date).order_by("-date").all()
        pnlYear = pnl.filter(date__year=year).aggregate(Sum('todayPnl'))
        if pnlYear.get('todayPnl__sum') is None:
            dic['yearPnl'] = 0.
        else:
            dic['yearPnl'] = round(pnlYear.get('todayPnl__sum') / 10000, 2)

        productData = productDailyReport.objects.filter(date=date).all()
        dic['totalAmount'] = round(productData.aggregate(Sum('totalEquity')).get('totalEquity__sum') / 10000, 2)
        dic['selfAmount'] = round(
            productData.filter(type__contains='主动管理').aggregate(Sum('totalEquity')).get('totalEquity__sum') / 10000, 2)
        dic['alertNum'] = len(productData.filter(~Q(alertRisk='正常')).all())
        dic['cleanNum'] = len(productData.filter(~Q(cleanRisk='正常')).all())

        reportData = rmDoubleWeeklyReport.objects.filter(date=date).first()
        dic['year'] = date[:4]
        dic['closePos'] = reportData.closePos
        dic['overLoss'] = reportData.overLoss
        dic['yearOverLoss'] = reportData.yearOverLoss
        dic['marginCall'] = reportData.marginCall

        dic['riskSupText'] = reportData.riskSupText
        dic['limitText'] = reportData.limitText
        dic['authText'] = reportData.authText
        dic['importantRiskText'] = reportData.importantRiskText

        dic['totalNum'] = reportData.totalNum
        dic['yearNum'] = reportData.yearNum

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