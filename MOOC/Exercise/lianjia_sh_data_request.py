# -*- coding: utf-8 -*-
"""
Created on Mon Nov 20 22:42:45 2017

@author: manny
"""

import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import time

######数据获取################################
#############################################

#设置headers信息
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1) \
AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'}
domain='http://sh.lianjia.com'#主域名
info_total=[]#存放信息的列表
for i in range(1,2):#爬取总页数
    res=requests.get('http://sh.lianjia.com/ershoufang/d'+str(i),headers=headers)#爬取拼接域名
    soup = BeautifulSoup(res.text,'html.parser')#使用html筛选器
    for j in range(0,30):#网站每页呈现30条数据，循环爬取
        url1=soup.select('.prop-title a')[j]['href']
        url=domain+url1#构造子域名
        pi=[]
        a=[soup.select('.info-col a')[1+3*j].get_text()]
        res_sub=requests.get(url,headers=headers)
        soup_sub=BeautifulSoup(res_sub.text,'html.parser')
        b=[soup_sub.select('.maininfo-estate-address')[0].text.strip()]
        c=[soup_sub.select('.baseinfo-parking-spot')[0].text.strip()]
        d=[soup_sub.select('.price-num')[0].text.strip()]
        pi=pi+a+d+b+c
        a=soup_sub.find_all(lambda tag: tag.name=='span' and tag.get('class')==['item-cell'])
        for b in a:
            pi.append(b.get_text(strip=True))
        if len(pi) > 28:
            for i in range(0,3):
                pi.pop(20)
        info_total.append(pi)
        time.sleep(0.5)
columns=['行政区','price','地点','车位','最低首付','参考月供','环线信息','小区名称','房源编号','房屋户型',\
    '配备电梯','areas','供暖方式','所在楼层','装修情况','房屋朝向','上次交易','房本年限','售房原因','房屋类型',\
    '挂牌均价','建筑年代','物业类型','楼栋总数','房屋总数','物业公司','开发商','挂牌房源']
df=pd.DataFrame(info_total,columns=columns)
ex_list1=list(df.areas)
ex_list=[]
for i in ex_list1:
    if(i != "暂无数据"):
        ex_list.append(i)
df=df[df.areas.isin(ex_list)]
df.to_csv('data_sh.csv',encoding='utf-8-sig')