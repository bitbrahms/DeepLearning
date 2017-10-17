# -*- coding: utf-8 -*-
"""
Created on Tue Oct 17 17:16:54 2017

@author: MannyXu
"""



def countchar(str):
    list_num = [0]*26
    str_ = str.lower()
    lens = int(len(str_))
    for i in range(lens):
        x = ord(str_[i])
        if x>=97 and x<=122:
            list_num[x-97] += 1
    return list_num
if __name__ == "__main__":
     str = input()
     print(countchar(str))