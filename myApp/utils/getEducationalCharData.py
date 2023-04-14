import json

from .getPublicData import *
from myApp.models import JobInfo


def getPageData():
    return list(educationList.keys())


def getAverage(list):
    # print(list)
    result = 0
    for i in list:
        result += i
    return round(result / len(list), 2)


# 工作年限薪涨幅度情况
def getExpirenceData(educational):
    hasEmpty = False
    if educational == '不限':
        jobs = JobInfo.objects.all()
    else:
        # jobs = JobInfo.objects.filter(educational=educational)
        jobs = JobInfo.objects.filter(educational=educational)
    workExp = {}
    workPeople = {}
    for job in workExperienceList:
        workExp[job] = []
        workPeople[job] = 0
    # print(workExp, workPeople)
    for job in jobs:
        for k, v in workExp.items():
            if job.workExperience == k:
                if job.pratice == 0:
                    workExp[k].append(json.loads(job.salary)[1])
                    workPeople[k] += 1

    for k, v in workExp.items():
        try:
            workExp[k] = getAverage(v)
        except:
            workExp[k] = 0

    if len(jobs) == 0:
        hasEmpty = True

    return list(workExp.keys()), list(workExp.values()), list(workPeople.values()), hasEmpty


# 学历人数
def getPeople():
    jobs = getAllJobs()

    educationData = {}
    for job in jobs:
        if educationData.get(job.educational, -1) == -1:
            educationData[job.educational] = 1
        else:
            educationData[job.educational] += 1
    return list(educationData.keys()), list(educationData.values())
