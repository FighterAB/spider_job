import json
from xml import etree
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import csv
import os
import time
import json
import django
import pandas as pd
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By

for i in range(1,31):
    if i != 1:
        url='https://www.yanglaocn.com/jianxun/yl/list_'+str(i)+'.html'
    else:
        url = 'https://www.yanglaocn.com/jianxun/yl/index.html'

    options = webdriver.Chrome(executable_path='./chromedriver.exe')
    options.get('https://www.yanglaocn.com/jianxun/yl/list_31.html')
    job_lists = options.find_elements(by=By.XPATH, value="//div[@class='newslistdiv']/div[@class='yl_dongtai_img_jx']")
    for index,job_list in enumerate(job_lists):
        title = job_list.find_element(by=By.XPATH,
                                 value=".//div[@class='yl_dongtai_img_bottom']/div[@class='yl_dongtai_img_bottom_text']/a").text
        with open('a.txt', 'a', encoding='utf-8') as file:
            file.write(title)
            file.write('\n')
            file.write('\n')
