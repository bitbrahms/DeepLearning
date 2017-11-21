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
url = 'https://bj.lianjia.com/ershoufang/pg'
#设置访问网站的请求头部信息
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1) \
AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'}

#使用for循环生成1-100的数字，转化格式后与前面的URL固定部分拼成要抓取的URL。
#设置每两个页面间隔1秒。抓取到的页面保存在html中

html = requests.get('https://bj.lianjia.com/ershoufang/', headers=headers).content
for i in range(1,2):
    url_new = (url + str(i) + '/')
    r = requests.get(url_new,headers=headers)
    html2 = r.content
    html = html + html2
    time.sleep(1)


#解析抓取的页面内容
lj = BeautifulSoup(html,'html.parser')

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

#将数据保存到csv文件中
house = pd.DataFrame({'totalprice':pi,'houseinfo':hi,'followinfo':fi})
#对房源信息进行分列
houseinfo_split = pd.DataFrame((x.split('|') for x in house.houseinfo),index=house.index,columns=['xiaoqu','huxing','mianji','chaoxiang','zhuangxiu','dianti'])
#将分列结果拼接回原数据表
house=pd.merge(house,houseinfo_split,right_index=True, left_index=True)
#对房源关注度进行分列
followinfo_split = pd.DataFrame((x.split('/') for x in house.followinfo),index=house.index,columns=['guanzhu','daikan','fabu'])
#将分列后的关注度信息拼接回原数据表
house=pd.merge(house,followinfo_split,right_index=True, left_index=True)
house=house.drop(['houseinfo', 'followinfo'], axis = 1)

###房源绘图
#按房源户型类别进行汇总
huxing=house.groupby('huxing')['huxing'].agg(len)
#房源户型分布绘图
plt.rc('font', family='STXihei', size=15)
huxing.plot(kind='barh',color='#052B6C',alpha=0.8,align='center',edgecolor='white')
plt.grid(color='#95a5a6',linestyle='--', linewidth=1,axis='y',alpha=0.4)
plt.xlabel('数量')
plt.ylabel('户型')
plt.title('房型数量分布')
plt.legend(['数量'], loc='upper right')
plt.show()

###面积绘图
#对房源面积进行二次分列
mianji_num_split = pd.DataFrame((x.split('平') for x in house.mianji),index=house.index,columns=['mianji_num','mi'])
#将分列后的房源面积拼接回原数据表
house = pd.merge(house,mianji_num_split,right_index=True,left_index=True)
#去除mianji_num字段两端的空格
house['mianji_num'] = house['mianji_num'].map(str.strip)
#更改mianji_num字段格式为float
house['mianji_num'] = house['mianji_num'].astype(float)
#查看所有房源面积的范围值
#print(house['mianji_num'].min(),house['mianji_num'].max())

#对房源面积进行分组
bins = [0, 50, 100, 150, 200, 250, 300, 350]
group_mianji = ['0-50', '50-100', '100-150', '150-200','200-250','250-300','300-350']
house['group_mianji'] = pd.cut(house['mianji_num'], bins, labels=group_mianji)
#按房源面积分组对房源数量进行汇总
group_mianji=house.groupby('group_mianji')['group_mianji'].agg(len)

#绘制房源面积分布图
plt.rc('font', family='STXihei', size=15)
group_mianji.plot(kind='barh',color='#052B6C',alpha=0.8,align='center',edgecolor='white')
plt.xlabel('数量')
plt.ylabel('面积范围')
plt.title('房屋面积分布')
plt.legend(['数目'], loc='upper right')
plt.grid(color='#95a5a6',linestyle='--', linewidth=1,axis='y',alpha=0.4)
plt.show()

###关注度绘图
#对房源关注度进行二次分列
guanzhu_num_split = pd.DataFrame((x.split('人') for x in house.guanzhu),index=house.index,columns=['guanzhu_num','ren'])
#将分列后的关注度数据拼接回原数据表
house=pd.merge(house,guanzhu_num_split,right_index=True, left_index=True)
#去除房源关注度字段两端的空格
house['guanzhu_num']=house['guanzhu_num'].map(str.strip)
#更改房源关注度及总价字段的格式
house[['guanzhu_num','totalprice']]=house[['guanzhu_num','totalprice']].astype(float)
#查看房源关注度的区间
#print(house['guanzhu_num'].min(),house['guanzhu_num'].max())

#对房源关注度进行分组，这里的bins也需要根据上边的min()和max()输出值进行设置
bins = [0, 100, 200, 300, 400, 500]
group_guanzhu = ['小于100', '100-200', '200-300', '300-400','400-500']
house['group_guanzhu'] = pd.cut(house['guanzhu_num'], bins, labels=group_guanzhu)
group_guanzhu=house.groupby('group_guanzhu')['group_guanzhu'].agg(len)

plt.rc('font', family='STXihei', size=15)
group_guanzhu.plot(kind='barh',color='#052B6C',alpha=0.8,align='center',edgecolor='white')
plt.ylabel('关注人数范围')
plt.xlabel('房源数量')
plt.title('房屋关注度分布')
plt.legend(['数量'], loc='upper right')
plt.grid(color='#95a5a6',linestyle='--', linewidth=1,axis='y',alpha=0.4)
plt.show()

#房源聚类分析
#导入sklearn中的KMeans进行聚类分析
from sklearn.cluster import KMeans
#使用房源总价，面积和关注度三个字段进行聚类
house_type = np.array(house[['totalprice','mianji_num','guanzhu_num']])
#设置质心数量为3
clf=KMeans(n_clusters=3)
#计算聚类结果
clf=clf.fit(house_type)
#查看分类结果的中心坐标
center=pd.DataFrame(clf.cluster_centers_, columns=['房价','面积','关注人数'])
#在原数据表中标注所属类别
house['label'] = clf.labels_
#显示所有数据内容
#print(house.label)


#if __name__ == '__main__':    
#   main()