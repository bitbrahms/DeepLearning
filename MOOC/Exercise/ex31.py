# -*- coding: utf-8 -*-
"""
Created on Tue Oct 17 14:45:00 2017

@author: MannyXu
"""

import requests
import re
from bs4 import BeautifulSoup

i, sum = 0, 0
count_c, count_s = 0, 0
while(count_s < 50 ):
    r = requests.get('https://book.douban.com/subject/3259440/comments/hot?p'+str(i+1))
    soup = BeautifulSoup(r.text, 'lxml')
    partten_c = soup.find_all(class_="comment-content")
    for item in partten_c:
        count_c += 1
        print(count_c, item.string)
        if count_c ==50:
            break

    partten_s = '<span class="user-stars allstar(.*?) rating"'
    s = re.findall(partten_s, r.text)
    for item in s:
        sum += int(item)
        count_s += 1
    i += 1
print('average_star:',sum/count_s)
from bs4 import BeautifulSoup
soup = BeautifulSoup(r.text, 'lxml')
