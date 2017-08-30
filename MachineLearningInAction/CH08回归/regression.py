# -*- coding: utf-8 -*-
'''
Created on Aug 22, 2017
@author: manny
'''
import numpy as np
import math

#加载数据
def loadDataSet(filename):
    numFeat = len(open(filename).readlines()[0].split('\t')) - 1
    dataMat = []
    labelMat = []
    fr = open(filename)
    for line in fr.readlines():
        lineArr = []
        curLine = line.strip().split('\t')
        for i in range(numFeat):
            lineArr.append(float(curLine[i]))
        dataMat.append(lineArr)
        labelMat.append(float(curLine[-1]))
    return dataMat,labelMat

#计算w
def standRegres(xArr,yArr):
    xMat = np.mat(xArr)
    yMat = np.mat(yArr).transpose()
    xTx = xMat.transpose() * xMat
    print(xTx)
    if np.linalg.det(xTx) == 0.0:
        print("The matrix is singular")
        return
    w = xTx.I * (xMat.transpose() * yMat)
    return w
