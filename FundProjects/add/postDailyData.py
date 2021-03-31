# -*- coding: utf-8 -*-

"""
@author: zzj

@contact: QQ:10996784

@Created on: 2020/10/13 007 11:28
"""

from django.http import JsonResponse
from django.shortcuts import redirect

from FundProjects.models import rmDailyReport, rmDoubleWeeklyReport
from datetime import datetime
import pandas as pd

hisSpecialProductList = ['钢铁1号', '星光璀璨1号', '和誉3号', '银河期货大宗商品1号', '权银河旗舰3/4号', '银河人保安心盛世1号', '融宝16号', '华澳臻智稳健1期',
                         '权银河恒星1号']
nonInvestProductList = ['权银河旗舰3/4号', '银河人保安心盛世1号', '融宝16号', '华澳臻智稳健1期', '权银河恒星1号']
# 上传文件（净值数据）入库


from sqlalchemy import create_engine


def postDeruiLimitData(request):
    """批量导入数据"""
    # if request.method == "POST":
    fileName = request.FILES.get('file')
    data = pd.read_excel(fileName, None)
    date = fileName.name[9:17]

    if 'L1级风险限额监测表' in data.keys():
        df1 = data['L1级风险限额监测表']
        df1.columns = df1.iloc[1]
        l1_creditAmt_nonSecBank_usable = df1.loc[df1.限额指标名称 == '融资授信资金规模（非券商银行类客户）（审批值）'].指标值.values[0]
        l1_creditAmt_nonSecBank_used = df1.loc[df1.限额指标名称 == '融资授信资金规模（非券商银行类客户）（占用值）'].指标值.values[0]
        l1_creditAmt_secBank_usable = df1.loc[df1.限额指标名称 == '融资授信资金规模（券商银行类客户）（审批数）'].指标值.values[0]
        l1_creditAmt_secBank_used = df1.loc[df1.限额指标名称 == '融资授信资金规模（券商银行类客户）（占用数）'].指标值.values[0]
        l1_loss = df1.loc[df1.限额指标名称 == '年内损失'].指标值.values[0]
        l1_cashDelta = df1.loc[df1.限额指标名称 == '敞口（cash delta）'].指标值.values[0]
        l1_var = df1.loc[df1.限额指标名称 == 'VaR (1d, 95%)'].指标值.values[0]
        l1_assetAmt = df1.loc[df1.限额指标名称 == '一级流动性储备资产规模/自有资产总额'].指标值.values[0]
    if 'L2级风险限额监测表' in data.keys():
        df2 = data['L2级风险限额监测表']
        df2.columns = df2.iloc[1]
        l2_otc_cashDelta = df2.loc[df2.限额指标名称 == '业务敞口（cash delta）'].loc[df2.业务类型 == '场外业务'].指标值.values[0]
        l2_otc_singleCreditAmt_nonSecBank = \
            df2.loc[df2.限额指标名称 == '单一客户场外业务授信规模(除券商、银行）'].loc[df2.业务类型 == '场外业务'].指标值.values[0]
        l2_otc_singleCreditAmt_secBank = \
            df2.loc[df2.限额指标名称 == '单一客户场外业务授信规模（券商、银行）'].loc[df2.业务类型 == '场外业务'].指标值.values[0]
        l2_otc_singleNominal = 0.
        l2_otc_creditAmt_nonSecBank = df2.loc[df2.限额指标名称 == '场外非券商、银行客户授信限额'].loc[df2.业务类型 == '场外业务'].指标值.values[0]
        l2_otc_creditAmt_secBank = df2.loc[df2.限额指标名称 == '场外券商、银行客户授信限额'].loc[df2.业务类型 == '场外业务'].指标值.values[0]
        l2_otc_loss = df2.loc[df2.限额指标名称 == '年内损失'].loc[df2.业务类型 == '场外业务'].指标值.values[0]
        l2_otc_var = df2.loc[df2.限额指标名称 == 'VaR(1d, 95%)'].loc[df2.业务类型 == '场外业务'].指标值.values[0]

        l2_omm_cashDelta = df2.loc[df2.限额指标名称 == '业务敞口（cash delta）'].loc[df2.业务类型 == '做市业务'].指标值.values[0]
        l2_omm_loss = df2.loc[df2.限额指标名称 == '年内损失'].loc[df2.业务类型 == '做市业务'].指标值.values[0]
        l2_omm_var = df2.loc[df2.限额指标名称 == 'VaR(1d, 95%)'].loc[df2.业务类型 == '做市业务'].指标值.values[0]

        l2_c_cashDelta = df2.loc[df2.限额指标名称 == '业务敞口（cash delta）'].loc[df2.业务类型 == '期现业务'].指标值.values[0]
        l2_c_singleCreditAmt = df2.loc[df2.限额指标名称 == '单一客户期现业务授信规模'].loc[df2.业务类型 == '期现业务'].指标值.values[0]
        l2_c_creditAmt_usable = df2.loc[df2.限额指标名称 == '期现客户授信限额(审批值)'].loc[df2.业务类型 == '期现业务'].指标值.values[0]
        l2_c_creditAmt_used = df2.loc[df2.限额指标名称 == '期现客户授信限额（占用值）'].loc[df2.业务类型 == '期现业务'].指标值.values[0]
        l2_c_loss = df2.loc[df2.限额指标名称 == '年内损失'].loc[df2.业务类型 == '期现业务'].指标值.values[0]
        l2_c_var = df2.loc[df2.限额指标名称 == 'VaR(1d, 95%)'].loc[df2.业务类型 == '期现业务'].指标值.values[0]

        l2_sigma_productCashDelta = df2.loc[df2.限额指标名称 == '业务敞口（cash delta）'].loc[df2.业务类型 == '金融产品投资（不包含现金管理类）'].指标值.values[0]
        l2_sigma_singleEquityAmt = df2.loc[df2.限额指标名称 == '投资单一权益类产品规模'].loc[df2.业务类型 == '金融产品投资（不包含现金管理类）'].指标值.values[0]
        l2_sigma_singleFIAmt = df2.loc[df2.限额指标名称 == '投资单一固定收益类产品规模'].loc[df2.业务类型 == '金融产品投资（不包含现金管理类）'].指标值.values[0]
        l2_sigma_singleMixAmt = df2.loc[df2.限额指标名称 == '投资单一混合类产品投资规模'].loc[df2.业务类型 == '金融产品投资（不包含现金管理类）'].指标值.values[0]
        l2_sigma_productLoss = df2.loc[df2.限额指标名称 == '年内投资损失'].loc[df2.业务类型 == '金融产品投资（不包含现金管理类）'].指标值.values[0]
        l2_sigma_productVaR = df2.loc[df2.限额指标名称 == 'VaR(1d, 95%)'].loc[df2.业务类型 == '金融产品投资（不包含现金管理类）'].指标值.values[0]

        #2021.1.13: 新增l2_sigma_productCashDelta、l2_sigma_productVaR
        l2_sigma_cashDelta = df2.loc[df2.限额指标名称 == '业务敞口（cash delta）'].loc[df2.业务类型 == '自营业务（不含金融产品投资）'].指标值.values[0]
        l2_sigma_loss = df2.loc[df2.限额指标名称 == '年内投资损失'].loc[df2.业务类型 == '自营业务（不含金融产品投资）'].指标值.values[0]
        l2_sigma_var = df2.loc[df2.限额指标名称 == 'VaR(1d, 95%)'].loc[df2.业务类型 == '自营业务（不含金融产品投资）'].指标值.values[0]



    if '买断回购限额及减值' in data.keys():
        df3 = data['买断回购限额及减值']
        other_repoAmt = df3.loc[df3.指标名称 == '买断式仓单规模']['值（单位元）'].values[0]
        other_repoAmtLoss = df3.loc[df3.指标名称 == '买断式仓单回购减值']['值（单位元）'].values[0]


    dic = {'date': datetime.strptime(str(date), "%Y%m%d"),
           'l1_creditAmt_nonSecBank_usable': l1_creditAmt_nonSecBank_usable,
           'l1_creditAmt_nonSecBank_used': l1_creditAmt_nonSecBank_used,
           'l1_creditAmt_secBank_usable': l1_creditAmt_secBank_usable,
           'l1_creditAmt_secBank_used': l1_creditAmt_secBank_used,
           'l1_loss': l1_loss,
           'l1_cashDelta': l1_cashDelta,
           'l1_var': l1_var,
           'l1_assetAmt': l1_assetAmt,

           'l2_otc_cashDelta': l2_otc_cashDelta,
           'l2_otc_singleCreditAmt_nonSecBank': l2_otc_singleCreditAmt_nonSecBank,
           'l2_otc_singleCreditAmt_secBank': l2_otc_singleCreditAmt_secBank,
           'l2_otc_singleNominal': l2_otc_singleNominal,
           'l2_otc_creditAmt_nonSecBank': l2_otc_creditAmt_nonSecBank,
           'l2_otc_creditAmt_secBank': l2_otc_creditAmt_secBank,
           'l2_otc_loss': l2_otc_loss,
           'l2_otc_var': l2_otc_var,

           'l2_omm_cashDelta': l2_omm_cashDelta,
           'l2_omm_loss': l2_omm_loss,
           'l2_omm_var': l2_omm_var,

           'l2_c_cashDelta': l2_c_cashDelta,
           'l2_c_singleCreditAmt': l2_c_singleCreditAmt,
           'l2_c_creditAmt_usable': l2_c_creditAmt_usable,
           'l2_c_creditAmt_used': l2_c_creditAmt_used,
           'l2_c_loss': l2_c_loss,
           'l2_c_var': l2_c_var,

           'l2_sigma_cashDelta': l2_sigma_cashDelta,
           'l2_sigma_singleEquityAmt': l2_sigma_singleEquityAmt,
           'l2_sigma_singleFIAmt': l2_sigma_singleFIAmt,
           'l2_sigma_singleMixAmt': l2_sigma_singleMixAmt,
           'l2_sigma_loss': l2_sigma_loss,
           'l2_sigma_var': l2_sigma_var,

           'l2_sigma_productCashDelta': l2_sigma_productCashDelta,
           'l2_sigma_productLoss': l2_sigma_productLoss,
           'l2_sigma_productVaR': l2_sigma_productVaR,

           'other_repoAmt': other_repoAmt,
           'other_repoAmtLoss': other_repoAmtLoss
           }

    dfLimit = pd.DataFrame(dic, index=[0])
    engine = create_engine("mysql+pymysql://root:123456@localhost/djangotest", encoding="utf8")
    pd.io.sql.to_sql(dfLimit.reset_index(drop=True), 'deruilimitdata', engine, schema='djangotest', if_exists='append')

    return JsonResponse({
        "code": 0,
        "msg": "成功",
        "data": {}
    })


