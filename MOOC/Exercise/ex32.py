# -*- coding: utf-8 -*-
"""
Created on Tue Oct 17 16:04:42 2017

@author: MannyXu
"""

import requests
import re
from bs4 import BeautifulSoup

r = requests.get('http://money.cnn.com/data/dow30/')
soup = BeautifulSoup(r.text, 'lxml')
#comp = soup.find_all(class_="wsod_symbol")
#price_partten = re.compile('<td class="wsod_aRight"><span stream="last.*class="wsod_stream">(.*)</span')
#price = re.findall(price_partten, r.text)
#code_partten = re.compile('<td class="wsod_aRight">(\d.*)</td>')
#code = re.findall(code_partten, r.text)
#lens = int(len(comp))
#print("%-6s%-10s%-10s" % ("comp", "price", "code"))
#for i in range(lens):
#   print('%-6s%-10s%-10s' % (comp[i].string, price[i], code[i]))
   
   
partten = re.compile('class="wsod_symbol">(.*)<\/a>.*title="(.*)".*\n.*class="wsod_stream">(.*)<\/span')
dow_list = re.findall(partten, r.text)
print(dow_list)
