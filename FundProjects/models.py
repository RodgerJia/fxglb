# -*- coding: utf-8 -*-
from django.db import models

# 产品基础信息表（对应新审批产品界面：进行产品录入。每支产品对应一条数据）
class fundBasicInfo(models.Model):
    index = models.AutoField(primary_key=True)
    date = models.DateField(auto_now=True, verbose_name="数据日期")
    confirmDate1 = models.DateField(verbose_name="投委会通过日期")
    confirmDate2 = models.DateField(verbose_name="总办会通过日期")
    productName = models.CharField(max_length=255, verbose_name="产品名称")
    productFullName = models.CharField(max_length=255, verbose_name="产品全名")

    productType1 = models.CharField(max_length=255, verbose_name="产品类型1")
    productType2 = models.CharField(max_length=255, verbose_name="产品类型2")
    productType3 = models.CharField(max_length=255, verbose_name="产品类型3")
    strategy = models.CharField(max_length=255, verbose_name="产品策略")
    senior = models.CharField(max_length=255, verbose_name="是否为次级")
    redeemLimit = models.CharField(max_length=255, verbose_name="赎回是否受限")
    manager = models.CharField(max_length=255, verbose_name="管理人")
    status = models.CharField(max_length=255, verbose_name="状态")
    sector = models.CharField(max_length=255, verbose_name="项目负责部门及人员")
    alertLimit = models.FloatField(default=0, verbose_name="预警线")
    cleanLimit = models.FloatField(default=0, verbose_name="清盘线")

    investableAmount = models.FloatField(default=0, verbose_name="剩余可投资额度")
    totalAmount = models.FloatField(default=0, verbose_name="累计审批额度")
    redeemCost = models.FloatField(default=0, verbose_name="累计赎回成本")

    preProvideFundDate = models.CharField(max_length=255, verbose_name="拟出资时间")
    preInvestDuration = models.CharField(max_length=255, verbose_name="拟投资期限")
    openDay = models.CharField(max_length=255, verbose_name="开放频率")
    temporaryOpen = models.CharField(max_length=255, verbose_name="是否有临开")

    rmAlertLimit = models.FloatField(default=0, verbose_name="风控预警线")
    rmCleanLimit = models.FloatField(default=0, verbose_name="风控止损线")

    rmRules = models.CharField(max_length=255, verbose_name="风控条款说明")
    investPurpose = models.CharField(max_length=255, verbose_name="投资目的")
    selfManage = models.CharField(max_length=255, verbose_name="是否为公司自主管理产品")
    investAdvisor = models.CharField(max_length=255, verbose_name="公司是否担任投顾")
    synergy = models.CharField(max_length=255, verbose_name="是否涉及与证券协同")
    thirdParty = models.CharField(max_length=255, verbose_name="第三方")
    synergyAmount = models.FloatField(default=0, verbose_name="拟协同业务规模")

    demo = models.CharField(max_length=255, verbose_name="备注")

    class Meta:
        db_table = "fundBasicInfo"

# 产品盈亏表（对应计算日报盈亏数据界面：对齐数据计算盈亏入库）
class fundPnlInfo(models.Model):
    index = models.AutoField(primary_key=True)
    date = models.DateField(verbose_name="数据日期")
    productName = models.CharField(max_length=255, verbose_name="产品名称")
    lastUpdateDate = models.DateField(auto_now=True, verbose_name="最后更新日期")

    acBuyAmount = models.FloatField(default=0, verbose_name="累计申购额度")
    acSellAmount = models.FloatField(default=0, verbose_name="累计赎回额度")
    buyCashAmount = models.FloatField(default=0, verbose_name="申购款")
    sellCashAmount = models.FloatField(default=0, verbose_name="赎回款")
    sellCost = models.FloatField(default=0, verbose_name="赎回成本")
    cashDiv = models.FloatField(default=0, verbose_name="现金分红")

    todayNetValue = models.FloatField(default=0, verbose_name="今日净值")
    cumPnl = models.FloatField(default=0, verbose_name="累计总盈亏")
    todayPnl = models.FloatField(default=0, verbose_name="当日盈亏")
    var = models.FloatField(default=0, verbose_name="VaR")

    class Meta:
        db_table = "fundPnlInfo"