def postDeruiSectorData(request):
    """批量导入数据"""
    # if request.method == "POST":
    fileName = request.FILES.get('file')
    data = pd.read_excel(fileName, None)

    date = fileName.name[14:22]
    dic = {}
    dic['date'] = datetime.strptime(str(date), "%Y%m%d")
    if '德睿风险指标报送模板' in data.keys():
        df1 = data['德睿风险指标报送模板']
        df1.columns = df1.iloc[2]
        dic['equityCashDelta'] = df1.loc[df1.指标名称 == '权益类（含其对应衍生品）敞口（Delta金额）'].执行值.values[0]
        dic['equityVar'] = df1.loc[df1.指标名称 == '权益类（含其对应衍生品）VaR（1d，95%）'].执行值.values[0]
        dic['equityPnl'] = df1.loc[df1.指标名称 == '权益类（含其对应衍生品）当年盈亏'].执行值.values[0]

        dic['equityLoss'] = df1.loc[df1.指标名称 == '权益类（含其对应衍生品）压力损失'].执行值.values[0]
        dic['nonEquityCashDelta'] = df1.loc[df1.指标名称 == '非权益类（含其对应衍生品）敞口（Delta金额）'].执行值.values[0]
        dic['nonEquityVar'] = df1.loc[df1.指标名称 == '非权益类（含其对应衍生品）VaR（1d，95%）'].执行值.values[0]
        dic['nonEquityPnl'] = df1.loc[df1.指标名称 == '非权益类（含其对应衍生品）当年盈亏'].执行值.values[0]
        dic['nonEquityLoss'] = df1.loc[df1.指标名称 == '非权益类（含其对应衍生品）压力损失'].执行值.values[0]

        dic['totalCashDelta'] = df1.loc[df1.指标名称 == '公司整体敞口（Delta金额）'].执行值.values[0]
        dic['totalVar'] = df1.loc[df1.指标名称 == '公司整体VaR（1d，95%）'].执行值.values[0]
        dic['totalPnl'] = df1.loc[df1.指标名称 == '公司整体当年盈亏（年度业务投资止损限额）'].执行值.values[0]
        dic['totalLoss'] = df1.loc[df1.指标名称 == '公司整体压力损失'].执行值.values[0]

        dic['otcAmt_fin'] = df1.loc[df1.指标名称 == '场外业务（金融）占用资金规模'].执行值.values[0]
        dic['otcCashDelta_fin'] = df1.loc[df1.指标名称 == '场外业务（金融）敞口（Delta金额）'].执行值.values[0]
        dic['otcVar_fin'] = df1.loc[df1.指标名称 == '场外期权（金融）VaR（1d，95%）'].执行值.values[0]
        dic['otcPnl_fin'] = df1.loc[df1.指标名称 == '场外期权（金融）当年盈亏'].执行值.values[0]

        dic['otcAmt_comm'] = df1.loc[df1.指标名称 == '场外业务（商品）占用资金规模'].执行值.values[0]
        dic['otcCashDelta_comm'] = df1.loc[df1.指标名称 == '场外业务（商品）敞口（Delta金额）'].执行值.values[0]
        dic['otcVar_comm'] = df1.loc[df1.指标名称 == '场外期权（商品）VaR（1d，95%）'].执行值.values[0]
        dic['otcPnl_comm'] = df1.loc[df1.指标名称 == '场外期权（商品）当年盈亏'].执行值.values[0]

        dic['otcAmt_other'] = df1.loc[df1.指标名称 == '场外业务（其他）占用资金规模'].执行值.values[0]
        dic['otcCashDelta_other'] = df1.loc[df1.指标名称 == '场外业务（其他）敞口（Delta金额）'].执行值.values[0]
        dic['otcVar_other'] = df1.loc[df1.指标名称 == '场外期权（其他）VaR（1d，95%）'].执行值.values[0]
        dic['otcPnl_other'] = df1.loc[df1.指标名称 == '场外期权（其他）当年盈亏'].执行值.values[0]

        dic['otcAmt'] = df1.loc[df1.指标名称 == '场外业务占用资金规模'].执行值.values[0]
        dic['otcCashDelta'] = df1.loc[df1.指标名称 == '场外业务敞口（Delta金额）'].执行值.values[0]
        dic['otcVar'] = df1.loc[df1.指标名称 == '场外业务VaR（1d，95%）'].执行值.values[0]
        dic['otcPnl'] = df1.loc[df1.指标名称 == '场外业务当年盈亏'].执行值.values[0]

        dic['ommAmt_fut'] = df1.loc[df1.指标名称 == '期货做市占用资金规模'].执行值.values[0]
        dic['ommCashDelta_fut'] = df1.loc[df1.指标名称 == '期货做市业务敞口（Delta金额）'].执行值.values[0]
        dic['ommVar_fut'] = df1.loc[df1.指标名称 == '期货做市业务VaR（1d，95%）'].执行值.values[0]
        dic['ommPnl_fut'] = df1.loc[df1.指标名称 == '期货做市业务当年盈亏'].执行值.values[0]

        dic['ommAmt_opt'] = df1.loc[df1.指标名称 == '期权做市占用资金规模'].执行值.values[0]
        dic['ommCashDelta_opt'] = df1.loc[df1.指标名称 == '期权做市业务敞口（Delta金额）'].执行值.values[0]
        dic['ommVar_opt'] = df1.loc[df1.指标名称 == '期权做市业务VaR（1d，95%）'].执行值.values[0]
        dic['ommPnl_opt'] = df1.loc[df1.指标名称 == '期权做市业务当年盈亏'].执行值.values[0]

        dic['ommAmt'] = df1.loc[df1.指标名称 == '做市业务占用资金规模'].执行值.values[0]
        dic['ommCashDelta'] = df1.loc[df1.指标名称 == '做市业务敞口（Delta金额）'].执行值.values[0]
        dic['ommVar'] = df1.loc[df1.指标名称 == '做市业务VaR（1d，95%）'].执行值.values[0]
        dic['ommPnl'] = df1.loc[df1.指标名称 == '做市业务当年盈亏'].执行值.values[0]

        dic['sigmaAmt_pro'] = df1.loc[df1.指标名称 == '自营业务（产品投资）占用资金规模'].执行值.values[0]
        dic['sigmaCashDelta_pro'] = df1.loc[df1.指标名称 == '自营业务（产品投资）敞口（Delta金额）'].执行值.values[0]
        dic['sigmaVar_pro'] = df1.loc[df1.指标名称 == '自营业务（产品投资）VaR（1d，95%）'].执行值.values[0]
        dic['sigmaPnl_pro'] = df1.loc[df1.指标名称 == '自营业务（产品投资）当年盈亏'].执行值.values[0]

        dic['sigmaAmt_vol'] = df1.loc[df1.指标名称 == '自营业务（波动率策略）占用资金规模'].执行值.values[0]
        dic['sigmaCashDelta_vol'] = df1.loc[df1.指标名称 == '自营业务（波动率策略）敞口（Delta金额）'].执行值.values[0]
        dic['sigmaVar_vol'] = df1.loc[df1.指标名称 == '自营业务（波动率策略）VaR（1d，95%）'].执行值.values[0]
        dic['sigmaPnl_vol'] = df1.loc[df1.指标名称 == '自营业务（波动率策略）当年盈亏'].执行值.values[0]

        dic['sigmaAmt'] = df1.loc[df1.指标名称 == '自营业务占用资金规模'].执行值.values[0]
        dic['sigmaCashDelta'] = df1.loc[df1.指标名称 == '自营业务敞口（Delta金额）'].执行值.values[0]
        dic['sigmaVar'] = df1.loc[df1.指标名称 == '自营业务VaR（1d，95%）'].执行值.values[0]
        dic['sigmaPnl'] = df1.loc[df1.指标名称 == '自营业务当年盈亏'].执行值.values[0]

        dic['cAmt_fund'] = df1.loc[df1.指标名称 == '期现融资类业务占用资金规模'].执行值.values[0]
        dic['cCashDelta_fund'] = df1.loc[df1.指标名称 == '期现融资类业务敞口（Delta金额）'].执行值.values[0]
        dic['cVar_fund'] = df1.loc[df1.指标名称 == '期现融资类业务VaR（1d，95%）'].执行值.values[0]
        dic['cPnl_fund'] = df1.loc[df1.指标名称 == '期现融资类业务当年盈亏'].执行值.values[0]

        dic['cAmt_basic'] = df1.loc[df1.指标名称 == '期现基差类业务占用资金规模'].执行值.values[0]
        dic['cCashDelta_basic'] = df1.loc[df1.指标名称 == '期现基差类业务敞口（Delta金额）'].执行值.values[0]
        dic['cVar_basic'] = df1.loc[df1.指标名称 == '期现基差类业务VaR（1d，95%）'].执行值.values[0]
        dic['cPnl_basic'] = df1.loc[df1.指标名称 == '期现基差类业务当年盈亏'].执行值.values[0]

        dic['cAmt'] = df1.loc[df1.指标名称 == '期现业务占用资金规模'].执行值.values[0]
        dic['cCashDelta'] = df1.loc[df1.指标名称 == '期现业务敞口（Delta金额）'].执行值.values[0]
        dic['cVar'] = df1.loc[df1.指标名称 == '期现业务VaR（1d，95%）'].执行值.values[0]
        dic['cPnl'] = df1.loc[df1.指标名称 == '期现业务当年盈亏'].执行值.values[0]

        dic['cashAmt'] = df1.loc[df1.指标名称 == '现金管理占用资金规模'].执行值.values[0]
        dic['creditAmt'] = df1.loc[df1.指标名称 == '授信占用资金规模'].执行值.values[0]

        dic['otcAmt_fin_fund'] = '/'
        dic['otcAmt_comm_fund'] = '/'
        dic['otcAmt_other_fund'] = '/'
        dic['otcMargin'] = '/'
    dfData = pd.DataFrame(dic, index=[0])
    dfData = dfData.replace('/', float('nan'))

    dfCredit = pd.DataFrame()

    if '特殊授信汇总' in data.keys():
        df2 = data['特殊授信汇总']
        df2.columns = df2.iloc[0]
        df2 = df2.drop(0, axis=0)
        dfCredit['sector'] = df2.业务
        dfCredit['name'] = df2.客户名称
        dfCredit['amt'] = df2.授信额度
        dfCredit['deadline'] = df2.授信有效期
    dfCredit['date'] = datetime.strptime(str(date), "%Y%m%d")

    if '证券' in data.keys():
        df3 = data['证券']
        dfData['stkAcctAmt'] = df3.当期账户余额.iloc[0]
        dfData['stkSTLoan'] = df3.临时拆借款.iloc[0]
        dfData['stkOthers'] = df3.其他.iloc[0]
    if '做市返还' in data.keys():
        df4 = data['做市返还']
        dfData['ommBack'] = df4['预估返还（本年累计）'].iloc[0]
        dfData['actOmmBack'] = df4['期货实际返还（本年累计）'].iloc[0]
        dfData['actOmmBackOpt'] = df4['期权实际返还（本年累计）'].iloc[0]
    engine = create_engine("mysql+pymysql://root:123456@localhost/djangotest", encoding="utf8")
    pd.io.sql.to_sql(dfData.reset_index(drop=True), 'deruisectordata', engine, schema='djangotest', if_exists='append')
    pd.io.sql.to_sql(dfCredit.reset_index(drop=True), 'deruicreditdata', engine, schema='djangotest',
                     if_exists='append')

    return JsonResponse({
        "code": 0,
        "msg": "成功",
        "data": {}
    })


