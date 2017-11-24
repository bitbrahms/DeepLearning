# -*- coding: utf-8 -*-
"""
Created on Mon Nov 20 22:42:45 2017

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
url = 'https://bj.lianjia.com/ershoufang/'
#设置访问网站的请求头部信息
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1) \
AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'}

r =requests.get(url,headers=headers)
html = r.content
url = 'https://bj.lianjia.com/ershoufang/pg'
for i in range(2,5):
        i = str(i)
        a = (url + i + '/')
        r = requests.get(url=a,headers=headers)
        html2 = r.content
        html = html + html2
        time.sleep(0.5)


#解析抓取的页面内容
lj = BeautifulSoup(html,'lxml')
#提取房源总价
price=lj.find_all('div',attrs={'class':'priceInfo'})
pi=[]
for a in price:
    totalPrice=a.span.string
    pi.append(totalPrice)
#提取房源信息
houseInfo=lj.find_all('div',attrs={'class':'houseInfo'})
hi=[]
for b in houseInfo:
    house=b.get_text()
    hi.append(house)
#提取房源关注度
followInfo=lj.find_all('div',attrs={'class':'followInfo'})
fi=[]
for c in followInfo:
    follow=c.get_text()
    fi.append(follow)

#生成dataframe格式
house = pd.DataFrame({'totalprice':pi,'houseinfo':hi,'followinfo':fi})

print(house)

'''
#对房源信息进行分列
houseinfo_split = pd.DataFrame((x.split('|') for x in house.houseinfo),index=house.index,columns=['xiaoqu','huxing','mianji','chaoxiang','zhuangxiu','dianti'])
#将分列结果拼接回原数据表
house=pd.merge(house,houseinfo_split,right_index=True, left_index=True)
#对房源关注度进行分列
followinfo_split = pd.DataFrame((x.split('/') for x in house.followinfo),index=house.index,columns=['guanzhu','daikan','fabu'])
#将分列后的关注度信息拼接回原数据表
house=pd.merge(house,followinfo_split,right_index=True, left_index=True)

house=house.drop(['houseinfo', 'followinfo'], axis = 1)
house.to_csv('data_beijing.csv', encoding='utf_8_sig')
'''