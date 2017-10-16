# -*- coding: utf-8 -*-
"""
Created on Mon Oct 16 13:42:23 2017

@author: MannyXu
"""
'''
import math
def prime(num):
    if num < 2:
        return False
    max = int(math.sqrt(num)) + 1
    for j in range(2,max):
        if num % j == 0:
            return False
    return True
        
def monisen(no):
    l2=[3]
    a=3
    while 1:
        if prime(a) == False:
            a = a+2
            continue
        x=2**a - 1 
        if prime(x) == False:
            a = a+2
            continue
        else:
            l2.append(x)
            a =a +2
        if len(l2) == no:
            break
    return l2[-1]
import time

start = time.clock()
print(monisen( int(input()) ))
end = time.clock()
print("time: %f s" % (end - start))
'''

import math
def prime(num):
    if num < 2:
        return False
    max = int(math.sqrt(num)) + 1
    for j in range(2,max):
        if num % j == 0:
            return False
    return True
        
def monisen(no):
    l2=[3]
    for i in range(3,1000,2):
        if prime(i):
            x = 2**i - 1
            if prime(x):
                l2.append(x)
        if len(l2) == no:            
            break
    return l2[-1]
print(monisen( int(input()) ))