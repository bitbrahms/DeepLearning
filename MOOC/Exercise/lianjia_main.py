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

df1=pd.read_csv('data_sh_1.csv')
df2=pd.read_csv('data_sh_2.csv')
df3=pd.read_csv('data_sh_3.csv')
df4=pd.concat([df1,df2,df3],axis=1)
print(df4.head(10))
df=df4.drop(['Unnamed: 0'], axis=1)
df=df.dropna(['areas'],axis=0)
print(df.head(10))
df.to_csv('test1.csv',encoding='utf-8-sig')