# 产品交易表（对应新增交易记录界面：包括申购、赎回、现金分红、分红再投）
class tradeInfo(models.Model):
    index = models.AutoField(primary_key=True)
    date = models.DateField(verbose_name="数据日期")
    productName = models.CharField(max_length=255, verbose_name="产品名称")
    applyDate = models.DateField(verbose_name="申请日期")
    confirmDate = models.DateField(verbose_name="确认日期")
    tradeType = models.CharField(max_length=255, verbose_name="交易类型")
    tradeShare = models.FloatField(default=0, verbose_name="交易份额")
    unitNet = models.FloatField(default=0, verbose_name="单位净值")
    fee = models.FloatField(default=0, verbose_name="手续费")
    tradeAmount = models.FloatField(default=0, verbose_name="交易款")
    cost = models.FloatField(default=0, verbose_name="赎回成本")

    class Meta:
        db_table = "tradeInfo"

# 总额度表（对应修改总办会额度界面，每审批新产品、赎回产品，更新一条数据）
class totalAmountInfo(models.Model):
    index = models.AutoField(primary_key=True)
    date = models.DateField(auto_now=True, verbose_name="数据日期")
    confirmDate = models.DateField(verbose_name="确认日期")

    totalAmount = models.FloatField(default=0, verbose_name="总额度")
    newUsed = models.FloatField(default=0, verbose_name="新增审批")
    usedAmount = models.FloatField(default=0, verbose_name="已审批额度")
    newBack = models.FloatField(default=0, verbose_name="已赎回额度")
    usableAmount = models.FloatField(default=0, verbose_name="剩余额度")

    demo = models.CharField(max_length=255, verbose_name="备注")

    class Meta:
        db_table = "totalAmount"

# 产品净值表（对应录入每日基金净值界面，对齐日期的净值数据。一支产品一个日期匹配一条净值数据）
class fundNetValueInfo(models.Model):
    index = models.AutoField(primary_key=True)
    date = models.DateField(verbose_name="数据日期")
    lastUpdateDate = models.DateField(auto_now=True, verbose_name="最后更新日期")

    productName = models.CharField(max_length=255, verbose_name="产品名称")
    netValue = models.FloatField(default=0, verbose_name="单位净值")
    acNetValue = models.FloatField(default=0, verbose_name="累计净值")

    demo = models.CharField(max_length=255, verbose_name="备注")

    class Meta:
        db_table = "fundNetValue"

# 真实产品净值表（对应录入每日基金净值界面，真实日期的净值数据。一支产品一个日期匹配一条净值数据）
class confirmNetValueInfo(models.Model):
    index = models.AutoField(primary_key=True)
    date = models.DateField(verbose_name="数据日期")
    lastUpdateDate = models.DateField(auto_now=True, verbose_name="最后更新日期")

    productName = models.CharField(max_length=255, verbose_name="产品名称")
    netValue = models.FloatField(default=0, verbose_name="单位净值")
    acNetValue = models.FloatField(default=0, verbose_name="累计净值")

    demo = models.CharField(max_length=255, verbose_name="备注")

    class Meta:
        db_table = "confirmNetValueInfo"

