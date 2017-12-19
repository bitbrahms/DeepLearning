#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-12-05 09:00:40
# @Author  : mannyxu (beilixumeng@163.com)

import urllib
import http.cookiejar

#保存cookie到cookie.txt文件
def get_cookie(url,formdata,headers):
	#cookie = http.cookiejar.CookieJar()
	cookie = http.cookiejar.LWPCookieJar('cookie.txt')
	handler = urllib.request.HTTPCookieProcessor(cookie)
	opener = urllib.request.build_opener(handler)
	res = urllib.request.Request(url,data=formdata,headers=headers)
	try:
		response = opener.open(res)
	except urllib.error.URLError as e:
		print(e.reason)
	cookie.save(ignore_discard=True,ignore_expires=True)
	#print(cookie)

def load_cookie():
    cookie = http.cookiejar.MozillaCookieJar('cookie.txt')
    cookie.load('cookie.txt', ignore_discard=True, ignore_expires=True)
    handler = urllib.request.HTTPCookieProcessor(cookie)
    opener = urllib.request.build_opener(handler)
    get_request = urllib.request.Request(url)
    get_response = opener.open(get_request)
    print(get_response.read().decode())

def main():
	url = 'https://accounts.douban.com/login'
	formdata = {
    	'redir': 'https://movie.douban.com/mine?status=collect',
    	'form_email': 'beilixumeng@163.com',
    	'form_password': '2010010203'}
	formdata = urllib.parse.urlencode(formdata).encode()
	headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) \
		AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'}
	get_cookie(url,formdata,headers)
	#load_cookie()

if __name__ == '__main__':
	main()