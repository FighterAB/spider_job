from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.http import HttpResponse
from myApp import models
from myApp.models import User, Admin
from .utils.error import *
import hashlib
from .utils import getHomeData
from .utils import getSelfInfo
from .utils import getChangePasswordData
from .utils.error import *
from .utils import getTableData
from .utils import getHistoryData
from .utils import getsalaryData
from .utils import getCompanyCharData
from .utils import getEducationalCharData
from .utils import getCompanyStatusCharData
from .utils import getAddressCharData


# 登录
def login(request):
    if request.method == 'GET':
        return render(request, "login.html")
    elif request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        # md5加密
        md5 = hashlib.md5()
        md5.update(password.encode())
        password = md5.hexdigest()
        try:
            user_obj = User.objects.get(username=username, password=password)
            request.session['username'] = user_obj.username
            return redirect('home')
        except:
            return errorResponse(request, '用户名或密码错误！')

        # if user_obj:
        #     # return HttpResponse("登陆成功")
        #     queryset = models.Job.objects.all()
        #     return render(request, 'home.html', {'queryset': queryset, "user": user_obj})
        # else:
        #     return HttpResponse("登陆失败")


# 注册
def registry(request):
    if request.method == 'GET':
        return render(request, "registry.html")
    # elif request.method == 'POST':
    else:
        username = request.POST.get("username")
        pwd = request.POST.get("password")
        checkpwd = request.POST.get("checkPassword")
        try:
            # 查找用户
            User.objects.get(username=username)
        except:
            # 没有找到
            if pwd != checkpwd: return errorResponse(request, '两次密码不一致！')
            if not username or not pwd or not checkpwd: return errorResponse(request, '不允许为空！')
            if username == 'admin': return errorResponse(request, '管理员账户无法通过该方法创建！')
            # 密码md5加密
            md5 = hashlib.md5()
            md5.update(pwd.encode())
            pwd = md5.hexdigest()
            User.objects.create(username=username, password=pwd)
            return redirect('login')
        return errorResponse(request, '该用户已被注册！')


# 退出登录
def logout(request):
    request.session.clear()
    return redirect('login')


# 主页
def home(request):
    # queryset = models.Job.objects.filter(id=1).first()
    username = request.session.get('username')
    # 获取当前登录用户信息
    userInfo = User.objects.get(username=username)
    # 获取当前时间
    year, month, day = getHomeData.getNowTime()
    # 获取用户创建时间
    userCreateData = getHomeData.getUserCreateTime()
    # 获取最新创建的用户信息
    userTops = getHomeData.getUserTops()
    # 获取全部标签
    jobsLen, usersLen, educationsTop, salaryTop, addressTop, salaryMonthTop, praticeMax = getHomeData.getAllTags()
    return render(request, 'index.html', {
        'userInfo': userInfo,
        'dateInfo': {
            'year': year,
            'month': month,
            'day': day
        },
        'userCreateData': userCreateData,
        'userTops': userTops,
        'tagDict': {
            'jobsLen': jobsLen,
            'usersLen': usersLen,
            'educationsTop': educationsTop,
            'salaryTop': salaryTop,
            'addressTop': addressTop,
            'salaryMonthTop': salaryMonthTop,
            'praticeMax': praticeMax
        }
    })


# 个人信息
def selfInfo(request):
    username = request.session.get('username')
    userInfo = User.objects.get(username=username)
    educations, workExperience, jobList = getSelfInfo.getPageData()
    if request.method == 'POST':
        getSelfInfo.changeSelfInfo(request.POST, request.FILES)
        userInfo = User.objects.get(username=username)

    return render(request, 'selfinfo.html', {
        'userInfo': userInfo,
        'pagaData': {
            'educations': educations,
            'workExperience': workExperience,
            'jobList': jobList
        }
    })


# 修改密码
def changePassword(request):
    username = request.session.get('username')
    userInfo = User.objects.get(username=username)
    if request.method == 'POST':
        res = getChangePasswordData.changePassword(userInfo, request.POST)
        if res != None:
            return errorResponse(request, res)
        userInfo = User.objects.get(username=username)
    return render(request, 'changepassword.html', {
        'userInfo': userInfo,
    })


# 数据总览
def tableData(request):
    userInfo = User.objects.get(username=request.session.get('username'))
    tableData = getTableData.getTableData()
    # 分页
    paginator = Paginator(tableData, 10)
    cur_page = 1
    if request.GET.get('page'): cur_page = int(request.GET.get('page'))
    c_page = paginator.page(cur_page)
    page_range = []
    visiblenumber = 10
    min = int(cur_page - visiblenumber / 10)
    if min < 1:
        min = 1
    max = min + visiblenumber
    if max > paginator.page_range[-1]:
        max = paginator.page_range[-1]
    for i in range(min, max):
        page_range.append(i)

    return render(request, 'tableData.html', {
        'userInfo': userInfo,
        'c_page': c_page,
        'page_range': page_range,
        'paginator': paginator,
    })
    pass


