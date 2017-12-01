#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-12-01 19:03:15
# @Author  : manny (beilixumeng@163.com)

# -*- coding: utf-8 -*-
"""
Created on Fri Dec  1 09:40:56 2017

@author: MannyXu
"""
	
from urllib import request
import os		
import re		
import requests		
from bs4 import BeautifulSoup	
import http.cookiejar
import json
from PIL import Image
			

#下载并显示进度
'''
if not os.path.exists('D:/CPU_Manny/workspace/DeepLearning/MOOC/Exercise/images/'):		
    os.mkdir('D:/CPU_Manny/workspace/DeepLearning/MOOC/Exercise/images/')		
res = requests.get('https://site.douban.com/106875/',headers=headers)		
data = re.findall('class="pic"><img src="(.*?)"',res.text)		
local = 'D:/CPU_Manny/workspace/DeepLearning/MOOC/Exercise/images/'		
x = 0		
for i in data:		
    urllib.request.urlretrieve(i,local+str(x)+'.jpg',cbk)		
     x = x+1		
		
 		
		
 def cbk(a,b,c):		
    percent = 100*a*b/c		
    if percent > 100:		
          percent = 100		
     print("%.2f%%" % percent)		
'''		
		
#豆瓣模拟登陆

url = 'https://accounts.douban.com/login'		
formdata = {
	'redir':'https://movie.douban.com/mine?status=collect',
    'form_email':'beilixumeng@163.com',		
    'form_password':'2010010203',		
    'user_login':'登录'}		
headers ={
	'User-Agent':'Mozilla/5.0 (Windows NT 6.1) \
	AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'}		
res = requests.post(url,data=formdata,headers=headers)

def movie_request(page):
    soup = BeautifulSoup(page,'lxml')
    result = soup.find_all('li',class_='title')
    for item in result:
        print(item.find('a').get_text())
if res.url !='https://movie.douban.com/mine?status=collect':
    print('需要验证码')
    soup = BeautifulSoup(res.text,'lxml')		
    data=soup.find_all('img',id='captcha_image')[0]['src']	
    captchaID = re.findall('<input type="hidden" name="captcha-id" value="(.*?)"/',res.text)
    request.urlretrieve(data,'captcha.jpg')
    im = Image.open('captcha.jpg')
    im.show()
    
    formdata['captcha-solution'] = input('please input captcha-solution here: ')  
    formdata['captcha-id'] = captchaID

    r=requests.post(url,data=formdata,headers=headers)
    page = r.text

    if r.url != 'https://movie.douban.com/mine?status=collect':
        print('failed')
    else:
         movie_request(page)
else:
     movie_request(res.text)