# 德睿限额数据表（对应日报界面中 上传德睿数据采集表。excel表入库，每天一条数据）
class deruiLimitData(models.Model):
    index = models.AutoField(primary_key=True)
    date = models.DateField(verbose_name="数据日期")
    l1_creditAmt_nonSecBank_usable = models.FloatField(default=0, verbose_name="融资授信资金规模（非券商银行类客户）（审批值）")
    l1_creditAmt_nonSecBank_used = models.FloatField(default=0, verbose_name="融资授信资金规模（非券商银行类客户）（占用值）")
    l1_creditAmt_secBank_usable = models.FloatField(default=0, verbose_name="融资授信资金规模（券商银行类客户）（审批数）")
    l1_creditAmt_secBank_used = models.FloatField(default=0, verbose_name="融资授信资金规模（券商银行类客户）（占用数）")
    l1_loss = models.FloatField(default=0, verbose_name="年内损失")
    l1_cashDelta = models.FloatField(default=0, verbose_name="敞口")
    l1_var = models.FloatField(default=0, verbose_name="VaR")
    l1_assetAmt = models.FloatField(default=0, verbose_name="一级流动性储备资产规模/自有资产总额")

    l2_otc_cashDelta = models.FloatField(default=0, verbose_name="场外业务敞口")
    l2_otc_singleCreditAmt_nonSecBank = models.FloatField(default=0, verbose_name="单一客户场外业务授信规模(除券商、银行）")
    l2_otc_singleCreditAmt_secBank = models.FloatField(default=0,verbose_name="单一客户场外业务授信规模（券商、银行）")
    l2_otc_singleNominal = models.FloatField(default=0, verbose_name="单一客户卖出（合同约定方向）场外业务有效名义本金规模")
    l2_otc_creditAmt_nonSecBank = models.FloatField(default=0,verbose_name="场外非券商、银行客户授信限额")
    l2_otc_creditAmt_secBank = models.FloatField(default=0, verbose_name="场外券商、银行客户授信限额")
    l2_otc_loss = models.FloatField(default=0, verbose_name="场外年内损失")
    l2_otc_var = models.FloatField(default=0, verbose_name="场外VaR")

    l2_omm_cashDelta = models.FloatField(default=0, verbose_name="做市业务敞口")
    l2_omm_loss = models.FloatField(default=0, verbose_name="做市年内损失")
    l2_omm_var = models.FloatField(default=0, verbose_name="做市VaR")

    l2_c_cashDelta = models.FloatField(default=0, verbose_name="期现业务敞口")
    l2_c_singleCreditAmt = models.FloatField(default=0, verbose_name="单一客户期现业务授信规模")
    l2_c_creditAmt_usable = models.FloatField(default=0, verbose_name="期现客户授信限额(审批值)")
    l2_c_creditAmt_used = models.FloatField(default=0, verbose_name="期现客户授信限额（占用值）")
    l2_c_loss = models.FloatField(default=0, verbose_name="期现年内损失")
    l2_c_var = models.FloatField(default=0, verbose_name="期现VaR")

    l2_sigma_productCashDelta= models.FloatField(default=0, verbose_name="金融产品投资业务敞口（不包含现金管理类）")
    l2_sigma_singleEquityAmt = models.FloatField(default=0, verbose_name="投资单一权益类产品规模")
    l2_sigma_singleFIAmt = models.FloatField(default=0, verbose_name="投资单一固定收益类产品规模")
    l2_sigma_singleMixAmt = models.FloatField(default=0, verbose_name="投资单一混合类产品投资规模")
    l2_sigma_productLoss = models.FloatField(default=0, verbose_name="金融产品投资年内损失（不包含现金管理类）")
    l2_sigma_productVaR = models.FloatField(default=0, verbose_name="金融产品投资VaR（不包含现金管理类）")

    l2_sigma_cashDelta = models.FloatField(default=0, verbose_name="自营业务（不含金融产品投资）敞口")
    l2_sigma_loss = models.FloatField(default=0, verbose_name="自营业务（不含金融产品投资）年内损失")
    l2_sigma_var = models.FloatField(default=0, verbose_name="自营业务（不含金融产品投资）VaR")

    other_repoAmt = models.FloatField(default=0, verbose_name="买断式仓单规模")
    other_repoAmtLoss = models.FloatField(default=0, verbose_name="买断式仓单回购减值")
    class Meta:
        db_table = "deruilimitdata"