def postFinanceData(request):
    """批量导入数据"""
    # if request.method == "POST":
    fileName = request.FILES.get('file')
    data = pd.read_excel(fileName, None)
    date = fileName.name[-13:-5]
    dic = {}
    dic['date'] = datetime.strptime(str(date), "%Y%m%d")
    if '产品投资明细' in data.keys():
        df1 = data['产品投资明细']
        df1.columns = df1.iloc[2]
        if '自有资金现金管理' in df1.iloc[4].values:
            dic['cashAmt'] = df1.iloc[4].在投产品规模
            dic['cashNum'] = df1.iloc[4].在投产品只数
            dic['cashQuartPnl'] = df1.iloc[4].当季盈亏
            dic['cashYearPnl'] = df1.iloc[4].当年盈亏
            dic['cashCumPnl'] = df1.iloc[4].累计盈亏
        if '自有资金投资产品' in df1.iloc[3].values:
            dic['productAmt'] = df1.iloc[3].在投产品规模
            dic['productNum'] = df1.iloc[3].在投产品只数
            dic['productYearPnl'] = df1.iloc[3].当年盈亏
            dic['productCumPnl'] = df1.iloc[3].累计盈亏
    if '风险监管指标填报' in data.keys():
        df2 = data['风险监管指标填报']
        df2.columns = df2.iloc[0]
        dic['netEquity'] = df2.loc[df2.指标名称 == '净资本'].指标执行值.values[0]
        dic['netAsset'] = df2.loc[df2.指标名称 == '净资产'].指标执行值.values[0]
        dic['netEAratio'] = df2.loc[df2.指标名称 == '净资本/净资产'].指标执行值.values[0]
        dic['riskCapital'] = df2.loc[df2.指标名称 == '风险资本准备总额'].指标执行值.values[0]
        dic['coverRatio'] = df2.loc[df2.指标名称 == '风险覆盖率'].指标执行值.values[0]

        dic['netECratio_sup'] = df2.loc[df2.指标名称 == '净资本/风险准备金总额'].指标执行值.values[0]
        dic['netEAratio_sup'] = df2.loc[df2.指标名称 == '净资本/净资产'].指标执行值.values[0]
        dic['liqALratio_sup'] = df2.loc[df2.指标名称 == '流动资产/流动负债'].指标执行值.values[0]
        dic['netLAratio_sup'] = df2.loc[df2.指标名称 == '负债/净资产'].指标执行值.values[0]

    dfData = pd.DataFrame(dic, index=[0])
    dfData = dfData.replace('', float('nan'))

    engine = create_engine("mysql+pymysql://root:123456@localhost/djangotest", encoding="utf8")
    pd.io.sql.to_sql(dfData.reset_index(drop=True), 'dailyfinancedata', engine, schema='djangotest', if_exists='append')

    return JsonResponse({
        "code": 0,
        "msg": "成功",
        "data": {}
    })


