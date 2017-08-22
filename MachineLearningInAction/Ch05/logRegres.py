'''
Created on Aug 22, 2017
@author: manny
'''
# -*- coding: utf-8 -*-

import numpy as np
import math

def loadDataSet():
    dataMatrix = []
    labelMatrix = []
    fr = open('testSet.txt')
    for line in fr.readlines():
        lineArr = line.strip().split()
        #strip() 方法用于移除字符串头尾指定的字符（默认为空格）
        #split()默认为所有的空字符，包括空格、换行(\n)、制表符(\t)等
        dataMatrix.append([1.0, float(lineArr[0]), float(lineArr[1])])
        labelMatrix.append(int(lineArr[2]))
    return dataMatrix,labelMatrix
        
#sigmoid
def sigmoid(x):
    return 1.0/(1 + math.exp(-x))

#
def gradAscent(dataMatIn, labelMatIn):
    dataMatrix = np.mat(dataMatIn)
    labelMatrix = np.mat(labelMatIn).transpose()#transpose 转置
    row,col = np.shape(dataMatrix)
    alpha = 0.01
    maxCycles = 500
    weights = np.ones((col,1))
    for k in range(maxCycles):
        h = np.mat([sigmoid(i) for i in dataMatrix * weights]).transpose()
        error = labelMatrix - h
        weights = weights + alpha * dataMatrix.transpose() * error
    return weights
    
#画出函数
def plotBestFig(weightIn):
    import matplotlib.pyplot as plt
    weights = weightIn.getA()#matrix.getA() 将matrix类型转换成array类型，array.asmatrix 则反过来
    dataMatrix,labelMatrix = loadDataSet()
    dataArr = np.array(dataMatrix)
    row = np.shape(dataArr)[0]
    xcord1 = []
    ycord1 = []
    xcord2 = []
    ycord2 = []
    for i in range(row):
        if int(labelMatrix[i]) == 1:
            xcord1.append(dataArr[i,1])
            ycord1.append(dataArr[i,2])
        else:
            xcord2.append(dataArr[i,1])
            ycord2.append(dataArr[i,2])
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(xcord1, ycord1, s=30, c='red')
    ax.scatter(xcord2, ycord2, s=30, c='green')
    x = np.arange(-3.0, 3.0, 0.1)
    y = (-weights[0]-weights[1]*x)/weights[2]
    ax.plot(x,y)
    plt.xlabel('X1')
    plt.ylabel('X2')
    plt.show()