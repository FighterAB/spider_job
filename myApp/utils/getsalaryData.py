from .getPublicData import *
from myApp.models import JobInfo
import json


def getPageDate():
    return list(educationList.keys()), workExperienceList

#薪资情况
def getBarData(defaulteducation, defaultworkExperience):
    if defaulteducation == '不限' and defaultworkExperience == '不限':
        jobs = JobInfo.objects.all()
    elif defaulteducation == '不限':
        jobs = JobInfo.objects.filter(workExperience=defaultworkExperience)
    elif defaultworkExperience != '不限':
        jobs = JobInfo.objects.filter(educational=defaulteducation)
    else:
        jobs = JobInfo.objects.filter(educational=defaulteducation, workExperience=defaultworkExperience)
    jobsType = {}
    for job in jobs:
        if job.pratice == 0:
            if jobsType.get(job.type, -1) == -1:
                jobsType[job.type] = [json.loads(job.salary)[1]]
            else:
                jobsType[job.type].append(json.loads(job.salary)[1])
    barData = {}
    for k, v in jobsType.items():
        if not barData.get(k, 0):
            # range对应salaryList中数据的个数5
            barData[k] = [0 for x in range(5)]
        for i in v:
            s = i / 1000
            if s < 10:
                barData[k][0] += 1
            elif s >= 10 and s < 20:
                barData[k][1] += 1
            elif s >= 20 and s < 30:
                barData[k][2] += 1
            elif s >= 30 and s < 40:
                barData[k][3] += 1
            else:
                barData[k][4] += 1
    legends = list(barData.keys())
    if len(legends) == 0: legends = None
    return salaryList, barData, legends


#平均薪资
def averageFn(list):
    total = 0
    for i in list:
        total += i
    return round(total / len(list), 1)

#平均薪资饼图
def pieData():
    jobs = getAllJobs()
    jobsType = {}
    for job in jobs:
        if job.pratice == 1:
            if jobsType.get(job.type, -1) == -1:
                jobsType[job.type] = [json.loads(job.salary)[1]]
            else:
                jobsType[job.type].append(json.loads(job.salary)[1])
    result = []
    for k, v in jobsType.items():
            result.append({
                'name': k,
                'value': averageFn(v)
            })
    return result

#漏斗图
def getFunnelData():
    jobs = JobInfo.objects.filter(salaryMonth__gt=0)
    data = {}
    for job in jobs:
        x = str(job.salaryMonth)+'薪'
        if data.get(x, -1) == -1:
            data[x] = 1
        else:
            data[x] += 1
    result = []
    for k, v in data.items():
        result.append({
            'name': k,
            'value': v
        })
    return  result