# 历史查询
def historyData(request):
    userInfo = User.objects.get(username=request.session.get('username'))

    return render(request, 'historyData.html', {
        'userInfo': userInfo,
    })


def addHistory(request, jobId):
    userInfo = User.objects.get(username=request.session.get('username'))
    getHistoryData.addHistory(userInfo, jobId)
    return redirect('historyData')


# 薪资
def salary(request):
    userInfo = User.objects.get(username=request.session.get('username'))
    educations, worlExperiences = getsalaryData.getPageDate()
    defaultEducation = '不限'
    defaulWorkExperiences = '不限'
    if request.GET.get('educational'): defaultEducation = request.GET.get('educational')
    if request.GET.get('worlExperience'): defaulWorkExperiences = request.GET.get('worlExperience')
    salaryList, barData, legends = getsalaryData.getBarData(defaultEducation, defaulWorkExperiences)
    pieData = getsalaryData.pieData()
    FunnelData = getsalaryData.getFunnelData()
    return render(request, 'salaryChar.html', {
        'userInfo': userInfo,
        'educations': educations,
        'worlExperience': worlExperiences,
        'defaultEducation': defaultEducation,
        'defaulWorkExperiences': defaulWorkExperiences,
        'salaryList': salaryList,
        'barData': barData,
        'legends': legends,
        'pieData': pieData,
        'FunnelData': FunnelData,
    })
    pass


# 公司
def company(request):
    userInfo = User.objects.get(username=request.session.get('username'))
    typeList = getCompanyCharData.getPageData()
    type = 'all'
    if request.GET.get('type'): type = request.GET.get('type')
    rowBarData, columBarData = getCompanyCharData.getCompanyBar(type)
    pieData = getCompanyCharData.getCompanyPie(type)
    companyPeople, lineData = getCompanyCharData.getCompanyPeople(type)
    return render(request, 'companyChar.html', {
        'userInfo': userInfo,
        'typeList': typeList,
        'type': type,
        'rowBarData': rowBarData,
        'columBarData': columBarData,
        'pieData': pieData,
        'companyPeople': companyPeople,
        'lineData': lineData,
    })
    pass


# 公司标签
def companyTags(request):
    userInfo = User.objects.get(username=request.session.get('username'))
    return render(request, 'companyTags.html', {
        'userInfo': userInfo,
    })
    pass


# 学历
def educational(request):
    userInfo = User.objects.get(username=request.session.get('username'))
    educations = getEducationalCharData.getPageData()
    defaultEducation = '不限'
    if request.GET.get('educational'): defaultEducation = request.GET.get('educational')
    workExp, charDataColunmOne, charDataColunmTwo, hasEmpty = getEducationalCharData.getExpirenceData(defaultEducation)
    barDataRow, barDataColunm = getEducationalCharData.getPeople()
    return render(request, 'educational.html', {
        'userInfo': userInfo,
        'educations': educations,
        'defaultEducation': defaultEducation,
        'workExp': workExp,
        'charDataColunmOne': charDataColunmOne,
        'charDataColunmTwo': charDataColunmTwo,
        'hasEmpty': hasEmpty,
        'barDataRow': barDataRow,
        'barDataColunm': barDataColunm,
    })
    pass


# 公司融资情况
def companyStatus(request):
    userInfo = User.objects.get(username=request.session.get('username'))
    defaultType = '不限'
    if request.GET.get('type'): defaultType = request.GET.get('type')
    typeList = getCompanyStatusCharData.getPageData()
    technologyRow, technologyColum = getCompanyStatusCharData.getTechnologyData(defaultType)
    companyStatusData = getCompanyStatusCharData.getCompanyStatusData()
    return render(request, 'companyStatus.html', {
        'userInfo': userInfo,
        'typeList': typeList,
        'defaultType': defaultType,
        'technologyRow': technologyRow,
        'technologyColum': technologyColum,
        'companyStatusData': companyStatusData,
    })
    pass


# 公司地址
def address(request):
    userInfo = User.objects.get(username=request.session.get('username'))
    hotCity = getAddressCharData.getPageData()
    defaultCity = '南京'
    if request.GET.get('city'): defaultCity = request.GET.get('city')
    salaryList, salaryColumn = getAddressCharData.getSalaryData(defaultCity)
    companyPeopleData = getAddressCharData.companyPeopleData(defaultCity)
    educationalData = getAddressCharData.getEducationData(defaultCity)
    distData = getAddressCharData.getDistData(defaultCity)
    return render(request, 'addressChar.html', {
        'userInfo': userInfo,
        'hotCity': hotCity,
        'defaultCity': defaultCity,
        'salaryList': salaryList,
        'salaryColumn': salaryColumn,
        'companyPeopleData': companyPeopleData,
        'educationalData': educationalData,
        'distData': distData,
    })
    pass
