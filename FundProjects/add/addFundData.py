# -*- coding: utf-8 -*-

"""
@author: zzj

@contact: QQ:10996784

@Created on: 2020/10/13 007 11:28
"""

from django.http import JsonResponse
from django.shortcuts import redirect

from FundProjects.models import fundBasicInfo, fundPnlInfo, tradeInfo, totalAmountInfo, fundNetValueInfo, \
    confirmNetValueInfo
from datetime import datetime
import pandas as pd

import FundProjects.method.fundpnl as fundpnl

from django.views.decorators.csrf import csrf_exempt

hisSpecialProductList = ['钢铁1号', '星光璀璨1号', '和誉3号', '银河期货大宗商品1号', '权银河旗舰3/4号', '银河人保安心盛世1号', '融宝16号', '华澳臻智稳健1期',
                         '权银河恒星1号']
nonInvestProductList = ['权银河旗舰3/4号', '银河人保安心盛世1号', '融宝16号', '华澳臻智稳健1期', '权银河恒星1号']



# 产品数据，新增处理

# 新增申购、赎回
def addTradeInfo(request):
    tradeType = request.POST.get('type', "")
    applyDate = request.POST.get('applyDate', "")
    applyDate = datetime.strptime(applyDate, "%Y-%m-%d")
    confirmDate = request.POST.get('confirmDate', "")
    confirmDate = datetime.strptime(confirmDate, "%Y-%m-%d")
    isHis = request.POST.get('isHis', "")
    if isHis == 'on':
        date = request.POST.get('dataDate', "")
    else:
        date = datetime.today()
    productName = request.POST.get('productName', "")

    tradeShare = float(request.POST.get('tradeShare', ""))
    unitNet = float(request.POST.get('unitNet', ""))
    fee = request.POST.get('fee', "")
    tradeAmount = float(request.POST.get('tradeAmount', ""))
    cost = request.POST.get('cost', "")
    if fee == '':
        fee = 0
    else:
        fee = float(fee)
    if cost == '':
        cost = 0
    else:
        cost = float(cost)

    index = tradeInfo.objects.order_by("-index").values()[0].get('index') + 1
    add_trade = tradeInfo(index=index,
                          date=date,
                          tradeType=tradeType,
                          applyDate=applyDate,
                          confirmDate=confirmDate,
                          productName=productName,

                          tradeShare=tradeShare,
                          unitNet=unitNet,
                          fee=fee,
                          tradeAmount=tradeAmount,
                          cost=cost,
                          )
    add_trade.save()

    if tradeType == '申购':
        investableAmount = fundBasicInfo.objects.filter(productName=productName).values()[0].get('investableAmount')
        investableAmount = investableAmount - tradeAmount
        fundBasicInfo.objects.filter(productName=productName).update(investableAmount=investableAmount)
        fundBasicInfo.objects.filter(productName=productName).update(status='在投')
        fundBasicInfo.objects.filter(productName=productName).update(date=datetime.today())

    if tradeType == '赎回':
        queryset = totalAmountInfo.objects.order_by("-index").values()[0]
        print(queryset)
        index = queryset.get('index') + 1
        totalAmt = float(queryset['totalAmount']),
        newUsed = 0,
        usedAmount = float(queryset['usedAmount']),
        newBack = float(queryset['newBack']) + cost,
        usableAmount = float(queryset['usableAmount']) + cost
        demo = productName + '产品赎回'
        add_Amount = totalAmountInfo(index=index,
                                     confirmDate=confirmDate,
                                     totalAmount=totalAmt[0],
                                     newUsed=newUsed[0],
                                     usedAmount=usedAmount[0],
                                     newBack=newBack[0],
                                     usableAmount=usableAmount,
                                     demo=demo
                                     )
        add_Amount.save()
        totalAmount = fundBasicInfo.objects.filter(productName=productName).values()[0].get('totalAmount')
        redeemCost = fundBasicInfo.objects.filter(productName=productName).values()[0].get('redeemCost')
        redeemCost = redeemCost + cost
        investableAmount = fundBasicInfo.objects.filter(productName=productName).values()[0].get('investableAmount')
        fundBasicInfo.objects.filter(productName=productName).update(redeemCost=redeemCost)
        if redeemCost == (totalAmount - investableAmount):
            fundBasicInfo.objects.filter(productName=productName).update(date=datetime.today())
            fundBasicInfo.objects.filter(productName=productName).update(status='已结束')
            if redeemCost != totalAmount:
                fundBasicInfo.objects.filter(productName=productName).update(investableAmount=0.0)
                add_Amount = totalAmountInfo(index=index + 1,
                                             confirmDate=confirmDate,
                                             totalAmount=totalAmt,
                                             newUsed=0.,
                                             usedAmount=usedAmount,
                                             newBack=0.,
                                             usableAmount=usableAmount + investableAmount,
                                             demo=productName + '产品结束，未使用额度返还至剩余额度'
                                             )
                add_Amount.save()

    return redirect('add/tradeinfo')