# 德睿业务数据表（对应日报界面中 上传德睿指标报送表。excel表入库，每天一条数据）
class deruisectordata(models.Model):
    index = models.AutoField(primary_key=True)
    date = models.DateField(verbose_name="数据日期")
    equityCashDelta = models.FloatField(default=0, verbose_name="权益类（含其对应衍生品）敞口（Delta金额）")
    equityVar = models.FloatField(default=0, verbose_name="权益类（含其对应衍生品）VaR")
    equityPnl = models.FloatField(default=0, verbose_name="权益类（含其对应衍生品）当年盈亏")
    equityLoss = models.FloatField(default=0, verbose_name="权益类（含其对应衍生品）压力损失")
    nonEquityCashDelta = models.FloatField(default=0, verbose_name="非权益类（含其对应衍生品）敞口（Delta金额）")
    nonEquityVar = models.FloatField(default=0, verbose_name="非权益类（含其对应衍生品）VaR（1d，95%）")
    nonEquityPnl = models.FloatField(default=0, verbose_name="非权益类（含其对应衍生品）当年盈亏")
    nonEquityLoss = models.FloatField(default=0, verbose_name="非权益类（含其对应衍生品）压力损失")

    totalCashDelta = models.FloatField(default=0, verbose_name="公司整体敞口（Delta金额）")
    totalVar = models.FloatField(default=0, verbose_name="公司整体VaR")
    totalPnl = models.FloatField(default=0, verbose_name="公司整体当年盈亏（年度业务投资止损限额）")
    totalLoss = models.FloatField(default=0, verbose_name="公司整体压力损失")

    otcAmt_fin = models.FloatField(default=0, verbose_name="场外业务（金融）占用资金规模")
    otcAmt_fin_fund = models.FloatField(default=0, verbose_name="场外业务（金融）占用资金规模（含保证金）")
    otcCashDelta_fin = models.FloatField(default=0, verbose_name="场外业务（金融）敞口（Delta金额）")
    otcVar_fin = models.FloatField(default=0, verbose_name="场外期权（金融）VaR（1d，95%）")
    otcPnl_fin = models.FloatField(default=0, verbose_name="场外期权（金融）当年盈亏")

    otcAmt_comm = models.FloatField(default=0, verbose_name="场外业务（商品）占用资金规模")
    otcAmt_comm_fund = models.FloatField(default=0, verbose_name="场外业务（商品）占用资金规模（含保证金）")
    otcCashDelta_comm = models.FloatField(default=0, verbose_name="场外业务（商品）敞口（Delta金额）")
    otcVar_comm = models.FloatField(default=0, verbose_name="场外期权（商品）VaR（1d，95%）")
    otcPnl_comm = models.FloatField(default=0, verbose_name="场外期权（商品）当年盈亏")

    otcAmt_other = models.FloatField(default=0, verbose_name="场外业务（其他）占用资金规模")
    otcAmt_other_fund = models.FloatField(default=0, verbose_name="场外业务（其他）占用资金规模（含保证金）")
    otcCashDelta_other = models.FloatField(default=0, verbose_name="场外业务（其他）敞口（Delta金额）")
    otcVar_other = models.FloatField(default=0, verbose_name="场外期权（其他）VaR（1d，95%）")
    otcPnl_other = models.FloatField(default=0, verbose_name="场外期权（其他）当年盈亏")

    otcAmt = models.FloatField(default=0,verbose_name="场外业务占用资金规模")
    otcMargin = models.FloatField(default=0, verbose_name="场外业务保证金")
    otcCashDelta = models.FloatField(default=0, verbose_name="场外业务敞口（Delta金额）")
    otcVar = models.FloatField(default=0,verbose_name="场外业务VaR（1d，95%）")
    otcPnl = models.FloatField(default=0, verbose_name="场外业务当年盈亏")

    ommAmt_fut = models.FloatField(default=0, verbose_name="期货做市占用资金规模")
    ommCashDelta_fut = models.FloatField(default=0, verbose_name="期货做市业务敞口（Delta金额）")
    ommVar_fut = models.FloatField(default=0, verbose_name="期货做市业务VaR（1d，95%）")
    ommPnl_fut = models.FloatField(default=0, verbose_name="期货做市业务当年盈亏")

    ommAmt_opt = models.FloatField(default=0, verbose_name="期权做市占用资金规模")
    ommCashDelta_opt = models.FloatField(default=0, verbose_name="期权做市业务敞口（Delta金额）")
    ommVar_opt = models.FloatField(default=0, verbose_name="期权做市业务VaR（1d，95%）")
    ommPnl_opt = models.FloatField(default=0, verbose_name="期权做市业务当年盈亏")

    ommAmt = models.FloatField(default=0, verbose_name="做市业务占用资金规模")
    ommCashDelta = models.FloatField(default=0, verbose_name="做市业务敞口（Delta金额）")
    ommVar = models.FloatField(default=0, verbose_name="做市业务VaR（1d，95%）")
    ommPnl = models.FloatField(default=0, verbose_name="做市业务当年盈亏")

    sigmaAmt_pro = models.FloatField(default=0, verbose_name="自营业务（产品投资）占用资金规模")
    sigmaCashDelta_pro = models.FloatField(default=0, verbose_name="自营业务（产品投资）敞口（Delta金额）")
    sigmaVar_pro = models.FloatField(default=0, verbose_name="自营业务（产品投资）VaR（1d，95%）")
    sigmaPnl_pro = models.FloatField(default=0, verbose_name="自营业务（产品投资）当年盈亏")

    sigmaAmt_vol = models.FloatField(default=0, verbose_name="自营业务（波动率策略）占用资金规模")
    sigmaCashDelta_vol = models.FloatField(default=0, verbose_name="自营业务（波动率策略）敞口（Delta金额）")
    sigmaVar_vol = models.FloatField(default=0, verbose_name="自营业务（波动率策略）VaR（1d，95%）")
    sigmaPnl_vol = models.FloatField(default=0, verbose_name="自营业务（波动率策略）当年盈亏")

    sigmaAmt = models.FloatField(default=0, verbose_name="自营业务占用资金规模")
    sigmaCashDelta = models.FloatField(default=0, verbose_name="自营业务敞口（Delta金额）")
    sigmaVar = models.FloatField(default=0, verbose_name="自营业务VaR（1d，95%）")
    sigmaPnl = models.FloatField(default=0, verbose_name="自营业务当年盈亏")

    cAmt_fund = models.FloatField(default=0, verbose_name="期现融资类业务占用资金规模")
    cCashDelta_fund = models.FloatField(default=0, verbose_name="期现融资类业务敞口（Delta金额）")
    cVar_fund = models.FloatField(default=0, verbose_name="期现融资类业务VaR（1d，95%）")
    cPnl_fund = models.FloatField(default=0, verbose_name="期现融资类业务当年盈亏")

    cAmt_basic = models.FloatField(default=0, verbose_name="期现基差类业务占用资金规模")
    cCashDelta_basic = models.FloatField(default=0, verbose_name="期现基差类业务敞口（Delta金额）")
    cVar_basic = models.FloatField(default=0, verbose_name="期现基差类业务VaR（1d，95%）")
    cPnl_basic = models.FloatField(default=0, verbose_name="期现基差类业务当年盈亏")

    cAmt = models.FloatField(default=0, verbose_name="期现业务占用资金规模")
    cCashDelta = models.FloatField(default=0, verbose_name="期现业务敞口（Delta金额）")
    cVar = models.FloatField(default=0, verbose_name="期现业务VaR（1d，95%）")
    cPnl = models.FloatField(default=0, verbose_name="期现业务当年盈亏")

    cashAmt = models.FloatField(default=0, verbose_name="现金管理占用资金规模")
    creditAmt = models.FloatField(default=0, verbose_name="授信占用资金规模")

    stkAcctAmt = models.FloatField(default=0, verbose_name="证券当期账户余额")
    stkSTLoan = models.FloatField(default=0, verbose_name="证券临时拆借款")
    stkOthers = models.FloatField(default=0, verbose_name="证券其他")

    ommBack = models.FloatField(default=0, verbose_name="预估返还")
    actOmmBack = models.FloatField(default=0, verbose_name="期货实际返还")
    actOmmBackOpt = models.FloatField(default=0, verbose_name="期权实际返还")
    class Meta:
        db_table = "deruisectordata"

