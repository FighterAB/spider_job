from .getPublicData import *
from myApp.models import JobInfo
import json


def getPageData():
    job = []
    jobs = getAllJobs()
    for i in jobs: job.append(i.type)
    return list(set(job))


def getTechnologyData(type):
    if type == '不限':
        jobs = getAllJobs()
    else:
        jobs = JobInfo.objects.filter(type=type)
    workTagData = {}
    for job in jobs:
        workTag = json.loads(job.workTag)
        for w in workTag:
            # 便签为空则跳过
            if not w: break
            if workTagData.get(w, -1) == -1:
                workTagData[w] = 1
            else:
                workTagData[w] += 1
    result = sorted(workTagData.items(), key=lambda x: x[1], reverse=True)[:20]
    technologyRow = []
    technologyColum = []
    for k, v in result:
        technologyRow.append(k)
        technologyColum.append(v)
    return technologyRow, technologyColum


def getCompanyStatusData():
    jobs = getAllJobs()
    statusData = {}
    for job in jobs:
        if statusData.get(job.companyStatus, -1) == -1:
            statusData[job.companyStatus] = 1
        else:
            statusData[job.companyStatus] += 1
    result = []
    for k, v in statusData.items():
        result.append({
            'name': k,
            'value': v}
        )
    return result
