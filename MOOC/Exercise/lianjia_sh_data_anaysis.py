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
from sklearn.cluster import KMeans

######数据分析################################
#############################################
df=pd.read_csv('data_sh.csv')


#按房源户型类别进行汇总
huxing=df.groupby('房屋户型')['房屋户型'].agg(len)
#房源户型分布绘图
plt.rc('font', family='STXihei', size=15)
huxing.plot(kind='barh', color='#052B6C', alpha=0.8,
            align='center', edgecolor='white')
plt.grid(color='#95a5a6', linestyle='--', linewidth=1, axis='y', alpha=0.4)
plt.xlabel('数量')
plt.ylabel('户型')
plt.title('房型数量分布')
plt.legend(['数量'], loc='upper right')
plt.show()

#对房源面积进行二次分列
mianji_num_split = pd.DataFrame((x.split('平') for x in df.areas),index=df.index,columns=['area','平方米'])
#将分列后的房源面积拼接回原数据表
df = pd.merge(df,mianji_num_split,right_index=True,left_index=True)
df['area'] = df['area'].map(str.strip)
# 更改mianji_num字段格式为float
df['area'] = df['area'].astype(float)
# 查看所有房源面积的范围值
# print(house['mianji_num'].min(),house['mianji_num'].max())
# 对房源面积进行分组
bins = [0, 50, 100, 150, 200, 250, 300, 350]
group_mianji = ['0-50', '50-100', '100-150',
                '150-200', '200-250', '250-300', '300-350']
df['group_mianji'] = pd.cut(df['area'], bins, labels=group_mianji)

# 按房源面积分组对房源数量进行汇总
group_mianji = df.groupby('group_mianji')['group_mianji'].agg(len)

#绘制房源面积分布图

plt.rc('font', family='STXihei', size=15)
group_mianji.plot(kind='barh', color='#052B6C', alpha=0.8,
                  align='center', edgecolor='white')
plt.xlabel('数量')
plt.ylabel('面积范围')
plt.title('房屋面积分布')
plt.legend(['数目'], loc='upper right')
plt.grid(color='#95a5a6', linestyle='--', linewidth=1, axis='y', alpha=0.4)
plt.show()


#按行政区进行划分
quyu=df.groupby('行政区')['行政区'].agg(len)
quyu.plot(kind='pie',autopct='%2.0f%%',labeldistance=1.1)
plt.show()


# 房源聚类分析
# 使用房源总价，面积和关注度三个字段进行聚类
house_type = np.array(df[['price', 'area']])
# 设置质心数量为3
clf = KMeans(n_clusters=3)
# 计算聚类结果
clf = clf.fit(house_type)
# 查看分类结果的中心坐标
center = pd.DataFrame(clf.cluster_centers_, columns=['房价', '面积'])
# 在原数据表中标注所属类别
df['label'] = clf.labels_
print(df.label)