# 新增产品
def addProductInfo(request):
    confirmDate1 = request.POST.get('confirmDate1', "")
    confirmDate1 = datetime.strptime(confirmDate1, "%Y-%m-%d")
    confirmDate2 = request.POST.get('confirmDate2', "")
    confirmDate2 = datetime.strptime(confirmDate2, "%Y-%m-%d")
    productName = request.POST.get('productName', "")
    productFullName = request.POST.get('productFullName', "")

    productType1 = request.POST.get('productType1', "")
    productType2 = request.POST.get('productType2', "")
    productType3 = request.POST.get('productType3', "")
    strategy = request.POST.get('strategy', "")
    senior = request.POST.get('senior', "")
    redeemLimit = request.POST.get('redeemLimit', "")
    if senior == 'on':
        senior = '1'
    else:
        senior = '0'
    if redeemLimit == 'on':
        redeemLimit = '是'
    else:
        redeemLimit = '否'

    manager = request.POST.get('manager', "")
    status = request.POST.get('status', "")
    if status == 'on':
        status = '未结束'
    else:
        status = '已结束'
    sector = request.POST.get('sector', "")

    totalAmount = float(request.POST.get('totalAmount', 0.))
    alertLimit = request.POST.get('alertLimit', 0.)
    if alertLimit == '':
        alertLimit = 0.
    else:
        alertLimit = float(alertLimit)
    cleanLimit = request.POST.get('cleanLimit', 0.)
    if cleanLimit == '':
        cleanLimit = 0.
    else:
        cleanLimit = float(cleanLimit)

    preProvideFundDate = request.POST.get('preProvideFundDate', "")
    preInvestDuration = request.POST.get('preInvestDuration', "")
    openDay = request.POST.get('openDay', "")
    temporaryOpen = request.POST.get('temporaryOpen', "")
    if temporaryOpen == 'on':
        temporaryOpen = '是'
    else:
        temporaryOpen = '否'

    rmAlertLimit = request.POST.get('rmAlertLimit', 0.)
    if rmAlertLimit == '':
        rmAlertLimit = 0.
    else:
        rmAlertLimit = float(rmAlertLimit)
    rmCleanLimit = request.POST.get('rmCleanLimit', 0.)
    if rmCleanLimit == '':
        rmCleanLimit = 0.
    else:
        rmCleanLimit = float(rmCleanLimit)

    rmRules = request.POST.get('rmRules', "")
    investPurpose = request.POST.get('investPurpose', "")
    selfManage = request.POST.get('selfManage', "")
    if selfManage == 'on':
        selfManage = '是'
    else:
        selfManage = '否'
    investAdvisor = request.POST.get('investAdvisor', "")
    if investAdvisor == 'on':
        investAdvisor = '是'
    else:
        investAdvisor = '否'
    synergy = request.POST.get('synergy', "")
    if synergy == 'on':
        synergy = '是'
    else:
        synergy = '否'
    thirdParty = request.POST.get('thirdParty', "")
    synergyAmount = request.POST.get('synergyAmount', 0.)
    if synergyAmount == '':
        synergyAmount = 0.
    else:
        synergyAmount = float(synergyAmount)

    demo = request.POST.get('demo', "")
    productList = fundBasicInfo.objects.filter(status__in=['未结束', '在投']).values('productName')

    # 如果存在修改审批额度
    if {'productName': productName} in productList:
        totalAmountOld = fundBasicInfo.objects.filter(productName=productName).values()[0].get('totalAmount')
        totalAmountChange = totalAmount - totalAmountOld
        # 修改审批额度
        if totalAmountChange != 0:
            fundBasicInfo.objects.filter(productName=productName).update(date=datetime.today())
            fundBasicInfo.objects.filter(productName=productName).update(totalAmount=totalAmount)
            investableAmountOld = fundBasicInfo.objects.filter(productName=productName).values()[0].get(
                'investableAmount')
            investableAmountNew = investableAmountOld + totalAmountChange
            fundBasicInfo.objects.filter(productName=productName).update(investableAmount=investableAmountNew)
            demoOld = fundBasicInfo.objects.filter(productName=productName).values()[0].get('demo')
            demoNew = demoOld + '*' + confirmDate2.strftime("%Y-%m-%d") + '将原审批额度' + str(totalAmountOld) + '修改至' + str(
                totalAmount) + '*' + demo
            fundBasicInfo.objects.filter(productName=productName).update(demo=demoNew)
            queryset = totalAmountInfo.objects.order_by("-index").values()[0]
            # 修改额度，增加额度表
            if status != '已结束':
                totalAmt = float(queryset['totalAmount']),
                newUsed = totalAmountChange,
                usedAmount = float(queryset['usedAmount']) + newUsed,
                newBack = float(queryset['newBack']),
                usableAmount = float(queryset['usableAmount']) - newUsed,
                demo = productName + '额度修改',
                index = queryset.get('index') + 1
                add_Amount = totalAmountInfo(index=index,
                                             confirmDate=confirmDate2,
                                             totalAmount=totalAmt[0],
                                             newUsed=newUsed[0],
                                             usedAmount=usedAmount[0],
                                             newBack=newBack[0],
                                             usableAmount=usableAmount,
                                             demo=demo
                                             )
                add_Amount.save()
                redeemCost = fundBasicInfo.objects.filter(productName=productName).values()[0].get('redeemCost')
                if totalAmount == 0 or redeemCost == (totalAmount - investableAmountNew):
                    fundBasicInfo.objects.filter(productName=productName).update(status='已结束')
        # fundBasicInfo.objects.filter(productName=productName).update(confirmDate1=confirmDate1)
        # fundBasicInfo.objects.filter(productName=productName).update(confirmDate2=confirmDate2)
        # fundBasicInfo.objects.filter(productName=productName).update(productType1=productType1)
        # fundBasicInfo.objects.filter(productName=productName).update(productType2=productType2)
        # fundBasicInfo.objects.filter(productName=productName).update(productType3=productType3)
        #
        # fundBasicInfo.objects.filter(productName=productName).update(strategy=strategy)
        # fundBasicInfo.objects.filter(productName=productName).update(senior=senior)
        # fundBasicInfo.objects.filter(productName=productName).update(redeemLimit=redeemLimit)
        # fundBasicInfo.objects.filter(productName=productName).update(manager=manager)
        # fundBasicInfo.objects.filter(productName=productName).update(status=status)
        # fundBasicInfo.objects.filter(productName=productName).update(sector=sector)
        #
        # fundBasicInfo.objects.filter(productName=productName).update(alertLimit=alertLimit)
        # fundBasicInfo.objects.filter(productName=productName).update(cleanLimit=cleanLimit)
        # fundBasicInfo.objects.filter(productName=productName).update(preProvideFundDate=preProvideFundDate)
        # fundBasicInfo.objects.filter(productName=productName).update(preInvestDuration=preInvestDuration)
        # fundBasicInfo.objects.filter(productName=productName).update(openDay=openDay)
        # fundBasicInfo.objects.filter(productName=productName).update(temporaryOpen=temporaryOpen)
        #
        # fundBasicInfo.objects.filter(productName=productName).update(rmAlertLimit=rmAlertLimit)
        # fundBasicInfo.objects.filter(productName=productName).update(rmCleanLimit=rmCleanLimit)
        #
        #
        # fundBasicInfo.objects.filter(productName=productName).update(rmRules=rmRules)
        # fundBasicInfo.objects.filter(productName=productName).update(investPurpose=investPurpose)
        # fundBasicInfo.objects.filter(productName=productName).update(selfManage=selfManage)
        # fundBasicInfo.objects.filter(productName=productName).update(investAdvisor=investAdvisor)
        # fundBasicInfo.objects.filter(productName=productName).update(synergy=synergy)
        # fundBasicInfo.objects.filter(productName=productName).update(thirdParty=thirdParty)
        # fundBasicInfo.objects.filter(productName=productName).update(synergyAmount=synergyAmount)
        # demoOld = fundBasicInfo.objects.filter(productName=productName).values()[0].get('demo')
        # demoNew = demoOld + '*' + demo
        # fundBasicInfo.objects.filter(productName=productName).update(demo=demoNew)
    else:
        index = fundBasicInfo.objects.order_by("-index").values()[0].get('index') + 1
        add_product = fundBasicInfo(index=index,
                                    confirmDate1=confirmDate1,
                                    confirmDate2=confirmDate2,
                                    productName=productName,
                                    productFullName=productFullName,

                                    productType1=productType1,
                                    productType2=productType2,
                                    productType3=productType3,
                                    strategy=strategy,
                                    senior=senior,
                                    redeemLimit=redeemLimit,
                                    manager=manager,
                                    status=status,
                                    sector=sector,

                                    alertLimit=alertLimit,
                                    cleanLimit=cleanLimit,
                                    investableAmount=totalAmount,
                                    totalAmount=totalAmount,
                                    redeemCost=0.,

                                    preProvideFundDate=preProvideFundDate,
                                    preInvestDuration=preInvestDuration,
                                    openDay=openDay,
                                    temporaryOpen=temporaryOpen,

                                    rmAlertLimit=rmAlertLimit,
                                    rmCleanLimit=rmCleanLimit,

                                    rmRules=rmRules,
                                    investPurpose=investPurpose,
                                    selfManage=selfManage,
                                    investAdvisor=investAdvisor,
                                    synergy=synergy,
                                    thirdParty=thirdParty,
                                    synergyAmount=synergyAmount,

                                    demo=demo
                                    )
        add_product.save()

        queryset = totalAmountInfo.objects.order_by("-index").values()[0]
        if status == '未结束':
            totalAmt = float(queryset['totalAmount']),
            newUsed = totalAmount,
            usedAmount = float(queryset['usedAmount']) + totalAmount,
            newBack = float(queryset['newBack']),
            usableAmount = float(queryset['usableAmount']) - totalAmount
            demo = '审批新产品' + productName
            index = queryset.get('index') + 1
            add_Amount = totalAmountInfo(index=index,
                                         confirmDate=confirmDate2,
                                         totalAmount=totalAmt[0],
                                         newUsed=newUsed[0],
                                         usedAmount=usedAmount[0],
                                         newBack=newBack[0],
                                         usableAmount=usableAmount,
                                         demo=demo
                                         )
            add_Amount.save()
        else:
            fundBasicInfo.objects.filter(productName=productName).update(investableAmount=0)
            fundBasicInfo.objects.filter(productName=productName).update(redeemCost=totalAmount)

    return redirect('add/newproduct')


