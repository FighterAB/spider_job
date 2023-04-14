import jieba
from matplotlib import pyplot as plt
from wordcloud import WordCloud
from PIL import Image
import numpy as np
from pymysql import *
import json

# 公司福利
def get_img_1(field, targetImageSrc, resImdSrc):
    # 连接数据库
    con = connect(host='127.0.0.1', port=3306, user='root', passwd='root', db='job', charset='utf8')
    cursor = con.cursor()
    sql = f"select {field} from bossjobinfo"
    cursor.execute(sql)
    data = cursor.fetchall()
    # print(data)
    text = ''
    for i in data:
        if i[0] != '无':
            companyTagsArr = json.loads(i[0]).split('，')
            for j in companyTagsArr:
                text = text + j
    cursor.close()
    con.close()
    data_cut = jieba.cut(text, cut_all=False)
    stop_words = []
    with open('./stopwords.txt', 'r', encoding='utf-8') as f:
        for line in f:
            if len(line) > 0:
                stop_words.append(line.strip())
    data_result = [x for x in data_cut if x not in stop_words]
    string = ' '.join(data_result)

    #    图片
    img = Image.open(targetImageSrc)
    img_arr = np.array(img)
    wc = WordCloud(
        # 背景颜色
        background_color='white',
        #
        mask=img_arr,
        font_path='STHUPO.TTF',
    )
    wc.generate_from_text(string)

    # 绘制图片
    fig = plt.figure(1)
    plt.imshow(wc)

    plt.axis("off")
    plt.savefig(resImdSrc, dpi=800)




# 公司
def get_img_2(field, targetImageSrc, resImdSrc):
    # 连接数据库
    con = connect(host='127.0.0.1', port=3306, user='root', passwd='root', db='job', charset='utf8')
    cursor = con.cursor()
    sql = f"select {field} from bossjobinfo"
    cursor.execute(sql)
    data = cursor.fetchall()
    # print(data)
    text = ''
    for i in data:
        text+=i[0]
    cursor.close()
    con.close()
    data_cut = jieba.cut(text, cut_all=False)
    stop_words = []
    with open('./stopwords.txt', 'r', encoding='utf-8') as f:
        for line in f:
            if len(line) > 0:
                stop_words.append(line.strip())
    data_result = [x for x in data_cut if x not in stop_words]
    string = ' '.join(data_result)

    #    图片
    img = Image.open(targetImageSrc)
    img_arr = np.array(img)
    wc = WordCloud(
        # 背景颜色
        background_color='white',
        #
        mask=img_arr,
        font_path='STHUPO.TTF',
    )
    wc.generate_from_text(string)

    # 绘制图片
    fig = plt.figure(1)
    plt.imshow(wc)

    plt.axis("off")
    plt.savefig(resImdSrc, dpi=800)

get_img_1('companyTags', '../static/picture/1.png', '../static/picture/companytags_cloud1.jpg')
get_img_2('title', '../static/picture/2.png', '../static/picture/companytags_cloud2.jpg')