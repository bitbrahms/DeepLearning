# -*- coding: utf-8 -*-
"""
Created on Tue Oct 17 16:04:42 2017

@author: MannyXu
"""

import requests
from bs4 import BeautifulSoup
import time
import os 
import urllib

url = 'https://movie.douban.com/chart'
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}

data = requests.get(url, headers=headers)
soup = BeautifulSoup(data.text, 'lxml')
imgs = soup.select(' div > div > table > tr > td > a > img')

imgs_local = []

folder_img = './img'

if os.path.exists(folder_img) ==False:
    os.mkdirs(folder_img)
    
for img in imgs:
    imgs_local.append(img.get('src'))
    
    
for index, img in enumerate(imgs_local):
    urllib.urlretrieve(img, folder_img)
    time.sleep(4)
