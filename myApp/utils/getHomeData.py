from .getPublicData import *
import time
import json


# 获取当前时间
def getNowTime():
    timeFormat = time.localtime()
    year = timeFormat.tm_year
    month = timeFormat.tm_mon
    day = timeFormat.tm_mday
    return year, monthList[month - 1], day


# 获取用户创建时间
def getUserCreateTime():
    users = getAllUsers()
    data = {}
    # 将用户创建账户时间以{时间：个数}格式进行存储
    for user in users:

        if data.get(str(user.createTime), -1) == -1:
            data[str(user.createTime)] = 1
        else:
            data[str(user.createTime)] += 1
    result = []
    # 对data进行遍历获取每个时间段的创建账户人数
    for k, v in data.items():
        result.append({
            'name': k,
            'value': v
        })
    return result


# 获取最新创建的用户信息
def getUserTops():
    users = getAllUsers()

    def sort_fn(item):
        return time.mktime(time.strptime(str(item.createTime), "%Y-%m-%d"))

    # 获取前六个用户
    users = list(sorted(users, key=sort_fn, reverse=True))[:6]
    return users
    # print(users)


# 获取全部标签
def getAllTags():
    jobs = JobInfo.objects.all()
    users = User.objects.all()
    educationsTop = '学历不限'
    salaryTop = 0
    salaryMonthTop = 0
    address = {}
    pratice = {}
    for job in jobs:
        # 获取岗位的最高学历
        if educationList[job.educational] < educationList[educationsTop]:
            educationsTop = job.educational
        # 判断是否为实习单位
        if job.pratice == 0:
            salary = json.loads(job.salary)[1]
            if salaryTop < salary:
                salaryTop = salary
        # 获取最高薪资
        if int(job.salaryMonth) > salaryMonthTop:
            salaryMonthTop = int(job.salaryMonth)
        # 获取优势城市
        if address.get(job.address, -1) == -1:
            address[job.address] = 1
        else:
            address[job.address] += 1

        # 获取岗位性质
        if pratice.get(job.pratice, -1) == -1:
            pratice[job.pratice] = 1
        else:
            pratice[job.pratice] += 1
    addressStr = sorted(address.items(), key=lambda x: x[1], reverse=True)[:3]
    addressTop = ''

    praticeMax = sorted(pratice.items(), key=lambda x: x[1], reverse=True)

    for index, item in enumerate(addressStr):
        if index == len(addressStr) - 1:
            addressTop += item[0]
        else:
            addressTop += item[0] + ','
    return len(jobs), len(users), educationsTop, salaryTop, addressTop,salaryMonthTop,praticeMax[0][0]

def getJobTimeData():
    jobs = getAllJobs()
    JobTimes = {}
    for job in jobs:
        if JobTimes.get(str(job.createTime),-1)==-1:
            JobTimes[str(job.createTime)]=1
        else:
            JobTimes[str(job.createTime)]+=1
    row = []
    column = []
    for k, v in JobTimes.items():
        row.append(k)
        column.append(v)
    return row,column
    print(row,column)


# def gettableData():
#     jobs = getAllJobs()
#     for job in jobs:
#         job.workTag = '/'.join(json.loads(job.workTag))
#         if job.workTag != '无':
#             job.companyTags = '/'.join(json.loads(job.companyTag)[0].split(','))
#         if job.companyPenple== '[0,10000]':
#             job.companyPenple = '10000以上'
#         else:
#             job.companyPenple = json.loads(job.companyPenple)
#             job.companyPenple = list(map(lambda x:str(x) +'人',job.companyPenple))
#             job.companyPenple = '-'.join(job.companyPenple)
#         job.salary = json.loads(job.salary)[1]
#     return jobs