# 德睿特殊授信数据表（对应日报界面中 上传德睿指标报送表。excel表入库，每天N条数据，每日数据数量不确定）
class deruiCreditData(models.Model):
    index = models.AutoField(primary_key=True)
    date = models.DateField(auto_now=True, verbose_name="数据日期")

    sector = models.CharField(max_length=255, verbose_name="业务类型")
    name = models.CharField(max_length=255, verbose_name="客户名称")
    amt = models.FloatField(default=0, verbose_name="授信额度")

    deadline = models.DateField(verbose_name="数据日期")

    class Meta:
        db_table = "deruiCreditData"

# 公司财务数据表（对应日报界面中，公司监管指标，财务管理部报送表。excel表入库，每天一条数据）
class dailyFinanceData(models.Model):
    index = models.AutoField(primary_key=True)
    date = models.DateField(auto_now=True, verbose_name="数据日期")

    cashAmt = models.FloatField(default=0, verbose_name="现金管理在投产品规模")
    cashNum = models.FloatField(default=0, verbose_name="现金管理在投产品只数")
    cashQuartPnl = models.FloatField(default=0, verbose_name="现金管理当季盈亏")
    cashYearPnl = models.FloatField(default=0, verbose_name="现金管理当年盈亏")
    cashCumPnl = models.FloatField(default=0, verbose_name="现金管理累计盈亏")

    netEquity = models.FloatField(default=0, verbose_name="净资本")
    netAsset = models.FloatField(default=0, verbose_name="净资产")
    netEAratio = models.FloatField(default=0, verbose_name="净资本/净资产")
    riskCapital = models.FloatField(default=0, verbose_name="风险资本准备总额")
    coverRatio = models.FloatField(default=0, verbose_name="风险覆盖率")

    netECratio_sup = models.FloatField(default=0, verbose_name="净资本/风险准备金总额（月度监管）")
    netEAratio_sup = models.FloatField(default=0, verbose_name="净资本/净资产（月度监管）")
    liqALratio_sup = models.FloatField(default=0, verbose_name="流动资产/流动负债（月度监管）")
    netLAratio_sup = models.FloatField(default=0, verbose_name="负债/净资产（月度监管）")

    productAmt = models.FloatField(default=0, verbose_name="产品投资在投产品规模")
    productNum = models.FloatField(default=0, verbose_name="产品投资在投产品只数")
    productYearPnl = models.FloatField(default=0, verbose_name="产品投资当年盈亏")
    productCumPnl = models.FloatField(default=0, verbose_name="产品投资累计盈亏")
    class Meta:
        db_table = "dailyFinanceData"