# 上传文件方式 新增产品
def postProduct(request):
    """批量导入数据"""
    # if request.method == "POST":
    f = request.FILES.get('file')
    df = pd.read_excel(f)
    df = df.fillna('')
    queryset = fundBasicInfo.objects.order_by("-index").values()[0]
    index = queryset.get('index')

    for i in range(len(df)):
        data = df.iloc[i]

        if type(data['投委会通过日期']) != datetime and type(data['投委会通过日期']) != pd.Timestamp:
            confirmDate1 = datetime.strptime(str(data['投委会通过日期']), "%Y%m%d")
        else:
            confirmDate1 = data['投委会通过日期']
        if type(data['总办会通过日期']) != datetime and type(data['总办会通过日期']) != pd.Timestamp:
            confirmDate2 = datetime.strptime(str(data['总办会通过日期']), "%Y%m%d")
        else:
            confirmDate2 = data['总办会通过日期']
        productName = data['产品名称']
        productFullName = data['产品全名']

        productType1 = data['产品类型1']
        productType2 = data['产品类型2']
        productType3 = data['产品类型3']
        strategy = data['产品策略']
        senior = data['是否为次级']
        redeemLimit = data['赎回是否受限']
        manager = data['管理人']
        status = data['状态']
        sector = data['项目负责部门及人员']

        if data['预警线'] == '':
            alertLimit = 0
        else:
            alertLimit = float(data['预警线'])
        if data['清盘线'] == '':
            cleanLimit = 0
        else:
            cleanLimit = float(data['清盘线'])
        totalAmount = round(float(data['累计审批额度']), 2)

        preProvideFundDate = data['拟出资时间']
        preInvestDuration = data['拟投资期限']
        openDay = data['开放日']
        temporaryOpen = data['是否有临开']

        if data['风控预警线'] == '':
            rmAlertLimit = 0
        else:
            rmAlertLimit = float(data['风控预警线'])
        if data['风控止损线'] == '':
            rmCleanLimit = 0
        else:
            rmCleanLimit = float(data['风控止损线'])

        rmRules = data['风控条款说明']
        investPurpose = data['投资目的']
        selfManage = data['是否为公司自主管理产品']
        investAdvisor = data['公司是否担任投顾']
        synergy = data['是否涉及与证券协同']
        thirdParty = data['第三方']
        if data['拟协同业务规模'] == '':
            synergyAmount = 0
        else:
            synergyAmount = float(data['拟协同业务规模'])

        if data['备注'] is None:
            demo = ''
        else:
            demo = data['备注']
        productList = fundBasicInfo.objects.values('productName')
        # 如果存在修改审批额度和其他字段
        if {'productName': productName} in productList:
            fundBasicInfo.objects.filter(productName=productName).update(demo=demo)
            totalAmountOld = fundBasicInfo.objects.filter(productName=productName).values()[0].get('totalAmount')
            totalAmountChange = totalAmount - totalAmountOld
            # 修改审批额度
            if totalAmountChange != 0:
                fundBasicInfo.objects.filter(productName=productName).update(date=datetime.today())
                fundBasicInfo.objects.filter(productName=productName).update(totalAmount=totalAmount)
                investableAmountOld = fundBasicInfo.objects.filter(productName=productName).values()[0].get(
                    'investableAmount')
                investableAmountNew = investableAmountOld + totalAmountChange
                fundBasicInfo.objects.filter(productName=productName).update(investableAmount=investableAmountNew)
                demoOld = fundBasicInfo.objects.filter(productName=productName).values()[0].get('demo')
                if demoOld is None:
                    demoOld = ''
                demoNew = demoOld + '*' + confirmDate2.strftime("%Y-%m-%d") + '将原审批额度' + str(
                    totalAmountOld) + '修改至' + str(totalAmount) + '*' + demo
                fundBasicInfo.objects.filter(productName=productName).update(demo=demoNew)
                queryset = totalAmountInfo.objects.order_by("-index").values()[0]
                # 修改额度，增加额度表
                if status == '未结束':
                    totalAmt = float(queryset['totalAmount']),
                    newUsed = totalAmountChange,
                    usedAmount = float(queryset['usedAmount']) + newUsed,
                    newBack = float(queryset['newBack']),
                    usableAmount = float(queryset['usableAmount']) - newUsed,
                    demo = productName + '额度修改',
                    index = queryset.get('index') + 1
                    add_Amount = totalAmountInfo(index=index,
                                                 confirmDate=confirmDate2,
                                                 totalAmount=totalAmt[0],
                                                 newUsed=newUsed[0],
                                                 usedAmount=usedAmount[0],
                                                 newBack=newBack[0],
                                                 usableAmount=usableAmount,
                                                 demo=demo
                                                 )
                    add_Amount.save()
                    redeemCost = fundBasicInfo.objects.filter(productName=productName).values()[0].get('redeemCost')
                    if totalAmount == 0 or redeemCost == (totalAmount - investableAmountNew):
                        fundBasicInfo.objects.filter(productName=productName).update(status='已结束')
            fundBasicInfo.objects.filter(productName=productName).update(confirmDate1=confirmDate1)
            fundBasicInfo.objects.filter(productName=productName).update(confirmDate2=confirmDate2)
            fundBasicInfo.objects.filter(productName=productName).update(productType1=productType1)
            fundBasicInfo.objects.filter(productName=productName).update(productType2=productType2)
            fundBasicInfo.objects.filter(productName=productName).update(productType3=productType3)

            fundBasicInfo.objects.filter(productName=productName).update(strategy=strategy)
            fundBasicInfo.objects.filter(productName=productName).update(senior=senior)
            fundBasicInfo.objects.filter(productName=productName).update(redeemLimit=redeemLimit)
            fundBasicInfo.objects.filter(productName=productName).update(manager=manager)
            fundBasicInfo.objects.filter(productName=productName).update(status=status)
            fundBasicInfo.objects.filter(productName=productName).update(sector=sector)

            fundBasicInfo.objects.filter(productName=productName).update(alertLimit=alertLimit)
            fundBasicInfo.objects.filter(productName=productName).update(cleanLimit=cleanLimit)
            fundBasicInfo.objects.filter(productName=productName).update(preProvideFundDate=preProvideFundDate)
            fundBasicInfo.objects.filter(productName=productName).update(preInvestDuration=preInvestDuration)
            fundBasicInfo.objects.filter(productName=productName).update(openDay=openDay)
            fundBasicInfo.objects.filter(productName=productName).update(temporaryOpen=temporaryOpen)

            fundBasicInfo.objects.filter(productName=productName).update(rmAlertLimit=rmAlertLimit)
            fundBasicInfo.objects.filter(productName=productName).update(rmCleanLimit=rmCleanLimit)

            fundBasicInfo.objects.filter(productName=productName).update(rmRules=rmRules)
            fundBasicInfo.objects.filter(productName=productName).update(investPurpose=investPurpose)
            fundBasicInfo.objects.filter(productName=productName).update(selfManage=selfManage)
            fundBasicInfo.objects.filter(productName=productName).update(investAdvisor=investAdvisor)
            fundBasicInfo.objects.filter(productName=productName).update(synergy=synergy)
            fundBasicInfo.objects.filter(productName=productName).update(thirdParty=thirdParty)
            fundBasicInfo.objects.filter(productName=productName).update(synergyAmount=synergyAmount)

        else:
            index = index + 1
            add_product = fundBasicInfo(index=index,
                                        confirmDate1=confirmDate1,
                                        confirmDate2=confirmDate2,
                                        productName=productName,
                                        productFullName=productFullName,

                                        productType1=productType1,
                                        productType2=productType2,
                                        productType3=productType3,
                                        strategy=strategy,
                                        senior=senior,
                                        redeemLimit=redeemLimit,
                                        manager=manager,
                                        status=status,
                                        sector=sector,

                                        alertLimit=alertLimit,
                                        cleanLimit=cleanLimit,
                                        investableAmount=totalAmount,
                                        totalAmount=totalAmount,
                                        redeemCost=0.,

                                        preProvideFundDate=preProvideFundDate,
                                        preInvestDuration=preInvestDuration,
                                        openDay=openDay,
                                        temporaryOpen=temporaryOpen,

                                        rmAlertLimit=rmAlertLimit,
                                        rmCleanLimit=rmCleanLimit,

                                        rmRules=rmRules,
                                        investPurpose=investPurpose,
                                        selfManage=selfManage,
                                        investAdvisor=investAdvisor,
                                        synergy=synergy,
                                        thirdParty=thirdParty,
                                        synergyAmount=synergyAmount,

                                        demo=demo
                                        )
            add_product.save()

            queryset = totalAmountInfo.objects.order_by("-index").values()[0]
            print(queryset)
            if status == '未结束':
                totalAmt = float(queryset['totalAmount']),
                newUsed = totalAmount,
                usedAmount = float(queryset['usedAmount']) + totalAmount,
                newBack = float(queryset['newBack']),
                usableAmount = float(queryset['usableAmount']) - totalAmount
                demo = '审批新产品' + productName
                index = queryset.get('index') + 1
                add_Amount = totalAmountInfo(index=index,
                                             confirmDate=confirmDate2,
                                             totalAmount=totalAmt[0],
                                             newUsed=newUsed[0],
                                             usedAmount=usedAmount[0],
                                             newBack=newBack[0],
                                             usableAmount=usableAmount,
                                             demo=demo
                                             )
                add_Amount.save()

    return JsonResponse({
        "code": 0,
        "msg": "成功",
        "data": {}
    })


