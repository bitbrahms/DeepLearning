# -*- coding: utf-8 -*-
"""
Created on Tue Nov 21 23:30:15 2017

@author: manny
"""

import requests
import time
from bs4 import BeautifulSoup
import re
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#设置列表页URL的固定部分
url = 'https://bj.lianjia.com/ershoufang/pg'
#设置访问网站的请求头部信息
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1) \
AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'}

#使用for循环生成1-100的数字，转化格式后与前面的URL固定部分拼成要抓取的URL。
#设置每两个页面间隔1秒。抓取到的页面保存在html中

html = ''
for i in range(1,3):
    url_new = (url + str(i) + '/')
    r = requests.get(url_new,headers=headers)
    html2 = r.text
    html += html2
    time.sleep(1)


#解析抓取的页面内容
lj = BeautifulSoup(html,'html.parser')

#提取房源总价
price=lj.find_all('div',attrs={'class':'priceInfo'})
pi=[]
for a in price:
    totalPrice=a.span.string
    pi.append(totalPrice)
print(pi)