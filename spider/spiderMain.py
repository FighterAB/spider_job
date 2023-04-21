import linecache
import random

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import csv
import os
import time
import json
import django
import pandas as pd

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Jop_spider.settings')
django.setup()

from myApp.models import JobInfo


# server = Service('./chromedriver.exe')
# options  = webdriver.ChromeOptions()
# options.add_experimental_option('excludeSwitches', ['enable-automation'])
# browser = webdriver.Chrome(service=server,options=options)


class spider(object):

    def getProxy(self):
        count = len(open('IP.txt', 'r').readlines())
        j = random.randint(1, count)
        line = linecache.getline('IP.txt', j)
        list = line.split("'")
        proxy = '--proxy-server=' + list[1].lower() + "://" + list[3]
        return proxy
    def __init__(self, type, page):
        self.type = type  # 岗位关键正
        self.page = page  # 页码数
        self.spiderUrl = 'https://www.zhipin.com/web/geek/job?query=%s&city=100010000&page=%s'

    def startBrowser(self):
        server = Service('./chromedriver.exe')
        options = webdriver.ChromeOptions()
        # 代理IP
        proxy = self.getProxy()
        options.add_argument(proxy)
        # 浏览器复用
        options.add_experimental_option('debuggerAddress', 'localhost:9222 ')  # chrome.exe --remote-debugging-port=9222
        # options.add_experimental_option('excludeSwitches', ['enable-automation'])
        browser = webdriver.Chrome(service=server, options=options)
        return browser

    def main(self, page):
        if self.page > page: return
        browser = self.startBrowser()
        print("正在爬取的页面路径" + self.spiderUrl % (self.type, self.page))
        browser.get(self.spiderUrl % (self.type, self.page))
        time.sleep(5)

        job_list = browser.find_elements(by=By.XPATH, value='//ul[@class="job-list-box"]/li')
        for index, job in enumerate(job_list):
            try:
                jobData = []
                print("正在爬取第%d个数据" % (index + 1))

                # title
                title = job.find_element(by=By.XPATH,
                                         value=".//a[@class='job-card-left']/div[contains(@class,'job-title')]/span[@class='job-name']").text

                # address
                addresses = job.find_element(by=By.XPATH,
                                             value=".//a[@class='job-card-left']/div[contains(@class,'job-title')]/span[@class='job-area-wrapper']/span").text.split(
                    '·')
                address = addresses[0]

                # dist
                if len(addresses) != 1:
                    dist = addresses[1]
                else:
                    dist = ''

                # type
                type = self.type

                tag_list = job.find_elements(by=By.XPATH,
                                             value=".//a[@class='job-card-left']/div[contains(@class,'job-info')]/ul/li")
                if len(tag_list) == 2:
                    # educational
                    educational = tag_list[1].text
                    # #workExperience
                    workExperience = tag_list[0].text
                else:
                    # educational
                    educational = tag_list[2].text
                    # #workExperience
                    workExperience = tag_list[1].text

                # hrname
                hrName = job.find_element(by=By.XPATH,
                                          value=".//a[@class='job-card-left']/div[contains(@class,'job-info')]/div[@class='info-public']").text

                # hrWork
                hrWork = job.find_element(by=By.XPATH,
                                          value=".//a[@class='job-card-left']/div[contains(@class,'job-info')]/div[@class='info-public']/em").text

                # workTag
                workTag = job.find_elements(by=By.XPATH,
                                            value=".//div[contains(@class,'job-card-footer')]/ul[@class='tag-list']/li")
                workTag = json.dumps(list(map(lambda x: x.text, workTag)),ensure_ascii=False)  # 不明白

                # pratice

                pratice = 0  # 实习

                # salary
                salaries = job.find_element(by=By.XPATH,
                                            value=".//a[@class='job-card-left']/div[contains(@class,'job-info')]/span[@class='salary']").text
                if salaries.find('K') != -1:
                    salaries = salaries.split('·')
                    if (len(salaries) == 1):
                        # salary

                        salary = list(map(lambda x: int(x) * 1000, salaries[0].replace('K', '').split('-')))
                        # salaryMonth
                        salaryMonth = '0薪'
                    else:
                        # salary
                        salary = list(map(lambda x: int(x) * 1000, salaries[0].replace('K', '').split('-')))
                        # salaryMonth
                        salaryMonth = salaries[1]
                else:
                    # salary
                    salary = list(map(lambda x: int(x), salaries.replace('元/天', '').split('-')))
                    # salaryMonth
                    salaryMonth = '0薪'
                    pratice = 1

                # companyTitle
                companyTitle = job.find_element(by=By.XPATH,
                                                value=".//div[@class='job-card-right']/div[@class='company-info']/h3/a").text

                # companyAvatar
                companyAvatar = job.find_element(by=By.XPATH,
                                                 value=".//div[@class='job-card-right']/div[@class='company-logo']/a/img").get_attribute(
                    'src')

                companyInfo = job.find_elements(by=By.XPATH,
                                                value=".//div[@class='job-card-right']/div[@class='company-info']/ul[@class='company-tag-list']/li")
                if (len(companyInfo) == 3):
                    # companyNature
                    companyNature = companyInfo[0].text
                    # companyStatus
                    companyStatus = companyInfo[1].text
                    # companyPeople
                    companyPeople = companyInfo[2].text
                    if (companyPeople != "10000人以上"):
                        companyPeople = list(map(lambda x: int(x), companyInfo[2].text.replace('人', '').split('-')))
                    else:
                        companyPeople = [0, 10000]
                else:
                    # companyNature
                    companyNature = companyInfo[0].text
                    # companyStatus
                    companyStatus = "未融资"
                    # companyPeople
                    companyPeople = companyInfo[1].text
                    if (companyPeople != "10000人以上"):
                        companyPeople = list(map(lambda x: int(x), companyInfo[1].text.replace('人', '').split('-')))
                    else:
                        companyPeople = [0, 10000]
                # companyTags
                companyTags = job.find_element(by=By.XPATH,
                                               value=".//div[contains(@class,'job-card-footer')]/div[@class='info-desc']").text
                if not companyTags:
                    companyTags = "无"
                else:
                    companyTags = json.dumps(companyTags,ensure_ascii=False)
                    # companyTags = json.dumps(companyTags.split('，'))

                # detailUrl
                detailUrl = job.find_element(by=By.XPATH,
                                             value=".//a[@class='job-card-left']").get_attribute('href')

                # companyUrl
                companyUrl = job.find_element(by=By.XPATH,
                                              value=".//div[@class='job-card-right']/div[@class='company-info']/h3/a").get_attribute(
                    'href')

                # # dist
                # dist = job.find_element(by=By.XPATH,
                #                          value=".//div[@class='job-card-right']/div[contains(@class,'job-card-footer')]/div[@class='info-desc']/span[@class='job-dist']").text
                # print(title,address,type,educational,workExperience,workTag,salary,salaryMonth,
                #       companyTags,hrWork,hrName,pratice,companyTitle,companyAvatar,companyNature,
                #       companyStatus,companyPeople,detailUrl,companyUrl,dist)

                jobData.append(title)
                jobData.append(address)
                jobData.append(type)
                jobData.append(educational)
                jobData.append(workExperience)
                jobData.append(workTag)
                jobData.append(salary)
                jobData.append(salaryMonth)
                jobData.append(companyTags)
                jobData.append(hrWork)
                jobData.append(hrName)
                jobData.append(pratice)
                jobData.append(companyTitle)
                jobData.append(companyAvatar)
                jobData.append(companyNature)
                jobData.append(companyStatus)
                jobData.append(companyPeople)
                jobData.append(detailUrl)
                jobData.append(companyUrl)
                jobData.append(dist)

                self.save_to_csv(jobData)

            except:
                pass

        self.page += 1
        self.main(page)

        # dist

    def clear_csv(self):
        df = pd.read_csv('./temp.csv')
        df.dropna(inplace=True)
        df.drop_duplicates(inplace=True)
        df['salaryMonth'] = df['salaryMonth'].map(lambda x: x.replace('薪', ''))
        print("总数据为%d" % df.shape[0])
        return df.values

    def save_to_sql(self):
        data = self.clear_csv()
        for job in data:
            # 修改数据
            # JobInfo.objects.filter(title=job[0],address=job[1],type=job[2],educational=job[3],hrWork=job[9],hrName=job[10],companyTitle=job[12]).update(companyTags=job[8])

            # 添加数据
            JobInfo.objects.create(
                title=job[0],
                address=job[1],
                type=job[2],
                educational=job[3],
                workExperience=job[4],
                workTag=job[5],
                salary=job[6],
                salaryMonth=job[7],
                companyTags=job[8],
                hrWork=job[9],
                hrName=job[10],
                pratice=job[11],
                companyTitle=job[12],
                companyAvatar=job[13],
                companyNature=job[14],
                companyStatus=job[15],
                companyPeople=job[16],
                detailUrl=job[17],
                companyUrl=job[18],
                dist=job[19]
            )

    def save_to_csv(self, rowData):
        with open('./temp.csv', 'a', newline='', encoding='utf-8') as wf:
            writer = csv.writer(wf)
            writer.writerow(rowData)

    def init(self):
        if not os.path.exists('./temp.csv'):
            with open('./temp.csv', 'a', encoding='utf-8', newline='') as wf:
                writer = csv.writer(wf)
                writer.writerow(
                    ["title", "address", "type", "educational", "workExperience", "workTag", "salary", "salaryMonth",
                     "companyTags", "hrWork", "hrName", "pratice", "companyTitle", "companyAvatar", "companyNature",
                     "companyStatus", "companyPeople", "detailUrl", "companyUrl", "dist"])


if __name__ == '__main__':
    job = ['python', 'php', 'c++', 'c#', 'go', 'web前端','大数据','爬虫',]
    # job = ['php', 'c语言', 'c++', 'c#', 'go', 'web前端', '大数据']
    # job = ['php', 'c语言']
    # job = [  'web前端', '大数据']
    # for i in range(len(job)):
    #     print("正在爬取%s的数据" % job[i])
    #     spiderObj = spider(type=job[i], page=1)
    #     spiderObj.init()
    #     spiderObj.main(10)
    # JobInfo.objects.all() #测试djangp是否引用成功 代表models引用成功 无其他作用
    spiderObj = spider(type='java', page=1)
    spiderObj.save_to_sql()
    # spiderObj.save_to_csv(list(map(lambda x: x.title, JobInfo.objects.all())))
