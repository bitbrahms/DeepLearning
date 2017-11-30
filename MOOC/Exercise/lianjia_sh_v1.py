# -*- coding: utf-8 -*-
"""
Created on Mon Nov 20 22:42:45 2017

@author: manny
"""

import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time
import re

url='http://sh.lianjia.com/ershoufang/sh4478927.html'

#设置访问网站的请求头部信息
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1) \
AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'}

r = requests.get(url,headers=headers)

soup = BeautifulSoup(r.text,'html.parser')
pi=[]
a=soup.find_all(lambda tag: tag.name=='span' and tag.get('class')==['item-cell'])
for b in a:
    pi.append(b.get_text(strip=True))
print(pi)
if len(pi) > 24:
    for i in range(0,3):
        pi.pop(16)
print(len(pi))
print(pi)
'''

houseary=[]#建立空列表放房屋信息
#domain='http://sh.lianjia.com'#为了之后拼接子域名爬取详细信息
info_total=[]
#for i in range(1,3):#爬取399页，想爬多少页直接修改替换掉400，不要超过总页数就好
    res=requests.get('http://sh.lianjia.com/ershoufang/d'+str(i),headers=headers)#爬取拼接域名
    soup = BeautifulSoup(res.text,'html.parser')#使用html筛选器
    for j in range(0,30):#网站每页呈现30条数据，循环爬取
        url1=soup.select('.prop-title a')[j]['href']#选中class=prop-title下的a标签里的第j个元素的href子域名内容
        url=domain+url1#构造子域名
        info={}
        pi=[]
        a=[soup.select('.info-col a')[1+3*j].get_text()]
        
        res_sub=requests.get(url,headers=headers)
        soup_sub=BeautifulSoup(res_sub.text,'html.parser')
        
        b=[soup_sub.select('.baseinfo-parking-spot')[0].text.strip()]
        c=[soup_sub.select('.baseinfo-parking-spot')[0].text.strip()]
        d=[soup_sub.select('.price-num')[0].text.strip()]
        pi=pi+a+b+c+d
        #print(pi)
        #info['行政区']=soup.select('.info-col a')[1+3*j].get_text()
        #info['地点']=soup_sub.select('.maininfo-estate-address')[0].text.strip()
        #info['车位']=soup_sub.select('.baseinfo-parking-spot')[0].text.strip()  
        #info['总价']=soup_sub.select('.price-num')[0].text.strip()
        #df = pd.DataFrame(info)
        a=soup_sub.find_all(lambda tag: tag.name=='span' and tag.get('class')==['item-cell'])
        for b in a:
            pi.append(b.get_text(strip=True))
        info_total.append(pi)
print(len(info_total))

columns=['最低首付','参考月供','环线信息','小区名称','房源编号','房屋户型',\
    '配备电梯','建筑面积','供暖方式','所在楼层','装修情况','房屋朝向','上次交易','房本年限','售房原因','房屋类型',\
    '挂牌均价','建筑年代','物业类型','楼栋总数','房屋总数','物业公司','开发商','挂牌房源','行政区','地点','车位','总价']
df=pd.DataFrame(info_total)
df.to_csv('data_sh.csv',encoding='utf-8-sig')
'''