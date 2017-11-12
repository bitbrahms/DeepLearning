# -*- coding: utf-8 -*-
"""
Created on Tue Oct 17 16:04:42 2017

@author: MannyXu
"""

import os
import requests
import BeautifulSoup from bs4
import urllib


quesNum = input("Please Input Question Num: ")
url = 'https://www.zhihu.com/question/'+str(quesNum)
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}

r = requests.get(url, headers=headers)
soup = BeautifulSoup(r.text, 'lxml')
title = soup.select('.QuestionHeader-title')
img = soupselect('')