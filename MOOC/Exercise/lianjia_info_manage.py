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


#对房源信息进行分列
houseinfo_split = pd.DataFrame((x.split('|') for x in house.houseinfo),index=house.index,columns=['xiaoqu','huxing','mianji','chaoxiang','zhuangxiu','dianti'])
#将分列结果拼接回原数据表
house=pd.merge(house,houseinfo_split,right_index=True, left_index=True)
#对房源关注度进行分列
followinfo_split = pd.DataFrame((x.split('/') for x in house.followinfo),index=house.index,columns=['guanzhu','daikan','fabu'])
#将分列后的关注度信息拼接回原数据表
house=pd.merge(house,followinfo_split,right_index=True, left_index=True)
#删除混乱信息
house=house.drop(['houseinfo', 'followinfo'], axis = 1)

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
'''
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
'''