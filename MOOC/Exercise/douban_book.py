#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-11-28 14:20:30
# @Author  : manny (beilixumeng@163.com)

import requests
import urllib
import re
import random
import time
from bs4 import BeautifulSoup
import os

if not os.path.exists('D:/CPU_Manny/workspace/DeepLearning/MOOC/Exercise/images'):
	os.mkdir('D:/CPU_Manny/workspace/DeepLearning/MOOC/Exercise/images')

def main():    
	url = 'http://huaban.com/favorite/beauty/'
	#url='https://www.zhihu.com/question/21844569'
	headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1) \
		AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'}
	html = urllib.request.Request(url,headers=headers)
	html = urllib.request.urlopen(html)
	print(html.read())
	

if __name__=='__main__':    
	main()