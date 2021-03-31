from django.forms.models import model_to_dict
from django.shortcuts import render, redirect
from FundProjects.models import  deruiLimitData,riskLimitInfo,risklimit_v
from datetime import datetime
import FundProjects.method.Utils as Utils


'''
查询主页风险限额
'''
def setRiskLimitInfo(date):
    if not date:
        date = Utils.prev_weekday(datetime.now().date())
    dlds = deruiLimitData.objects.filter(date=date)
    while not dlds:
        date = Utils.prev_weekday(date)
        dlds = deruiLimitData.objects.filter(date=date)
    dld = model_to_dict(dlds.first())
    rlv = model_to_dict(risklimit_v.objects.filter(date=date).first())
    # 公司限额
    rliDataSet = riskLimitInfo.objects.all()
    for rliData in rliDataSet:
        if rliData.targetTableName == 'risklimit_v' and rliData.targetValueTag != '-':
            rliData.targetValueTag = rlv.get(rliData.targetValueTag)
        elif rliData.targetTableName == 'deruiLimitData':
            rliData.targetValueTag = round(dld.get(rliData.targetValueTag),4)
        else:
            rliData.targetValueTag = '未开展'
    return rliDataSet, str(date)