# 修改额度表
def modifyAmtInfo(request):
    confirmDate = request.POST.get('confirmDate', "")
    if confirmDate is None or confirmDate == "":
        confirmDate = datetime.today()
    else:
        confirmDate = datetime.strptime(confirmDate, "%Y-%m-%d")

    totalAmount = float(request.POST.get('totalAmount', ""))

    queryset = totalAmountInfo.objects.order_by("-index").values()[0]
    print(queryset)
    newUsed = float(queryset['newUsed']),
    usedAmount = float(queryset['usedAmount']),
    newBack = float(queryset['newBack']),
    usableAmount = float(queryset['usableAmount']) + (totalAmount - float(queryset['totalAmount']))
    demo = '修改总办会审批额度'
    index = queryset.get('index') + 1
    add_Amount = totalAmountInfo(index=index,
                                 confirmDate=confirmDate,
                                 totalAmount=totalAmount,
                                 newUsed=newUsed[0],
                                 usedAmount=usedAmount[0],
                                 newBack=newBack[0],
                                 usableAmount=usableAmount,
                                 demo=demo
                                 )
    add_Amount.save()
    return redirect('add/modifyamt')


# 上传文件（净值数据）入库
@csrf_exempt
def postPnl(request):
    """批量导入数据"""
    # if request.method == "POST":
    f = request.FILES.get('file')
    df = pd.read_excel(f)

    date = df.iloc[0]['数据日期']
    if type(date) != datetime:
        date = datetime.strptime(str(int(date)), "%Y%m%d")
    queryset = fundBasicInfo.objects.filter(confirmDate2__lte=date).values()
    # 获取所有的产品名称，如果excel文件里有的，直接插入数据库
    # 如果文件里没有，但是状态为在投，获取上一日数据
    for query in queryset:
        productName = query.get('productName')
        status = query.get('status')
        if productName in df.产品名称.tolist():
            data = df.loc[df.产品名称 == productName]
            for i in range(len(data)):
                if str(data.iloc[i].数据日期) != 'nan':
                    if type(data.iloc[i]['数据日期']) != datetime:
                        date = datetime.strptime(str(int(data.iloc[i]['数据日期'])), "%Y%m%d")
                    else:
                        date = data.iloc[i]['数据日期']
                    productName = data.iloc[i]['产品名称']
                    netValue = data.iloc[i]['单位净值']
                    acNetValue = data.iloc[i]['累计净值']
                    demo = data.iloc[i]['备注']
                    index = fundNetValueInfo.objects.order_by("-index").values()[0].get('index') + 1
                    add_NetValue = fundNetValueInfo(index=index,
                                                    date=date,
                                                    productName=productName,
                                                    netValue=netValue,
                                                    acNetValue=acNetValue,
                                                    demo=demo
                                                    )
                    add_NetValue.save()

                    if str(data.iloc[i].真实日期) != 'nan':
                        if type(data.iloc[i]['真实日期']) != datetime:
                            date = datetime.strptime(str(int(data.iloc[i]['真实日期'])), "%Y%m%d")
                        else:
                            date = data.iloc[i]['真实日期']
                        productName = data.iloc[i]['产品名称']
                        netValue = data.iloc[i]['单位净值']
                        acNetValue = data.iloc[i]['累计净值']
                        demo = data.iloc[i]['备注']
                        if len(confirmNetValueInfo.objects.filter(productName=productName).filter(
                                date=date).values()) > 0:
                            confirmNetValueInfo.objects.filter(productName=productName).filter(date=date).update(
                                netValue=netValue)
                            confirmNetValueInfo.objects.filter(productName=productName).filter(date=date).update(
                                acNetValue=acNetValue)
                            confirmNetValueInfo.objects.filter(productName=productName).filter(date=date).update(
                                demo=demo)
                            confirmNetValueInfo.objects.filter(productName=productName).filter(date=date).update(
                                lastUpdateDate=datetime.today())
                        else:
                            index = confirmNetValueInfo.objects.order_by("-index").values()[0].get('index') + 1
                            add_NetValue = confirmNetValueInfo(index=index,
                                                               date=date,
                                                               productName=productName,
                                                               netValue=netValue,
                                                               acNetValue=acNetValue,
                                                               demo=demo
                                                               )
                            add_NetValue.save()
                else:
                    if type(data.iloc[i]['真实日期']) != datetime:
                        date = datetime.strptime(str(int(data.iloc[i]['真实日期'])), "%Y%m%d")
                    else:
                        date = data.iloc[i]['真实日期']
                    productName = data.iloc[i]['产品名称']
                    netValue = data.iloc[i]['单位净值']
                    acNetValue = data.iloc[i]['累计净值']
                    demo = data.iloc[i]['备注']
                    if len(confirmNetValueInfo.objects.filter(productName=productName).filter(date=date).values()) > 0:
                        confirmNetValueInfo.objects.filter(productName=productName).filter(date=date).update(
                            netValue=netValue)
                        confirmNetValueInfo.objects.filter(productName=productName).filter(date=date).update(
                            acNetValue=acNetValue)
                        confirmNetValueInfo.objects.filter(productName=productName).filter(date=date).update(
                            demo=demo)
                        confirmNetValueInfo.objects.filter(productName=productName).filter(date=date).update(
                            lastUpdateDate=datetime.today())
                    else:
                        index = confirmNetValueInfo.objects.order_by("-index").values()[0].get('index') + 1
                        add_confirmNetValue = confirmNetValueInfo(index=index,
                                                                  date=date,
                                                                  productName=productName,
                                                                  netValue=netValue,
                                                                  acNetValue=acNetValue,
                                                                  demo=demo
                                                                  )
                        add_confirmNetValue.save()
        else:
            if status == '在投':
                nvData = fundNetValueInfo.objects.filter(productName=productName, date__lte=date).order_by(
                    "-date").values()

                lastDate = nvData.first().get('date')
                nvData = nvData.filter(date=lastDate).order_by("-lastUpdateDate").first()
                netValue = nvData['netValue']
                acNetValue = nvData['acNetValue']
                index = index + 1
                add_NetValue = fundNetValueInfo(index=index,
                                                date=date,
                                                productName=productName,
                                                netValue=netValue,
                                                acNetValue=acNetValue,
                                                demo='无录入数据，自动取前一日净值'
                                                )
                add_NetValue.save()
    return JsonResponse({
        "code": 0,
        "msg": "成功",
        "data": {}
    })


