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
'''
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
'''


#模拟登陆知乎

session = requests.Session()
headers ={'User-Agent':'Mozilla/5.0 (Windows NT 6.1) leWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'}

'''
def get_cookie():
    session.cookies = http.cookiejar.LWPCookieJar("cookie")
    print（session.cookies)
    try:
        session.cookies.load(ignore_discard=True)
    except IOError:
        print('Cookie未加载！')
'''
def get_xsrf(url):
    res = session.get(url,headers=headers)
    xsrf = re.findall('<input type="hidden" name="_xsrf" value="(.*?)"/',res.text)[0]
    return xsrf

def get_captcha():
    #验证码时间戳转换
    t = str(int(time.time()*1000))
    captcha_url = 'http://www.zhihu.com/captcha.gif?r=' + t + "&type=login"
    response = session.get(captcha_url, headers=headers)
    urllib.requests.retrieve('captcha_url','captcha.jpg')
    im = Image.open('cptcha.gif')
    im.show()
    captcha=input('Please input your captcha here: ')
    return captcha

def log_in(username,passward):
    formData={}
    if re.match('\d{11}$',str(username)):
        url = 'http://www.zhihu.com/login/phone_num'
        formData['phone_num']=username
    else:
        url = 'http://www.zhihu.com/login/email'
        formData['email']=username
    xsrf = get_xsrf(url)
    formData = {'_xsrf':xsrf,'password':passward}
    # 若不用验证码，直接登录
    login_page = session.post(url, data=formData, headers=headers)
    print(login_page)
    # 打印返回的响应，r = 1代表响应失败，msg里是失败的原因
    # loads可以反序列化内置数据类型，而load可以从文件读取
    '''
    login_code = login_page.json()
    print(login_code)
    
    if login_code["r"] == 1:
        # 要用验证码，post后登录
        formData['captcha'] = get_captcha()
        login_page = session.post(url, data=formData, headers=headers)
    #   login_code = login_page.json()
    #    print((login_code['msg'])
    # 保存cookie到本地
    #session.cookies.save()
    '''
def isLogin():
    # 通过查看用户个人信息来判断是否已经登录
    url = "https://www.zhihu.com/settings/profile"
    # 禁止重定向，否则登录失败重定向到首页也是响应200
    login_code = session.get(url, headers=headers, allow_redirects=False).status_code
    if login_code == 200:
        return True
    else:
        return False



if __name__ == '__main__':
    if isLogin():
        print('您已经登录')
    else:
        username = input('输入账号：')
        passward = input('输入密码：')
        log_in(username,passward)