# 公司资管情况 （对应日报界面中，上传公司风控表，excel表入库，每天一条）
class productDailyReport(models.Model):
    index = models.AutoField(primary_key=True)
    date = models.DateField(auto_now=True, verbose_name="数据日期")

    type = models.CharField(max_length=255, verbose_name="产品类型")
    totalEquity = models.FloatField(default=0, verbose_name="总资产权益")
    alertRisk = models.CharField(max_length=255, verbose_name="测试后预警风险")
    cleanRisk = models.CharField(max_length=255, verbose_name="清盘风险")

    class Meta:
        db_table = "productDailyReport"

# 日报补充数据（对应日报界面，每天一条）
class rmDailyReport(models.Model):
    index = models.AutoField(primary_key=True)
    date = models.DateField(verbose_name="数据日期")

    closePos = models.FloatField(default=0, verbose_name="当日强平")
    overLoss = models.FloatField(default=0, verbose_name="当日新增穿仓损失")
    yearOverLoss = models.FloatField(default=0, verbose_name="年度累计穿仓损失")
    overRisk = models.FloatField(default=0, verbose_name="风险度超100%客户数")

    importantText = models.CharField(max_length=255, verbose_name="重要事项")
    limitText = models.CharField(max_length=255, verbose_name="限额情况")
    totalNum = models.FloatField(default=0, verbose_name="总期数")
    yearNum = models.FloatField(default=0, verbose_name="当年期数")

    nonInvestAmount = models.FloatField(default=0, verbose_name="已审批未投资额度")
    class Meta:
        db_table = "rmDailyReport"