def postPnlHis(request):
    """批量导入数据"""
    # if request.method == "POST":
    f = request.FILES.get('file')
    df = pd.read_excel(f)

    for i in range(len(df)):
        if str(df.iloc[i].数据日期) != 'nan':
            if type(df.iloc[i]['数据日期']) != datetime:
                date = datetime.strptime(str(int(df.iloc[i]['数据日期'])), "%Y%m%d")
            else:
                date = df.iloc[i]['数据日期']
            productName = df.iloc[i]['产品名称']
            netValue = df.iloc[i]['单位净值']
            acNetValue = df.iloc[i]['累计净值']
            demo = df.iloc[i]['备注']
            index = fundNetValueInfo.objects.order_by("-index").values()[0].get('index') + 1
            add_NetValue = fundNetValueInfo(index=index,
                                            date=date,
                                            productName=productName,
                                            netValue=netValue,
                                            acNetValue=acNetValue,
                                            demo=demo
                                            )
            add_NetValue.save()

        if str(df.iloc[i].真实日期) != 'nan':
            if type(df.iloc[i]['真实日期']) != datetime:
                date = datetime.strptime(str(int(df.iloc[i]['真实日期'])), "%Y%m%d")
            else:
                date = df.iloc[i]['真实日期']
            productName = df.iloc[i]['产品名称']
            netValue = df.iloc[i]['单位净值']
            acNetValue = df.iloc[i]['累计净值']
            demo = df.iloc[i]['备注']
            if len(confirmNetValueInfo.objects.filter(productName=productName).filter(date=date).values()) > 0:
                confirmNetValueInfo.objects.filter(productName=productName).filter(date=date).update(
                    netValue=netValue)
                confirmNetValueInfo.objects.filter(productName=productName).filter(date=date).update(
                    acNetValue=acNetValue)
                confirmNetValueInfo.objects.filter(productName=productName).filter(date=date).update(
                    demo=demo)
                confirmNetValueInfo.objects.filter(productName=productName).filter(date=date).update(
                    lastUpdateDate=datetime.today())
            else:
                index = confirmNetValueInfo.objects.order_by("-index").values()[0].get('index') + 1
                add_NetValue = confirmNetValueInfo(index=index,
                                                   date=date,
                                                   productName=productName,
                                                   netValue=netValue,
                                                   acNetValue=acNetValue,
                                                   demo=demo
                                                   )
                add_NetValue.save()

    return JsonResponse({
        "code": 0,
        "msg": "成功",
        "data": {}
    })


