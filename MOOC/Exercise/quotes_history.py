# -*- coding: utf-8 -*-
"""
Created on Wed Oct 25 07:50:15 2017

@author: manny
"""

# -*- coding: utf-8 -*-
"""
Get quotesdf
 
@author: Dazhuang
"""
 
import requests
import re
import json
import pandas as pd
 
def retrieve_quotes_historical(stock_code):
    quotes = []
    url = 'https://finance.yahoo.com/quote/%s/history?p=%s' % (stock_code, stock_code)
    r = requests.get(url)
    m = re.findall('"HistoricalPriceStore":{"prices":(.*?),"isPending"', r.text)
    if m:
        quotes = json.loads(m[0])
        quotes = quotes[::-1]
    return  [item for item in quotes if not 'type' in item]
 
quotes = retrieve_quotes_historical('AXP')
quotesdf = pd.DataFrame(quotes)
# quotesdf = quotesdf_ori.drop(['unadjclose'], axis = 1)  原先的网站数据有unadjclose列，目前已删除
print(quotesdf)