def postRiskDailyData(request):
    """批量导入数据"""
    # if request.method == "POST":
    fileName = request.FILES.get('file')
    data = pd.read_excel(fileName, None)

    date = fileName.name[-15:-5]
    dfData = pd.DataFrame()

    if '净值日报' in data.keys():
        df1 = data['净值日报']
        dfData['futAcct'] = df1.期货账号.tolist()
        dfData['stkAcct'] = df1.股票账户.tolist()
        dfData['productId'] = df1.产品编码.tolist()
        dfData['productName'] = df1.产品名称.tolist()
        dfData['type'] = df1.产品性质.tolist()

        dfData['totalEquity'] = df1.总资产权益.tolist()
        dfData['futEquity'] = df1.期货账户权益.tolist()
        dfData['lastOtherEquity'] = df1.前日其它资产权益.tolist()
        dfData['otherEquity'] = df1.其它资产权益.tolist()
        dfData['otherChange'] = df1.其他资产变化.tolist()
        dfData['futPosPnl'] = df1.期货持仓盈亏.tolist()
        dfData['futMtmPnl'] = df1.期货盯市盈亏.tolist()
        dfData['lastFutEquity'] = df1.前日期货账户权益.tolist()
        dfData['futEquityChange'] = df1.期货账户权益变化.tolist()
        dfData['futOptMargin'] = df1['期货期权占用保证金（公司标准）'].tolist()
        dfData['availFund'] = df1.可用资金.tolist()
        dfData['futNetValue'] = df1.期货净合约价值.tolist()
        dfData['futValue'] = df1.期货总合约价值.tolist()
        dfData['stockValue'] = df1.股票合约价值.tolist()
        dfData['bondValue'] = df1.债券价值.tolist()
        dfData['fundAmount'] = df1.基金份额.tolist()

        dfData['netValue'] = df1.账面净值.tolist()
        dfData['lastNetValue'] = df1.前日估值.tolist()
        dfData['todayNetValueChange'] = df1.今日净值变化.tolist()
        dfData['evalNetValue'] = df1.估值净值.tolist()
        dfData['leverage'] = df1.杠杆度.tolist()
        dfData['riskRatio'] = df1['风险比例(%)'].tolist()
        dfData['futMarginDiff'] = df1.期货多头与空头占用保证金差值.tolist()
        dfData['netPos'] = df1.净敞口市值.tolist()

        dfData['alertNetValue'] = df1.预警净值.tolist()
        dfData['alertDiff'] = df1.预警值差额.tolist()
        dfData['onAlertRisk'] = df1.隔夜预警风险.tolist()
        dfData['stressTest'] = df1['压力测试（-5%）净值'].tolist()
        dfData['alertRisk'] = df1.测试后预警风险.tolist()
        dfData['clean'] = df1.清盘线.tolist()
        dfData['cleanRisk'] = df1.清盘风险.tolist()
        dfData['pbSystem'] = df1.PB系统.tolist()

    dfData['date'] = datetime.strptime(str(date), "%Y-%m-%d")

    engine = create_engine("mysql+pymysql://root:123456@localhost/djangotest", encoding="utf8")
    pd.io.sql.to_sql(dfData.reset_index(drop=True), 'productdailyreport', engine, schema='djangotest',
                     if_exists='append')

    return JsonResponse({
        "code": 0,
        "msg": "成功",
        "data": {}
    })