# 计算日报盈亏数据->入库
def calcPnlReport(request):
    today = request.POST.get("calcDate")  # 前端传入的时间,计算日期,默认为今日

    if today is None or today == "":
        today = datetime.today()  # 获取当前日期
        today = today.strftime("%Y-%m-%d")
    else:
        today = datetime.strptime(today, "%Y-%m-%d").strftime("%Y-%m-%d")

    date = request.POST.get("searchDate")  # 前端传入的时间,数据日期
    project_date = datetime.strptime(date, "%Y-%m-%d").strftime("%Y-%m-%d")

    productName = request.POST.get("productName")
    # 默认计算全部产品
    if productName == '' or productName is None:
        pnlData = fundPnlInfo.objects.filter(date=project_date).all()
        if len(pnlData) != 0:
            fundPnlInfo.objects.filter(date=project_date).all().delete()
        queryset = fundBasicInfo.objects.filter(status__in=['已结束', '在投'], confirmDate2__lte=date).values()
        for query in queryset:
            productName = query.get('productName')
            if query.get('status') == '已结束':
                # 如果状态为已结束，且今日有赎回交易，则为今日刚结束，需要计算盈亏，取赎回数据里的单位净值
                tradeData = tradeInfo.objects.filter(productName=productName, tradeType='赎回',
                                                     date=today).first()
                if tradeData is None:
                    continue
                netValue = tradeData.unitNet
            else:
                # 在投的产品直接取单位净值（最早更新的数据）
                netValue = fundNetValueInfo.objects.filter(productName=productName, date=project_date).order_by(
                    "lastUpdateDate").first()
                netValue = netValue.netValue
            # 获取数据库中原始数据
            df = fundpnl.dailyPnl(productName, project_date, today, netValue)
            pnlInx = fundPnlInfo.objects.order_by("-index").values()[0]
            index = pnlInx.get('index') + 1
            add_Amount = fundPnlInfo(index=index,
                                     date=datetime.strptime(str(project_date), '%Y-%m-%d'),
                                     productName=productName,

                                     acBuyAmount=df['acBuyAmount'].iloc[0],
                                     acSellAmount=df['acSellAmount'].iloc[0],
                                     buyCashAmount=df['buyCashAmount'].iloc[0],
                                     sellCashAmount=df['sellCashAmount'].iloc[0],
                                     sellCost=df['sellCost'].iloc[0],
                                     cashDiv=df['cashDiv'].iloc[0],

                                     todayNetValue=df['todayNetValue'].iloc[0],
                                     cumPnl=df['cumPnl'].iloc[0],
                                     todayPnl=df['todayPnl'].iloc[0],
                                     var=df['var'].iloc[0]
                                     )
            add_Amount.save()
    else:
        # 获取数据库中原始数据
        tradeData = tradeInfo.objects.filter(productName=productName, tradeType='赎回',
                                             confirmDate=project_date).first()
        if tradeData is None:
            netValue = fundNetValueInfo.objects.filter(productName=productName, date=project_date).order_by(
                "lastUpdateDate").first()
            netValue = netValue.netValue
        else:
            netValue = tradeData.unitNet

        df = fundpnl.dailyPnl(productName, project_date, today, netValue)
        pnlData = fundPnlInfo.objects.filter(productName=productName, date=project_date).first()
        if len(pnlData) == 0:
            pnlInx = fundPnlInfo.objects.order_by("-index").values()[0]
            index = pnlInx.get('index') + 1
            add_Pnl = fundPnlInfo(index=index,
                                  date=datetime.strptime(str(project_date), '%Y-%m-%d'),
                                  productName=productName,

                                  acBuyAmount=df['acBuyAmount'].iloc[0],
                                  acSellAmount=df['acSellAmount'].iloc[0],
                                  buyCashAmount=df['buyCashAmount'].iloc[0],
                                  sellCashAmount=df['sellCashAmount'].iloc[0],
                                  sellCost=df['sellCost'].iloc[0],
                                  cashDiv=df['cashDiv'].iloc[0],

                                  todayNetValue=df['todayNetValue'].iloc[0],
                                  cumPnl=df['cumPnl'].iloc[0],
                                  todayPnl=df['todayPnl'].iloc[0],
                                  var=df['var'].iloc[0]
                                  )
            add_Pnl.save()
        else:
            fundPnlInfo.objects.filter(productName=productName).filter(date=project_date).update(
                acBuyAmount=df['acBuyAmount'].iloc[0])
            fundPnlInfo.objects.filter(productName=productName).filter(date=project_date).update(
                acSellAmount=df['acSellAmount'].iloc[0])
            fundPnlInfo.objects.filter(productName=productName).filter(date=project_date).update(
                buyCashAmount=df['buyCashAmount'].iloc[0])
            fundPnlInfo.objects.filter(productName=productName).filter(date=project_date).update(
                sellCashAmount=df['sellCashAmount'].iloc[0])
            fundPnlInfo.objects.filter(productName=productName).filter(date=project_date).update(
                sellCost=df['sellCost'].iloc[0])
            fundPnlInfo.objects.filter(productName=productName).filter(date=project_date).update(
                cashDiv=df['cashDiv'].iloc[0])

            fundPnlInfo.objects.filter(productName=productName).filter(date=project_date).update(
                todayNetValue=df['todayNetValue'].iloc[0])
            fundPnlInfo.objects.filter(productName=productName).filter(date=project_date).update(
                cumPnl=df['cumPnl'].iloc[0])
            fundPnlInfo.objects.filter(productName=productName).filter(date=project_date).update(
                todayPnl=df['todayPnl'].iloc[0])
            fundPnlInfo.objects.filter(productName=productName).filter(date=project_date).update(
                var=df['var'].iloc[0])
    return redirect('add/calcpnlreport')


