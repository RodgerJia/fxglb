from datetime import date, timedelta,datetime
from django.apps import apps


'''
获取前一个工作日
'''
def prev_weekday(dateParam):
    if type(dateParam).__name__ != 'date':
        dateParam = datetime.strptime(dateParam, '%Y-%m-%d').date()
    dateParam -= timedelta(days=1)
    while dateParam.weekday() > 4: # Mon-Fri are 0-4
        dateParam -= timedelta(days=1)
    return dateParam


'''
字符串转日期
'''
def parse_ymd(s) -> object:
    year_s, mon_s, day_s = str(s).split('-')
    return datetime(int(year_s), int(mon_s), int(day_s))



'''
获取models字段名称
'''

def getmodelfield(appname, modelname):
    modelobj = apps.get_model(appname, modelname)
    field_dic = {}
    for field in modelobj._meta.fields:
        field_dic[field.name] = field.verbose_name
        print('字段类型:', field)  # 返回的是‘charfield','textfield',等这些类型
    return field_dic
