# -*- coding: utf-8 -*-
"""
Created on Fri Dec  1 09:40:56 2017

@author: MannyXu
"""

from urllib import request,parse,
from http import cookiejar

if __name__ == 'main':
    #设置保存cookie的文件，同级目录下的cookie.txt
    filename = 'cookie.txt'
    #声明一个MozillaCookieJar对象实例来保存cookie，之后写入文件
    cookie = cookiejar.MozillaCookieJar(filename)
    #利用urllib.request库的HTTPCookieProcessor对象来创建cookie处理器,也就CookieHandler
    handler=request.HTTPCookieProcessor(cookie)
    #通过CookieHandler创建opener
    opener = request.build_opener(handler)
    #此处的open方法打开网页
    url = 'https://accounts.douban.com/login'
    formdata = {
    'redir': 'https://movie.douban.com/mine?status=collect',
    'form_email': 'beilixumeng@163.com',
    'form_password': '2010010203',
    'user_login': '登录'}
    formdata = urllib.parse.urlencode(formdata).encode()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) \
    AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'}
    
    req = request.Request(url,data=formdata,headers=headers)
    print(req)
    res = opener.open(req)
    page = res.read().decode()
    #保存cookie到文件
    cookie.save(ignore_discard=True, ignore_expires=True)
    print(cookie)
    for i in cookie:
        print(i.name)
        print(i.value)
