# -*- coding: utf-8 -*-
"""
Created on Mon Oct 16 10:30:25 2017

@author: MannyXu
"""

def Mod37(i):
    if i % 37:
        return False
    else:
        return True

def nums(i):
    sevs = i % 10
    tens = (i // 10) % 10
    huds = i // 100
    num1 = tens * 100 + sevs * 10 + huds
    num2 = sevs * 100 + huds * 10 +tens
    return num1, num2

for i in range(100,1001):
    if Mod37(i):
        num1, num2 = nums(i)
        if Mod37(num1) and Mod37(num2):
            continue
        else:
            print("Bad Job")
            break
    elif i <1000:
        continue
    print("Good Job")
