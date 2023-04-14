from .getPublicData import *
from myApp.models import JobInfo
import json


def getPageData():
    return hotCity

# 薪资分布情况
def getSalaryData(city):
    jobs = JobInfo.objects.filter(address=city)
    salary = []
    for job in jobs:
        if job.pratice == 0:
            salary.append(json.loads(job.salary)[1])
    salaryColumn = [0 for i in range(len(salaryList))]
    for i in salary:
        s = i / 1000
        if s < 10:
            salaryColumn[0] += 1
        elif s < 20:
            salaryColumn[1] += 1
        elif s < 30:
            salaryColumn[2] += 1
        elif s < 40:
            salaryColumn[3] += 1
        else:
            salaryColumn[4] += 1
    return salaryList, salaryColumn

# 公司人数分布情况
def companyPeopleData(city):
    jobs = JobInfo.objects.filter(address=city)
    companyPeoples = []
    for job in jobs:
        companyPeoples.append(json.loads(job.companyPeople)[1])
    # print(companyPeople)
    companyPeopleColumn = [0 for i in range(len(companyPeople))]
    for s in companyPeoples:
        if s <= 20:
            companyPeopleColumn[0] += 1
        elif s < 100:
            companyPeopleColumn[1] += 1
        elif s < 500:
            companyPeopleColumn[2] += 1
        elif s < 1000:
            companyPeopleColumn[3] += 1
        elif s < 10000:
            companyPeopleColumn[4] += 1
        else:
            companyPeopleColumn[5] += 1
    result = []
    for index,item in enumerate(companyPeopleColumn):
        result.append({
            'name': companyPeople[index],
            'value': item
        })

    return result

# 学历要求
def getEducationData(city):
    jobs = JobInfo.objects.filter(address=city)
    education = {}
    for job in jobs:
        if education.get(job.educational,-1) ==-1:
            education[job.educational] = 1
        else:
            education[job.educational] += 1
    result = []
    for index,item in education.items():
        result.append({
            'name': index,
            'value': item
        })
    return result

def getDistData(city):
    jobs = JobInfo.objects.filter(address=city)
    distData = {}
    for job in jobs:
        if distData.get(job.dist,-1) ==-1:
            distData[job.dist] = 1
        else:
            distData[job.dist] += 1
    result = []
    for k,v in distData.items():
        result.append({
            'name': k,
            'value': v,
        })
    return result
