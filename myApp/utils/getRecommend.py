from .getPublicData import *
from myApp.models import JobInfo
from myApp.models import User
import json
import random


def getRecommend(userInfo):
    user = User.objects.get(username=userInfo.username)
    jobs = JobInfo.objects.filter(address=userInfo.address, type=userInfo.work, workExperience=userInfo.workExperience)
    jobs = random.sample(list(jobs), 10)

    def map_fn(item):
        item.salary = json.loads(item.salary)
        item.companyPeople = json.loads(item.companyPeople)
        item.workTag = json.loads(item.workTag)
        if item.companyTags != '无':
            item.companyTags = json.loads(item.companyTags).split('，')
        if not item.pratice:
            item.salary = list(map(lambda x: str(int(x / 1000)), item.salary))
        else:
            item.salary = list(map(lambda x: str(x), item.salary))
        item.salary = '-'.join(item.salary)
        item.companyPeople = list(map(lambda x: str(x), item.companyPeople))
        item.companyPeople = '-'.join(item.companyPeople)
        return item

    jobs = list(map(map_fn, jobs))

    return jobs