def addDailyData(request):
    dataDate = request.POST.get('dataDate', "")

    closePos = float(request.POST.get('closePos', 0))
    overLoss = float(request.POST.get('overLoss', 0))
    yearOverLoss = float(request.POST.get('yearOverLoss', 0))
    overRisk = float(request.POST.get('overRisk', 0))
    nonInvestAmount = float(request.POST.get('nonInvestAmount', 0))

    importantText = request.POST.get('importantText', "")
    limitText = request.POST.get('limitText', "当日无超董事会授权及L1\L2限额情况")
    if limitText == '':
        limitText = '当日无超董事会授权及L1\L2限额情况'

    index = rmDailyReport.objects.order_by("-index").values()[0].get('index') + 1
    totalNum = rmDailyReport.objects.order_by("-totalNum").values()[0].get('totalNum') + 1
    yearNum = rmDailyReport.objects.order_by("-totalNum").values()[0].get('yearNum') + 1
    lastDate = rmDailyReport.objects.order_by("-totalNum").values()[0].get('date')
    if str(lastDate.year) != dataDate[:4]:
        yearNum = 1

    add_report = rmDailyReport(index=index,
                               date=dataDate,
                               closePos=closePos,
                               overLoss=overLoss,
                               yearOverLoss=yearOverLoss,
                               overRisk=overRisk,
                               nonInvestAmount=nonInvestAmount,

                               importantText=importantText,
                               limitText=limitText,
                               totalNum=totalNum,
                               yearNum=yearNum,
                               )
    add_report.save()

    return redirect('periodicReport/dailyReport')


