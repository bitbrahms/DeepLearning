#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-12-11 14:05:44
# @Author  : mannyxu (beilixumeng@163.com)

import pandas as pd

data = pd.read_csv('spider/iris.csv',names=[0,1,2,3,'message'],index_col='message')
print(data)
