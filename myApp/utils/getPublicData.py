from myApp.models import *

# 月份
monthList = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
             'November', 'December']
# 教育水平
educationList = {
    '博士': 1,
    '硕士': 2,
    '本科': 3,
    '大专': 4,
    '高中': 5,
    '中专/中技': 6,
    '初中及以下': 7,
    '学历不限': 8,
}
# 工作经验
workExperienceList = ['经验不限', '在校/应届', '1-3年', '3-5年', '5-10年', '10年以上']

# 薪资分布情况
salaryList = ['0-10k', '10k-20k', '20k-30k', '30-40k', '40k以上']

companyPeople = ['20人以下', '100人以下', '500人以下', '1000人以下', '10000人以下', '10000人以上']

hotCity = ['南京', '北京', '上海', '深圳', '成都', '昆明', "郑州", '重庆', '广州', '东莞', '天津']


# 获取全部用户信息
def getAllUsers():
    return User.objects.all()


# 获取全部招聘信息
def getAllJobs():
    return JobInfo.objects.all()
