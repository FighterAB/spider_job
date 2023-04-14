from django.db import models


# Create your models here.
class JobInfo(models.Model):
    # id = models.AutoField('id',primary_key=True)
    title = models.CharField('岗位名称', max_length=200, default='')
    address = models.CharField('省会', max_length=255, default='')
    type = models.CharField('职业', max_length=255, default='')
    educational = models.CharField('学历', max_length=255, default='')
    workExperience = models.CharField('工作经验', max_length=255, default='')
    workTag = models.CharField('工作标签', max_length=255, default='')
    salary = models.CharField('薪资', max_length=255, default='')
    salaryMonth = models.CharField('年终奖', max_length=255, default='')
    companyTags = models.CharField('公司福利', max_length=650, default='')
    hrWork = models.CharField('人事职位', max_length=255, default='')
    hrName = models.CharField('人事姓名', max_length=255, default='')
    pratice = models.BooleanField('是否为实习单位', max_length=255, default='')
    companyTitle = models.CharField('公司名称', max_length=255, default='')
    companyAvatar = models.CharField('公司头像', max_length=255, default='')
    companyNature = models.CharField('公司性质', max_length=255, default='')
    companyStatus = models.CharField('公司状态', max_length=255, default='')
    companyPeople = models.CharField('公司人数', max_length=255, default='')
    detailUrl = models.CharField('详情页面', max_length=300, default='')
    companyUrl = models.CharField('公司详情页面', max_length=255, default='')
    createTime = models.DateField('创建时间', auto_now_add=True)
    dist = models.CharField('公司地址', max_length=255, default='')

    class Meta:
        db_table = 'bossjobInfo'


class User(models.Model):
    # id = models.AutoField('id',primary_key=True)
    username = models.CharField('用户名', max_length=255, default='')
    password = models.CharField('密码', max_length=255, default='')
    educational = models.CharField('学历', max_length=255, default='')
    workExperience = models.CharField('工作经验', max_length=255, default='')
    address = models.CharField('意向城市', max_length=255, default='')
    work = models.CharField('意向岗位', max_length=255, default='')
    avatar = models.FileField('头像', upload_to="avatar", default='avatar/default.png')
    createTime = models.DateField('创建时间', auto_now_add=True)

    class Meta:
        db_table = 'user'

class Admin(models.Model):
    username = models.CharField('用户名', max_length=255,)
    password = models.CharField('密码', max_length=255,)
    class Meta:
        db_table = 'admin'


class History(models.Model):
    job = models.ForeignKey(JobInfo, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    count = models.IntegerField('点击次数', default=0)

    class Meta:
        db_table = 'history'
