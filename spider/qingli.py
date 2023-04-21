
import numpy
import pandas as pd


data = pd.read_csv('./temp¸±±¾.csv',encoding='gbk')
print(data.head(10))
data.drop_duplicates(keep='first',inplace=True)
print(data.head(10))
data.to_csv('./test.csv',index=False,encoding='gbk')