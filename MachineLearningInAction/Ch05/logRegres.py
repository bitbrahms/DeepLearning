# -*- coding: utf-8 -*-
'''
Created on Aug 22, 2017
@author: manny
'''

import numpy as np
import math
import matplotlib.pyplot as plt

#加载数据，生成data矩阵和label矩阵
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
        
#sigmoid函数
def sigmoid(x):
    return 1.0/(1 + math.exp(-x))

#梯度上升优化算法：一次处理完所有样本
'''
回归系数初始化为1
重复R次：
    计算整个数据集梯度
    使用alpha x gradient更新回归系数
返回回归系数值
'''

def gradAscent(dataMatIn, labelMatIn):
    dataMatrix = np.mat(dataMatIn)
    labelMatrix = np.mat(labelMatIn).transpose()#transpose 转置
    row,col = np.shape(dataMatrix)
    #移动步长
    alpha = 0.01
    #迭代500次
    maxCycles = 500
    #初始权重设为1
    weights = np.ones((col,1))
    #h=A*b
    for k in range(maxCycles):
        h = np.mat([sigmoid(i) for i in dataMatrix * weights]).transpose()
        error = labelMatrix - h
        #算法推导
        weights = weights + alpha * dataMatrix.transpose() * error
    return weights
    
#画图
def plotBestFig(weightIn): 
    weights = weightIn
    #weights = weightIn.getA()#matrix.getA() 将matrix类型转换成array类型，array.asmatrix 则反过来
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
    fig = plt.figure()#创建画布
    ax = fig.add_subplot(111)#1x1图像的第一幅
    #scatter 散点图
    #s，size,散点大小，#market，散点形状，默认为圈，s是正方形
    #alpha 散点亮度，label标签
    ax.scatter(xcord1, ycord1, s=30, c='red',marker='s',alpha=1,label='P1')
    ax.scatter(xcord2, ycord2, s=30, c='green',alpha=1,label='P0')
    #arange(start,stop,step)
    x = np.arange(-3.0, 3.0, 0.1)
    #对于sigmoid函数，输入0是类别1和类别0的分界线，因此设定0=weights*x，又weights[0]
    #人为设置为1了
    y = (-weights[0]-weights[1]*x)/weights[2]
    ax.plot(x,y)
    plt.xlabel('X1')
    plt.ylabel('X2')
    plt.title('basic scatter plot')
    plt.legend(loc='upper right')#label 位置，没有这行则图中不会出现label
    plt.show()

#随机梯度上升算法：一次仅用一个样本点来更新回归系数，这是一个在线学习算法
'''
所有回归系数初始为1
对数据集中的每个样本
    计算该样本梯度
    使用alpha x gradient更新回归系数
返回回归系数值
'''

def randGradAscent0(dataMatrix,labelMatrix):
    row,col = np.shape(dataMatrix)
    alpha = 0.01
    weights = np.ones(col)
    for i in range(row):
        h = sigmoid(sum(dataMatrix[i]*weights))
        error = labelMatrix[i] - h
        weights = weights + [alpha * error * k for k in dataMatrix[i]]
    return weights

#改进版随机梯度上升算法
def randGradAscent(dataMatrix,labelMatrix,numIter=150):
#    dataMatrix,labelMatrix = loadDataSet()
    dataMatrix  = np.array(dataMatrix)
    labelMatrix = np.array(labelMatrix)
    row,col = np.shape(dataMatrix)
    weights = np.ones(col)
    for j in range(numIter):
        dataIndex = list(range(row))
        for i in range(row):
            alpha = 0.0001 #为何alpha不可调整？？？？？
            randIndex = int(np.random.uniform(0,len(dataIndex)))
            h = sigmoid(np.dot(dataMatrix[randIndex], weights))
            error = labelMatrix[randIndex] - h
#            weights = weights + [alpha * error * k for k in dataMatrix[randIndex]]
            weights = weights + alpha * error * dataMatrix[randIndex]
            del(dataIndex[randIndex])
    return weights
   
#回归分类函数
def classfyVector(inX,trainingweights):
    inX = np.array(inX)
    weights = np.array(trainingweights)
    prob = sigmoid(float(np.dot(inX, weights)))
    if prob > 0.5:
        return 1.0
    else:
        return 0.0

#
def colicTest():
    frTrain = open('horseColicTraining.txt')
    frTest =  open('horseColicTest.txt')
    trainingSet = []
    trainingLabel = []
    for line in frTrain.readlines():
        currentLine = line.strip().split('\t')
        lineArr = []
        for i in range(21):
            lineArr.append(float(currentLine[i]))
        trainingSet.append(lineArr)
        trainingLabel.append(float(currentLine[21]))
    trainWeights = randGradAscent(trainingSet,trainingLabel,500)
    
    errorCount = 0
    numTestVec = 0.0
    for line in frTest.readlines():
        numTestVec += 1.0
        currentLine = line.strip().split('\t')
        col = np.shape(currentLine)[0]
        lineArr = []
        for i in range(21):
            lineArr.append(float(currentLine[i]))
        testLabel = int(float(currentLine[21]))
        trainingLabel = int(classfyVector(lineArr,trainWeights))
        if trainingLabel != testLabel:
            errorCount += 1
    errorRate = (float(errorCount)/numTestVec)
    print('the errorRate is : %f' % errorRate)
    return errorRate
    
#
def multiTest():
    numTests = 10
    errorSum = 0.0
    for i in range(numTests):
        errorSum += colicTest()
    print('%d iterations thr avg is: %s' % (numTests,errorSum/float(numTests)))
