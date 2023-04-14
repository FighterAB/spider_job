from .getPublicData import *
import json

def getPageData():
    jobs = getAllJobs()
    typeData = []
    for job in jobs: typeData.append(job.type)
    return list(set(typeData))


def getCompanyBar(type):
    if type == 'all':
        jobs = getAllJobs()
    else:
        jobs = JobInfo.objects.filter(type=type)
    natureData = {}
    for job in jobs:
        if natureData.get(job.companyNature, -1) == -1:
            natureData[job.companyNature] = 1
        else:
            natureData[job.companyNature] += 1
    natureList = list(sorted(natureData.items(), key=lambda x: x[1], reverse=True))
    rowData = []
    columData = []
    for k, v in natureList:
        rowData.append(k)
        columData.append(v)
    # 前二十条数据
    return rowData[:20], columData[:20]


def getCompanyPie(type):
    if type == 'all':
        jobs = getAllJobs()
    else:
        jobs = JobInfo.objects.filter(type=type)
    addressData = {}
    for job in jobs:
        if addressData.get(job.address, -1) == -1:
            addressData[job.address] = 1
        else:
            addressData[job.address] += 1
    result = []
    for k, v in addressData.items():
        result.append({
            'name': k,
            'value': v
        })
    return result[:40]
    # natureList = list(sorted(addressData.items(), key=lambda x: x[1], reverse=True))


def getCompanyPeople(type):
    if type == 'all':
        jobs = getAllJobs()
    else:
        jobs = JobInfo.objects.filter(type=type)

    def map_fn(item):
        item.companyPeople = json.loads(item.companyPeople)[1]
        return item

    jobs = list(map(map_fn, jobs))
    data = [0 for i in range(6)]

    for job in jobs:
        p = job.companyPeople
        if p <= 20:
            data[0] += 1
        elif p <= 100:
            data[1] += 1
        elif p <= 500:
            data[2] += 1
        elif p <= 1000:
            data[3] += 1
        elif p < 10000:
            data[4] += 1
        else:
            data[5] += 1
    return companyPeople,data
