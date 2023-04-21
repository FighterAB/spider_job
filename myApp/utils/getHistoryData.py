from .getPublicData import *
from myApp.models import History
from django.db.models import F
import json


def addHistory(userInfo, jobid):
    print(userInfo.id, jobid)
    hisData = History.objects.filter(user_id=userInfo.id, job_id=jobid)
    if len(hisData):
        hisData[0].count = F('count') + 1
        hisData[0].save()
    else:
        History.objects.create(user_id=userInfo.id, job_id=jobid, count=1)
    pass

def removeHistory(hisId):
    his  = History.objects.get(id=hisId)
    his.delete()


def getHistoryData(userInfo):
    data = list(History.objects.filter(user_id=userInfo.id).order_by('-count'))

    def map_fn(item):
        item.job.salary = json.loads(item.job.salary)
        item.job.companyPeople = json.loads(item.job.companyPeople)
        item.job.workTag = json.loads(item.job.workTag)
        if item.job.companyTags != '无':
            item.job.companyTags = json.loads(item.job.companyTags).split('，')
        if not item.job.pratice:
            item.job.salary = list(map(lambda x: str(int(x / 1000)), item.job.salary))
        else:
            item.job.salary = list(map(lambda x: str(x), item.job.salary))
        item.job.salary = '-'.join(item.job.salary)
        item.job.companyPeople = list(map(lambda x: str(x), item.job.companyPeople))
        item.job.companyPeople = '-'.join(item.job.companyPeople)
        return item

    data = list(map(map_fn, data))
    return data
