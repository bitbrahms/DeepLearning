# -*- coding: utf-8 -*-
"""
<<<<<<< HEAD
Created on Wed Oct 25 07:50:15 2017

@author: manny
"""

# -*- coding: utf-8 -*-
"""
Get quotesdf
 
@author: Dazhuang
"""
 
=======
Created on Sun Nov 12 14:50:40 2017

@author: MannyXu
"""

>>>>>>> 6399ca80ebfb10368e2c3af3ec219a4d1cd2b322
import requests
import re
import json
import pandas as pd
<<<<<<< HEAD
from datetime import date
import time

=======
 
>>>>>>> 6399ca80ebfb10368e2c3af3ec219a4d1cd2b322
def retrieve_quotes_historical(stock_code):
    quotes = []
    url = 'https://finance.yahoo.com/quote/%s/history?p=%s' % (stock_code, stock_code)
    r = requests.get(url)
    m = re.findall('"HistoricalPriceStore":{"prices":(.*?),"isPending"', r.text)
    if m:
        quotes = json.loads(m[0])
        quotes = quotes[::-1]
    return  [item for item in quotes if not 'type' in item]
 
<<<<<<< HEAD
quotes = retrieve_quotes_historical('KO')
list1 = []
for i in range(len(quotes)):
    x = date.fromtimestamp(quotes[i]['date'])
    y = date.strftime(x,'%Y-%m-%d')
    list1.append(y)
quotesdf_ori = pd.DataFrame(quotes, index = list1)
quotesdf = quotesdf_ori.drop(['date'], axis = 1)
#print(quotesdf)


listtemp = []
for i in range(len(quotesdf)):
    temp = time.strptime(quotesdf.index[i], '%Y-%m-%d')
    listtemp.append(temp.tm_mon)
tempdf = quotesdf.copy()
tempdf['month'] = listtemp
quotesKOdf = tempdf
print(quotesKOdf)
=======
quotes = retrieve_quotes_historical('AXP')
quotesdf = pd.DataFrame(quotes)
# quotesdf = quotesdf_ori.drop(['unadjclose'], axis = 1)  原先的网站数据有unadjclose列，目前已删除
print(quotesdf)
>>>>>>> 6399ca80ebfb10368e2c3af3ec219a4d1cd2b322
