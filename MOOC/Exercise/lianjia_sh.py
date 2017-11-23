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



headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) \
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

    #tmp=get_house_info(url,soup,j)
    #houseary.append(tmp)#传入自编函数需要的参数



'''
def get_house_info(url,soup,j):#定义函数，目标获得子域名里的房屋详细信息
    info={}#构造字典，作为之后的返回内容

    s0=soup.select('.info-col a')[1+3*j]#通过传入的j获取所在区的内容
    pat='<a.*?>(.*?)</a>'#构造提取正则
    info['diqu']=''.join(list(re.compile(pat).findall(str(s0))))#使用join将提取的列表转为字符串

    s1=soup.select('.info-col a')[0+3*j]#[0].text.strip()
    pat1='<span.*?>(.*?)</span>'
    info['didian']=''.join(list(re.compile(pat1).findall(str(s1))))

    s2=soup.select('.info-col a')[2+3*j]#[0].text.strip()1
    pat2='<a.*?>(.*?)</a>'
    info['weizhi']=''.join(list(re.compile(pat2).findall(str(s2))))
    #print(len(info))
    #q=requests.get(url)#使用子域名
    
    #soup=BeautifulSoup(q.text,'html.parser')#提取子域名内容,即页面详细信息
    
    for dd in soup.select('.content li'):#提取class=content标签下的li标签房屋信息
        a=dd.get_text(strip=True)#推荐的去空格方法，比strip（）好用
        if '：' in a:#要有冒号的，用中文的冒号，因为网页中是中文  
            key,value=a.split('：')#根据冒号切分出键和值
            info[key]=value
            info['总价']=soup.select('.bold')[0].text.strip()#提取总价信息
    print(len(info))
    return info
  #传回这一个页面的详细信息
  '''
  