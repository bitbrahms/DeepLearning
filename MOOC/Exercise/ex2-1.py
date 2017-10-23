# -*- coding: utf-8 -*-
"""
Created on Fri Oct 13 19:19:32 2017

@author: MannyXu
"""

def tempChg(F):
    C = 5/9 * (F-32)
    return C
for i in range(0,320,20):
    print('%d:%d' % (i,tempChg(i)))
