# -*- coding: utf-8 -*-
# @Date    : 2017-11-29 22:41:54
# @Author  : MannyXu (beilixumeng@163.com)

from urllib import request
url = 'http://www.baidu.com'
res = request.urlopen(url)
print(res.read())