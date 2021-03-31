"""FundProjects URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.urls import path
from FundProjects.views import *
import FundProjects.get.getFundData as getFundData
import FundProjects.add.addFundData as addFundData
import FundProjects.add.postDailyData as postDailyData
import FundProjects.get.getDailyData as getDailyData
import FundProjects.get.secReport as secReport
import FundProjects.brokeData.brokeData as brokeData
urlpatterns = [
    path('login', login),
    path('', index),
    #新界面添加url

    path('getData', getData),

    path('add/tradeinfo', tradeinfo),
    path('add/newproduct', newproduct),
    path('add/modifyamt', modifyamt),
    path('add/unitdata', unitdata),
    path('add/calcpnlreport', calcpnlreport),
    path('add/calctruepnl', calctruepnl),

    path('report/combinedStat', combinedStat),
    path('report/productReportSec', productReportSec),
    path('report/fundData', fundData),
    path('report/productReportBroke', productReportBroke),

    path('periodicReport/dailyReport', dailyReport),
    path('periodicReport/doubleWeeklyReport', doubleWeeklyReport),

    path('dataAnalysis/deruiSectorAnalysis', deruiSectorAnalysis),
    path('dataAnalysis/companyAnalysis', companyAnalysis),

    path('test/test1', test1),
    path('test/test2', test2),
    path('test/test3', test3),

    #查询数据添加url
    path('getTradeInfo', getFundData.getTradeInfo),
    path('getBasicInfo', getFundData.getBasicInfo),
    path('getTotalAmountInfo', getFundData.getTotalAmountInfo),
    path('getFundNetValueInfo', getFundData.getFundNetValueInfo),
    path('getConfirmNetValueInfo', getFundData.getConfirmNetValueInfo),
    path('getFundPnlReportData', getFundData.getFundPnlReportData),
    path('availableProductName', getFundData.availableProductName),

    # 提交、上传 产品相关数据
    path('addTradeInfo', addFundData.addTradeInfo),
    path('addProductInfo', addFundData.addProductInfo),
    path('postProduct', addFundData.postProduct),
    path('modifyAmtInfo', addFundData.modifyAmtInfo),
    path('calcPnlReport', addFundData.calcPnlReport),
    path('postPnl', addFundData.postPnl),
    path('postPnlHis', addFundData.postPnlHis),
    path('modifyBasicInfo', addFundData.modifyBasicInfo),

    # 日报数据
    path('postDeruiLimitData', postDailyData.postDeruiLimitData),
    path('postDeruiSectorData', postDailyData.postDeruiSectorData),
    path('postFinanceData', postDailyData.postFinanceData),
    path('postRiskDailyData', postDailyData.postRiskDailyData),
    path('addDailyData', postDailyData.addDailyData),
    path('getDailyData',getDailyData.getDailyData),
    path('productEchartsView', getDailyData.productEchartsView),
    path('getSpecialCreidtInfo', getDailyData.getSpecialCreidtInfo),

    # 双周报
    path('addDoubleWeeklyData', postDailyData.addDoubleWeeklyData),
    path('getDoubleWeeklyData', getDailyData.getDoubleWeeklyData),

    # 证券报表
    path('getCombinedStat', secReport.getCombinedStat),
    path('getProductReportSec', secReport.getProductReportSec),

    # 经纪业务
    path('postBrokerData', brokeData.postBrokerData),
    path('getBrokerData', brokeData.getBrokerData),
    path('getBrokerDataSeries', brokeData.getBrokerDataSeries),
    path('getInvestAmountData', brokeData.getInvestAmountData),

    # 主页风险检查
    path('checkRisk', checkRisk),
    path('updateRiskLimit', updateRiskLimit),
    path('checkProductSituation', checkProductSituation),

    # 德睿业务分析
    path('addOtcData', addOtcData),
    path('checkDeruiSector', checkDeruiSector),
    path('checkDeruiSectorEchartsView', checkDeruiSectorEchartsView),

    # 公司业务分析
    path('postSctorFundResult', postSctorFundResult),

    # 根据日报数据计算收益率
    path('getRet', getRet),

    # test
    path('productApi', productApi),
    path('addProduct', addProduct),


]