# 双周报补充数据（对应双周报界面，每天一条）
class rmDoubleWeeklyReport(models.Model):
    index = models.AutoField(primary_key=True)
    date = models.DateField(verbose_name="数据日期")

    closePos = models.FloatField(default=0, verbose_name="强平情况")
    marginCall = models.FloatField(default=0, verbose_name="追保情况")
    yearOverLoss = models.FloatField(default=0, verbose_name="当年新增穿仓损失")
    overLoss = models.FloatField(default=0, verbose_name="年度累计穿仓损失")

    riskSupText = models.CharField(max_length=255, verbose_name="风险监管指标")
    limitText = models.CharField(max_length=255, verbose_name="董事会风险授权")
    authText = models.CharField(max_length=255, verbose_name="风险限额指标")
    importantRiskText = models.CharField(max_length=255, verbose_name="重大风险事件")
    totalNum = models.FloatField(default=0, verbose_name="总期数")
    yearNum = models.FloatField(default=0, verbose_name="当年期数")

    class Meta:
        db_table = "rmDoubleWeeklyReport"

# 风险限额表(对应主页风险限额)
class riskLimitInfo(models.Model):
    index = models.AutoField(primary_key=True)
    date = models.DateField(verbose_name="数据日期")

    limitType = models.CharField(max_length=255, verbose_name="限额类别")
    businessType = models.CharField(max_length=255, verbose_name="业务类型")
    limitTargetName = models.CharField(max_length=255, verbose_name="限额指标名称")
    limitValue = models.FloatField(default=0, verbose_name="限额值")
    targetValueTag = models.CharField(max_length=255, verbose_name="指标值标签")
    targetTableName = models.CharField(max_length=255, verbose_name="指标标签所属表")
    riskLevel = models.CharField(max_length=255, verbose_name="风险等级")

    class Meta:
        db_table = "riskLimitInfo"

class risklimit_v(models.Model):
    index = models.AutoField(primary_key=True)
    date = models.DateField(verbose_name="数据日期")

    cashAmt = models.CharField(max_length=255, verbose_name="自有资金现金管理")
    netECratio_sup = models.CharField(max_length=255, verbose_name="净资本/风险准备金总额")
    netEAratio_sup = models.CharField(max_length=255, verbose_name="净资本/净资产")
    liqALratio_sup = models.CharField(max_length=255, verbose_name="流动资产/流动负债")
    netLAratio_sup = models.CharField(max_length=255, verbose_name="负债/净资产")
    managerAmt = models.CharField(max_length=255, verbose_name="自有资金投资单一管理人（不含现金管理）")
    productAmt = models.CharField(max_length=255, verbose_name="自有资金投资产品类资产规模")
    hedgeAmt = models.CharField(max_length=255, verbose_name="自有资金投资对冲套利类策略产品规模")
    fixedAmt = models.CharField(max_length=255, verbose_name="自有资金投资方向性策略产品规模-固定收益类及其他")
    equityAmt = models.CharField(max_length=255, verbose_name="自有资金投资方向性策略产品规模-权益类、混合类、商品及金融衍生品类")
    yearPnl = models.CharField(max_length=255, verbose_name="自有资金投资产品类资产亏损限额")
    yearPnlAlarm = models.CharField(max_length=255, verbose_name="自有资金投资产品类资产亏损预警值")

    class Meta:
        db_table = "risklimit_v"