# -*- coding: utf-8 -*-
"""
Created on Mon Oct 16 10:53:32 2017

@author: MannyXu
"""
import math

def isPrime(i):
    if i == 2 or i == 3:
        return True
    else:
        max = int(math.sqrt(i)) + 1
        for j in range(2, max):
            if i % j == 0:
                return False
                break
            elif j < max - 1 :
                continue
            return True

num = 0
for i in range(4,2002,2):
    for j in range(2,i-1):
        if isPrime(j) and isPrime(i-j):
            num = num + 1
            if num % 6 :
                print("%4d=%4d  +  %4d" % (i, j, i-j),end='  ')
            else:
                print("%4d=%4d  +  %4d" % (i, j, i-j))
            break
        elif j >= i-1:
            print("Bad Job")
            break
        else:
            continue
