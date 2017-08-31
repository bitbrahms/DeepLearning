# -*- coding: utf-8 -*-
'''
Created on Aug 22, 2017
@author: manny
'''
import numpy as np
import math

def loadSimpData():
    dataMat = np.mat([[1. , 2.1],
                    [2. , 1.1],
                    [1.3 , 1.],
                    [1. , 1.],
                    [2. , 1.]])
    classLabel = [1.0, 1.0, -1.0, -1.0, 1.0]
    return dataMat, classLabel


#阈值比较分类
def stumpClassify(dataMat, dimen, thread, threadIneq):
    retArray = np.ones((np.shape(dataMat)[0], 1))
    if threadIneq == 'lt':
        retArray[np.array(dataMat[:, dimen]) <= thread] = -1.0
    else:
        retArray[np.array(dataMat[:, dimen] > thread)] = -1.0
    return retArray
    
#最佳单层决策树
def bulidStump(dataMat, classLabel, D):
    dataMat = np.mat(dataMat)
    classLabel = np.mat(classLabel).transpose()
    row, col = np.shape(dataMat)
    numSteps = 10.0
    bestStump = {}
    bestClassEst = np.mat(np.zeros((row, 1)))
    minError = math.inf
    for i in range(col):
        rangeMin = dataMat[:, i].min()
        rangeMax = dataMat[:, i].max()
        stepSize = (rangeMax - rangeMin)/numSteps
        for j in range(-1,int(numSteps)+1):
            for inequal in ['lt','gt']:
                thread = rangeMin + stepSize * float(j)
                predVal = stumpClassify(dataMat,i,thread,inequal)
                errArr = np.mat(np.ones((row,1)))
                errArr[predVal == classLabel] = 0
                weightedError = (D.transpose() * errArr)[0,0]
                #print("split: dim:%d thread:%.2f threadIneq:%s weightedError:%.3f" \
                #% (i,thread,inequal,weightedError))
                if (weightedError < minError):
                    minError = weightedError
                    bestClassEst = predVal.copy()
                    bestStump['dim'] = i
                    bestStump['thread'] = thread
                    bestStump['ineq'] = inequal
    return bestStump,minError,bestClassEst

#AdaBoost算法
def adaBoostTrain(dataMat,classLabel,numIt=40):
    #weakClassArr 存储弱分类函数
    weakClassArr = []
    row = np.shape(dataMat)[0]
    D = np.mat(np.ones((row,1))/row)
    aggClassEst = np.mat(np.zeros((row,1)))
    for i in range(numIt):
        bestStump, error, classEst = bulidStump(dataMat,classLabel,D)
        #print("D:",D.transpose())
        #计算本次分类器的系数，其中max()语句为了保证没有除零溢出
        alpha = float(0.5*math.log((1.0-error)/max(error,1e-16)))
        bestStump['alpha'] = alpha
        weakClassArr.append(bestStump)
        #print("classEst: ",classEst.transpose())
        #计算D*exp(-alpha*yi*Gm)
        expon = np.mat(np.multiply(-1*alpha*np.mat(classLabel).transpose(),classEst))
        a = [math.exp(i) for i in expon]
        #D = np.multiply(D,a)
        D = np.array([D[i]*a[i] for i in range(row)])
        #print(D)
        #计算下一次迭代的D系数
        D = D/D.sum()
        #求此时的集成函数
        aggClassEst += alpha * np.mat(classEst)
        #print("aggClassEst :",aggClassEst.transpose())
        #如果集成函数符号和classlabel一致，则分类正确，错误率为零，!=用于判断分类错误的数目
        aggErrors = np.multiply(np.sign(aggClassEst) != np.mat(classLabel).transpose(), np.ones((row,1)))
        errorRate = aggErrors.sum()/row
        print("total error: ",errorRate,"\n")
        if errorRate == 0.0:
            break
    return weakClassArr
                
#AdaBoost分类器
def adaClassify(dataMat,weakClassArr):
    dataMat = np.mat(dataMat)
    row,col = np.shape(dataMat)
    aggClassEst = np.mat(np.zeros((row,1)))
    for i in range(len(weakClassArr)):
        classEst = stumpClassify(dataMat,weakClassArr[i]['dim'],\
                    weakClassArr[i]['thread'],\
                    weakClassArr[i]['ineq'])
        aggClassEst += weakClassArr[i]['alpha'] * classEst
        print(aggClassEst)
    return np.sign(aggClassEst)
    
#
def loadDataSet(fileName):
    numFeats = len(open(fileName).readlines()[0].split('\t'))
    dataMat = []
    classLabel = []
    fr = open(fileName)
    for line in fr.readlines():
        lineArr = []
        curLine = line.strip().split('\t')
        for i in range(numFeats -1):
            lineArr.append(float(curLine[i]))
        dataMat.append(lineArr)
        classLabel.append(float(curLine[-1]))
    return dataMat,classLabel
 
        