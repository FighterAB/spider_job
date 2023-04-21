import linecache
import random

count  = len(open('IP.txt', 'r').readlines())
j = random.randint(1,count+1)
print(j)
line = linecache.getline('IP.txt',j)
print(line)
print('--proxy-server='+line.split("'")[1].lower()+"://"+line.split("'")[3])