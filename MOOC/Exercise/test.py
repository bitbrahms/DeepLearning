# -*- coding: utf-8 -*-
"""
Created on Tue Oct 17 17:16:54 2017

@author: MannyXu
"""
#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
from bs4 import BeautifulSoup

html_doc = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title"><b>The Dormouse's story</b></p>

<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>

<p class="story">...</p>

"""

soup = BeautifulSoup(html_doc,'html.parser')
lacie = soup.find_all(attrs={'class': 'sister'})

for i in lacie:
	print(i)
	print(i.get_text())
	'''
import numpy as np
import matplotlib.pyplot as plt
 
labels =  [u'第一部分',u'第二部分',u'第三部分','D']
fracs = [15, 30.55, 44.44, 10]
explode = [0, 0.1, 0, 0] # 0.1 凸出这部分，
plt.axes(aspect=1)  # set this , Figure is round, otherwise it is an ellipse
#autopct ，show percet
plt.pie(x=fracs, labels=labels,autopct='%3.1f %%',)
plt.title('各区房子分布') 
'''
labeldistance，文本的位置离远点有多远，1.1指1.1倍半径的位置
autopct，圆里面的文本格式，%3.1f%%表示小数有三位，整数有一位的浮点数
shadow，饼是否有阴影
startangle，起始角度，0，表示从0开始逆时针转，为第一块。一般选择从90度开始比较好看
pctdistance，百分比的text离圆心的距离
patches, l_texts, p_texts，为了得到饼图的返回值，p_texts饼图内部文本的，l_texts饼图外label的文本
'''
 
plt.show()