# 修改产品基础数据
def modifyBasicInfo(request):
    productName = request.GET.get('productName')
    basicInfo_modify = request.GET.get('basicInfo')
    confirmDate1_modify = basicInfo_modify[basicInfo_modify.find('投委会通过日期:') + 8:basicInfo_modify.find(';')]
    basicInfo_modify = basicInfo_modify[basicInfo_modify.find(';')+1:]
    confirmDate2_modify = basicInfo_modify[basicInfo_modify.find('总办会通过日期:') + 8:basicInfo_modify.find(';')]
    basicInfo_modify = basicInfo_modify[basicInfo_modify.find(';')+1:]
    confirmDate1_modify = datetime.strptime(confirmDate1_modify, "%Y-%m-%d")
    confirmDate2_modify = datetime.strptime(confirmDate2_modify, "%Y-%m-%d")
    fundBasicInfo.objects.filter(productName=productName).update(confirmDate1=confirmDate1_modify)
    fundBasicInfo.objects.filter(productName=productName).update(confirmDate2=confirmDate2_modify)
    status_modify = basicInfo_modify[basicInfo_modify.find('状态:') + 3:basicInfo_modify.find(';')]
    basicInfo_modify = basicInfo_modify[basicInfo_modify.find(';')+1:]
    fundBasicInfo.objects.filter(productName=productName).update(status=status_modify)
    investableAmount_modify = basicInfo_modify[basicInfo_modify.find('剩余可投资额度:') + 8:basicInfo_modify.find(';')]
    basicInfo_modify = basicInfo_modify[basicInfo_modify.find(';')+1:]
    totalAmount_modify = basicInfo_modify[basicInfo_modify.find('累计审批额度:') + 7:basicInfo_modify.find(';')]
    basicInfo_modify = basicInfo_modify[basicInfo_modify.find(';')+1:]
    redeemCost_modify = basicInfo_modify[basicInfo_modify.find('累计赎回成本:') + 7:basicInfo_modify.find(';')]
    basicInfo_modify = basicInfo_modify[basicInfo_modify.find(';')+1:]
    fundBasicInfo.objects.filter(productName=productName).update(investableAmount=investableAmount_modify)
    fundBasicInfo.objects.filter(productName=productName).update(totalAmount=totalAmount_modify)
    fundBasicInfo.objects.filter(productName=productName).update(redeemCost=redeemCost_modify)

    productFullName_modify = basicInfo_modify[basicInfo_modify.find('产品全名:') + 5:basicInfo_modify.find(';')]
    basicInfo_modify = basicInfo_modify[basicInfo_modify.find(';')+1:]
    fundBasicInfo.objects.filter(productName=productName).update(productFullName=productFullName_modify)
    productType1_modify = basicInfo_modify[basicInfo_modify.find('产品类型1:') + 6:basicInfo_modify.find(';')]
    basicInfo_modify = basicInfo_modify[basicInfo_modify.find(';')+1:]
    productType2_modify = basicInfo_modify[basicInfo_modify.find('产品类型2:') + 6:basicInfo_modify.find(';')]
    basicInfo_modify = basicInfo_modify[basicInfo_modify.find(';')+1:]
    productType3_modify = basicInfo_modify[basicInfo_modify.find('产品类型3:') + 6:basicInfo_modify.find(';')]
    basicInfo_modify = basicInfo_modify[basicInfo_modify.find(';')+1:]
    fundBasicInfo.objects.filter(productName=productName).update(productType1=productType1_modify)
    fundBasicInfo.objects.filter(productName=productName).update(productType2=productType2_modify)
    fundBasicInfo.objects.filter(productName=productName).update(productType3=productType3_modify)

    strategy_modify = basicInfo_modify[basicInfo_modify.find('产品策略:') + 5:basicInfo_modify.find(';')]
    basicInfo_modify = basicInfo_modify[basicInfo_modify.find(';')+1:]
    senior_modify = basicInfo_modify[basicInfo_modify.find('是否为次级:') + 6:basicInfo_modify.find(';')]
    basicInfo_modify = basicInfo_modify[basicInfo_modify.find(';') + 1:]
    redeemLimit_modify = basicInfo_modify[basicInfo_modify.find('赎回是否受限:') + 7:basicInfo_modify.find(';')]
    basicInfo_modify = basicInfo_modify[basicInfo_modify.find(';') + 1:]
    fundBasicInfo.objects.filter(productName=productName).update(strategy=strategy_modify)
    fundBasicInfo.objects.filter(productName=productName).update(senior=senior_modify)
    fundBasicInfo.objects.filter(productName=productName).update(redeemLimit=redeemLimit_modify)
    manager_modify = basicInfo_modify[basicInfo_modify.find('管理人:') + 4:basicInfo_modify.find(';')]
    basicInfo_modify = basicInfo_modify[basicInfo_modify.find(';') + 1:]
    sector_modify = basicInfo_modify[basicInfo_modify.find('项目负责部门及人员:') + 10:basicInfo_modify.find(';')]
    basicInfo_modify = basicInfo_modify[basicInfo_modify.find(';') + 1:]
    fundBasicInfo.objects.filter(productName=productName).update(manager=manager_modify)
    fundBasicInfo.objects.filter(productName=productName).update(sector=sector_modify)

    alertLimit_modify = basicInfo_modify[basicInfo_modify.find('预警线:') + 4:basicInfo_modify.find(';')]
    basicInfo_modify = basicInfo_modify[basicInfo_modify.find(';') + 1:]
    cleanLimit_modify = basicInfo_modify[basicInfo_modify.find('清盘线:') + 4:basicInfo_modify.find(';')]
    basicInfo_modify = basicInfo_modify[basicInfo_modify.find(';') + 1:]
    fundBasicInfo.objects.filter(productName=productName).update(alertLimit=alertLimit_modify)
    fundBasicInfo.objects.filter(productName=productName).update(cleanLimit=cleanLimit_modify)
    preProvideFundDate_modify = basicInfo_modify[basicInfo_modify.find('拟出资时间:') + 6:basicInfo_modify.find(';')]
    basicInfo_modify = basicInfo_modify[basicInfo_modify.find(';') + 1:]
    preInvestDuration_modify = basicInfo_modify[basicInfo_modify.find('拟投资期限:') + 6:basicInfo_modify.find(';')]
    basicInfo_modify = basicInfo_modify[basicInfo_modify.find(';') + 1:]
    fundBasicInfo.objects.filter(productName=productName).update(preProvideFundDate=preProvideFundDate_modify)
    fundBasicInfo.objects.filter(productName=productName).update(preInvestDuration=preInvestDuration_modify)
    openDay_modify = basicInfo_modify[basicInfo_modify.find('开放频率:') + 5:basicInfo_modify.find(';')]
    basicInfo_modify = basicInfo_modify[basicInfo_modify.find(';') + 1:]
    temporaryOpen_modify = basicInfo_modify[basicInfo_modify.find('是否有临开:') + 6:basicInfo_modify.find(';')]
    basicInfo_modify = basicInfo_modify[basicInfo_modify.find(';') + 1:]
    fundBasicInfo.objects.filter(productName=productName).update(openDay=openDay_modify)
    fundBasicInfo.objects.filter(productName=productName).update(temporaryOpen=temporaryOpen_modify)
    rmAlertLimit_modify = basicInfo_modify[basicInfo_modify.find('风控预警线:') + 6:basicInfo_modify.find(';')]
    basicInfo_modify = basicInfo_modify[basicInfo_modify.find(';') + 1:]
    rmCleanLimit_modify = basicInfo_modify[basicInfo_modify.find('风控止损线:') + 6:basicInfo_modify.find(';')]
    basicInfo_modify = basicInfo_modify[basicInfo_modify.find(';') + 1:]
    fundBasicInfo.objects.filter(productName=productName).update(rmAlertLimit=rmAlertLimit_modify)
    fundBasicInfo.objects.filter(productName=productName).update(rmCleanLimit=rmCleanLimit_modify)
    rmRules_modify = basicInfo_modify[basicInfo_modify.find('风控条款说明:') + 7:basicInfo_modify.find(';')]
    basicInfo_modify = basicInfo_modify[basicInfo_modify.find(';') + 1:]
    investPurpose_modify = basicInfo_modify[basicInfo_modify.find('投资目的:') + 5:basicInfo_modify.find(';')]
    basicInfo_modify = basicInfo_modify[basicInfo_modify.find(';') + 1:]
    selfManage_modify = basicInfo_modify[basicInfo_modify.find('是否为公司自主管理产品:') + 12:basicInfo_modify.find(';')]
    basicInfo_modify = basicInfo_modify[basicInfo_modify.find(';') + 1:]
    investAdvisor_modify = basicInfo_modify[basicInfo_modify.find('公司是否担任投顾:') + 9:basicInfo_modify.find(';')]
    basicInfo_modify = basicInfo_modify[basicInfo_modify.find(';') + 1:]
    synergy_modify = basicInfo_modify[basicInfo_modify.find('是否涉及与证券协同:') + 10:basicInfo_modify.find(';')]
    basicInfo_modify = basicInfo_modify[basicInfo_modify.find(';') + 1:]
    thirdParty_modify = basicInfo_modify[basicInfo_modify.find('第三方:') + 4:basicInfo_modify.find(';')]
    basicInfo_modify = basicInfo_modify[basicInfo_modify.find(';') + 1:]
    synergyAmount_modify = basicInfo_modify[basicInfo_modify.find('拟协同业务规模:') + 8:basicInfo_modify.find(';')]
    basicInfo_modify = basicInfo_modify[basicInfo_modify.find(';') + 1:]
    fundBasicInfo.objects.filter(productName=productName).update(rmRules=rmRules_modify)
    fundBasicInfo.objects.filter(productName=productName).update(investPurpose=investPurpose_modify)
    fundBasicInfo.objects.filter(productName=productName).update(selfManage=selfManage_modify)
    fundBasicInfo.objects.filter(productName=productName).update(investAdvisor=investAdvisor_modify)
    fundBasicInfo.objects.filter(productName=productName).update(synergy=synergy_modify)
    fundBasicInfo.objects.filter(productName=productName).update(thirdParty=thirdParty_modify)
    fundBasicInfo.objects.filter(productName=productName).update(synergyAmount=synergyAmount_modify)
    demo_modify = basicInfo_modify[basicInfo_modify.find('备注:') + 3:-1]
    fundBasicInfo.objects.filter(productName=productName).update(demo=demo_modify)
    return JsonResponse({
        "code": 0,
        "status": "success"
    })
