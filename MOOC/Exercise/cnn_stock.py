# -*- coding: utf-8 -*-
"""
<<<<<<< HEAD
Created on Sun Nov 12 20:49:09 2017

@author: manny
=======
Created on Sun Nov 12 14:50:17 2017

@author: MannyXu
>>>>>>> 6399ca80ebfb10368e2c3af3ec219a4d1cd2b322
"""

import requests
import re
import pandas as pd
 
def retrieve_dji_list():
    r = requests.get('http://money.cnn.com/data/dow30/')
    search_pattern = re.compile('class="wsod_symbol">(.*?)<\/a>.*?<span.*?">(.*?)<\/span>.*?\n.*?class="wsod_stream">(.*?)<\/span>')
    dji_list_in_text = re.findall(search_pattern, r.text)
    dji_list = []
    for item in dji_list_in_text:
        dji_list.append([item[0], item[1], float(item[2])])
    return dji_list
 
dji_list = retrieve_dji_list()
djidf = pd.DataFrame(dji_list)
<<<<<<< HEAD
cols = ['code', 'name', 'lasttrade']
djidf.columns = cols
=======
>>>>>>> 6399ca80ebfb10368e2c3af3ec219a4d1cd2b322
print(djidf)