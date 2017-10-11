# -*- coding: utf-8 -*-
'''
Created on Aug 22, 2017
@author: manny
'''
import numpy as np
import math
import matplotlib.pyplot as plt

#绘图
def pltFigure(xArr,yArr,k=1.0):
    yHat = lwlrTest(xArr,xArr,yArr,k)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    #对xArr排序
    xMat = np.mat(xArr)
    srt = xMat[:,1].argsort(0)
    xSort = xMat[srt][:,0,:]
    ax.plot(xSort[:,1], yHat[srt])
    ax.scatter(xMat[:,1].flatten().A[0], np.mat(yArr).transpose().flatten().A[0], s=2, c='red')
    plt.show()

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
    #linalg.det() 求行列式
    if(np.linalg.det(xTx) == 0.0):
        print("The matrix is singular")
        return
    #.I 求逆
    w = xTx.I * (xMat.transpose() * yMat)
    return w


#局部权重线性回归
def lwlr(testPoint, xArr, yArr, k=1.0):
    xArr = np.mat(xArr)
    yArr = np.mat(yArr).transpose()
    row,col = np.shape(xArr)
    weights = np.mat(np.eye((row)))
    for i in range(row):
        diffMat = testPoint - xArr[i,:]
        weights[i,i] = math.exp(diffMat*diffMat.transpose() / (-2.0*k**2))
    xTx = xArr.transpose() * weights * xArr
    if(np.linalg.det(xTx) == 0.0):
        print("the matrix is singular")
        return
    w = xTx.I * xArr.transpose() * weights * yArr
    return testPoint * w

#测试程序
def lwlrTest(testArr, xArr, yArr, k=1.0):
    row = np.shape(testArr)[0]
    yHat = np.zeros(row)
    for i in range(row):
        yHat[i] = lwlr(testArr[i], xArr, yArr, k)
    return yHat

#岭回归
def ridgeRegres(xArr,yArr,lam=0.2):
    xTx = np.mat(xArr).transpose() * np.mat(xArr)
    row,col=np.shape(xArr)
    demon = xTx + np.eye(col) *lam
    if np.linalg.det(demon) == 0.0:
        print("singular")
        return 
    w = demon.I * np.mat(xArr).transpose() * yArr
    return w

#标准化处理
def ridgeTest(xArr,yArr):
    xMat = np.mat(xArr)
    yMat = np.mat(yArr).transpose()
    yMean = np.mean(yMat,0)
    yMat = yMat - yMean
    xMean = np.mean(xMat,0)
    xVar = np.var(xMat,0)
    xMat = (xMat - xMean)/xVar
    numTest = 30
    wMat = np.zeros((numTest, np.shape(xMat)[1]))
    for i in range(numTest):
        w = ridgeRegres(xMat,yMat,math.exp(i-10))
        wMat[i,:] = w.transpose()
    return wMat

#均值为零，方差为1    
def regularize(xArr):
    xMean = np.mean(xArr,0)
    xVar = np.var(xArr,0)
    xMat = (xArr - xMean)/xVar
    return xMat

def rssError(yArr, yHat):
    return (((yArr - yHat)**2).sum())

#前向逐步线性回归
def stageWise(xArr, yArr, eps=0.01, numIt =100):
    xMat = np.mat(xArr)
    yMat = np.mat(yArr).transpose()
    yMean = np.mean(yMat,0)
    yMat = yMat - yMean
    xMat = regularize(xArr)
    row,col = np.shape(xMat)
    returnMat = np.zeros((numIt, col))
    ws = np.mat(np.zeros((col,1)))
    wsTest = ws.copy()
    wsMat = ws.copy()
    for i in range(numIt):
        print(ws.transpose())
        lowestError = math.inf
        for j in range(col):
            for sign in [-1,1]:
                wsTest = ws.copy()
                wsTest[j] += eps * sign
                yTest = xMat * wsTest
                rssE = rssError(yMat.A, yTest.A)
                if rssE < lowestError:
                    lowestError = rssE
                    wsMat = wsTest
        ws = wsMat.copy()
        returnMat[i,:] = ws.transpose()
    return returnMat

#预测乐高玩具价格
from time import sleep
import json
import urllib
def searchForSet(retX, retY, setNum, yr, numPce, origPrc):
    sleep(10)
    myAPIstr = 'AIzaSyD2cR2KFyx12hXu6PFU-wrWot3NXvko8vY'  
    searchURL = 'https://www.googleapis.com/shopping/search/v1/public/products?key=%s&country=US&q=lego+%d&alt=json' % (myAPIstr, setNum)  
    pg = urllib.request.urlopen(searchURL)
    retDict = json.loads(pg.read())
    for i in range(len(retDict['items'])):
        try:
            curItem = retDict['item'][i]
            if curItem['product']['condition'] == 'new':
                newFlag = 1
            else:
                newFlag = 0
            listOfInv =curItem['product']['inventories']
            for item in listOfInv:
                sellingPrice = item['price']
                if sellingPrice > origPrc * 0.5:
                    print("%d\t%d\t%d\t%f\t%f" % \
                        (yr, numPce, newFlag, origPrc, sellingPrice))
                    retX.append([yr, numPce, newFlag, origPrc])
                    retY.append([sellingPrice])
        except: print('problem with item %d' % i)

def setDataCollect(retX,retY):
            searchForSet(retX, retY, 8288, 2006, 800, 49.99)
            searchForSet(retX, retY, 10030, 2002, 3096, 269.99)
            searchForSet(retX, retY, 10179, 2007, 5195, 499.99)
            searchForSet(retX, retY, 10181, 2007, 3428, 199.99)
            searchForSet(retX, retY, 10189, 2008, 5922, 299.99)
            searchForSet(retX, retY, 10196, 2009, 3263, 249.99)
            
    