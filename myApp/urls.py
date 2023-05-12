from django.urls import path
from myApp import views

urlpatterns = [
    path('login/', views.login, name='login'),

    path('regist/', views.registry, name='registry'),

    path('home', views.home, name="home"),

    path('logout/', views.logout, name="logout"),

    path('selfInfo/', views.selfInfo, name="selfInfo"),

    path('changePassword/', views.changePassword, name="changePassword"),

    path('tableData/', views.tableData, name="tableData"),

    path('historyData/', views.historyData, name="historyData"),

    path('addHistory/<int:jobId>', views.addHistory, name="addHistory"),

    path('removeHistory/<int:hisId>', views.removeHistory, name="removeHistory"),

    path('salary/', views.salary, name="salary"),

    path('company/', views.company, name="company"),

    path('companyTags/', views.companyTags, name="companyTags"),

    path('educational/', views.educational, name="educational"),

    path('companyStatus/', views.companyStatus, name="companyStatus"),

    path('address/', views.address, name="address"),

    path('recommend/', views.recommend, name="recommend"),

]
