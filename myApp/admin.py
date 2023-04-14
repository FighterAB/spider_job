from django.contrib import admin
from myApp.models import JobInfo,User,History

class JobManager(admin.ModelAdmin):
    list_display = ["id","title", "address", "type", "educational", "workExperience", "workTag", "salary", "salaryMonth",
                     "companyTags", "hrWork", "hrName", "pratice", "companyTitle", "companyAvatar", "companyNature",
                     "companyStatus", "companyPeople", "detailUrl", "companyUrl", "dist"]
    #选择可以跳转连接的字段
    list_display_links = ["title"]
    #不需要进入详情页面即可修改
    list_editable = ['address']
    #过滤操作(过滤器)
    list_filter = ["educational", "type"]
    #搜索字段,只能选一个字段，多选会报错
    search_fields = ['title']
    #使选择无法修改
    readonly_fields =['id']
    #分页(20数据为一页)
    list_per_page = 20
    #时间
    date_hierarchy = 'createTime'

admin.site.register(JobInfo,JobManager)