def addDoubleWeeklyData(request):
    dataDate = request.POST.get('dataDate', "")

    closePos = float(request.POST.get('closePos', ""))
    marginCall = float(request.POST.get('marginCall', ""))
    yearOverLoss = float(request.POST.get('yearOverLoss', ""))
    overLoss = float(request.POST.get('overLoss', ""))

    riskSupText = request.POST.get('riskSupText', "公司各项风险监管指标均运行平稳，优于监管标准")
    authText = request.POST.get('authText', "公司及子公司各项业务均在董事会授权范围内有序开展")
    limitText = request.POST.get('limitText', "公司L1\L2限额执行良好，未发生超限事项")
    importantRiskText = request.POST.get('importantRiskText', "公司及子公司当期未发生重大风险事件")
    if riskSupText == '':
        riskSupText = '公司各项风险监管指标均运行平稳，优于监管标准'
    if authText == '':
        authText = '公司及子公司各项业务均在董事会授权范围内有序开展'
    if limitText == '':
        limitText = '公司L1\L2限额执行良好，未发生超限事项'
    if importantRiskText == '':
        importantRiskText = '公司及子公司当期未发生重大风险事件'

    index = rmDoubleWeeklyReport.objects.order_by("-index").values()[0].get('index') + 1
    totalNum = rmDoubleWeeklyReport.objects.order_by("-totalNum").values()[0].get('totalNum') + 1
    yearNum = rmDoubleWeeklyReport.objects.order_by("-totalNum").values()[0].get('yearNum') + 1
    lastDate = rmDoubleWeeklyReport.objects.order_by("-totalNum").values()[0].get('date')
    if str(lastDate.year) != dataDate[:4]:
        yearNum = 1

    add_report = rmDoubleWeeklyReport(index=index,
                                      date=dataDate,
                                      closePos=closePos,
                                      marginCall=marginCall,
                                      yearOverLoss=yearOverLoss,
                                      overLoss=overLoss,

                                      riskSupText=riskSupText,
                                      limitText=limitText,
                                      authText=authText,
                                      importantRiskText=importantRiskText,
                                      totalNum=totalNum,
                                      yearNum=yearNum,
                                      )
    add_report.save()

    return redirect('periodicReport/doubleWeeklyReport')