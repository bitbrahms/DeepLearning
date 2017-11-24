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



#设置访问网站的请求头部信息
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1) \
AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'}
houseary=[]#建立空列表放房屋信息
domain='http://sh.lianjia.com'#为了之后拼接子域名爬取详细信息
for i in range(1,2):#爬取399页，想爬多少页直接修改替换掉400，不要超过总页数就好
    res=requests.get('http://sh.lianjia.com/ershoufang/d'+str(i),headers=headers)#爬取拼接域名
    soup = BeautifulSoup(res.text,'html.parser')#使用html筛选器
#print(soup)
for j in range(0,1):#网站每页呈现30条数据，循环爬取
    url1=soup.select('.prop-title a')[j]['href']#选中class=prop-title下的a标签里的第j个元素的href子域名内容
    url=domain+url1#构造子域名
    #print(url)
        #houseary.append(gethousedetail1(url,soup,j))#传入自编函数需要的参数
#def gethousedetail1(url,soup,j):#定义函数，目标获得子域名里的房屋详细信息
    info={}#构造字典，作为之后的返回内容
    
    info['行政区']=soup.select('.info-col a')[1+3*j].get_text()#通过传入的j获取所在
    info['小区']=soup.select('.info-col a')[0+3*j].get_text()
    info['位置']=soup.select('.info-col a')[2+3*j].get_text()
    res_sub=requests.get(url,headers=headers)#使用子域名
    soup_sub=BeautifulSoup(res_sub.text,'html.parser')#提取子域名内容,即页面详细信息
    #print(soup_sub)
    #print(soup_sub.select('.module-row li'))

    b=soup_sub.find_all(lambda tag: tag.name=='span' and tag.get('class')==['item-cell'])
    for info in b:#提取class=content标签下的li标签房屋信息
        #print(info.get_text())
        a=info.get_text(strip=True)#推荐的去空格方法，比strip（）好用
        #a=info.span.string
        print(a)
        #a=info.get_text()
        if '\n' in a:#要有冒号的，用中文的冒号，因为网页中是中文  
            key,value=a.split('\n')#根据冒号切分出键和值
            info[key]=value
    info['总价']=soup_sub.select('.bold')[0].text.strip()#提取总价信息
    #print(info)
    #return info#传回这一个页面的详细信息