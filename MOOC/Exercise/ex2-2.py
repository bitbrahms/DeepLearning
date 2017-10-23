# -*- coding: utf-8 -*-
"""
Created on Mon Oct 16 10:04:02 2017

@author: MannyXu
"""

score = int(input("please input your score: "))

if score >= 90 and score <= 100:
    print("%d : A" % score)
elif score >=70 and score < 90:
    print("%d : B" % score)
elif score >=60 and score < 70:
    print("%d : C" % score)
elif score >=0 and score < 60:

    print("%d : D" % score)
else:
    print("%d : Invalid score" % score)
