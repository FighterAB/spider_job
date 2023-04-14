from .getPublicData import *


def getPageData():
    jobs = getAllJobs()
    jobType = {}
    for job in jobs:
        if jobType.get(job.type, -1) == -1:
            jobType[job.type] = 1
        else:
            jobType[job.type] += 1
    # print(list(educationList.keys()),workExperienceList,list(jobType.keys()))
    return list(educationList.keys()), workExperienceList, list(jobType.keys())

def changeSelfInfo(newInfo,fileInfo):
    user = User.objects.get(username=newInfo.get('username'))
    user.educational = newInfo.get('educational')
    user.workExperience = newInfo.get('workExperience')
    user.address = newInfo.get('address')
    user.work = newInfo.get('work')
    if fileInfo.get('avatar') !=None:
        user.avatar = fileInfo.get('avatar')
    user.save()
