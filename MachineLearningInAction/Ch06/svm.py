# -*- coding: utf-8 -*-
'''
Created on Aug 22, 2017
@author: manny
'''
import numpy as np
from math import exp


#加载数据
def loadDataSet(filename):
    dataMatrix = []
    labelMatrix = []
    fr = open(filename)
    for line in fr.readlines():
        lineArr = line.strip().split('\t')
        dataMatrix.append([float(lineArr[0]), float(lineArr[1])])
        labelMatrix.append(float(lineArr[2]))
    return dataMatrix,labelMatrix
    
#选择随机数，i是当前alpha下标，m是所有alpha总数
def selRand(i,m):
    j=i
    while(j==i):
        j=int(np.random.uniform(0,m))
    return j
 
#调整大于H或者小于L的alpha值
def clipAlpha(aj,H,L):
    if aj > H:
        aj = H
    if aj < L:
        aj = L
    return aj
    
'''
创建一个alpha向量并初始化
当迭代次数小于最大迭代次数：
    对数据集中的每个向量
        如果该数据向量可以被优化
            随机选择另一个数据向量
            同时优化这两个向量
            如果两个向量都不能被优化，退出本次循环
     如果所有向量都没有被优化，增加迭代次数，继续下一次优化
'''

def simplifiedSmo(dataMatrix,labelMatrix,C,toler,maxIter):#toler，容错率；
    dataMatrix = np.mat(dataMatrix)
    labelMatrix = np.mat(labelMatrix).transpose()
    b = 0
    row,col = np.shape(dataMatrix)
    alphas = np.mat(np.zeros((row,1)))
    iterNum = 0
    while (iterNum < maxIter):
        alphasPairsChanged = 0
        #遍历数据矩阵每一行
        for i in range(row):
            #预测值f(xi)=∑aiyiK(xj,xi)+b
            fxi = np.multiply(alphas,labelMatrix).transpose() * \
            (dataMatrix * dataMatrix[i,:].transpose()) + b
            #预测值与真实值之差
            Ei = fxi - float(labelMatrix[i])
            #判断alpha是否可以优化
            if(((labelMatrix[i]*Ei < -toler) and (alphas[i] < C)) or \
                ((labelMatrix[i]*Ei > toler) and (alphas[i] > 0))):
                #进入优化程序，随机选择另一个变量
                j = selRand(i,row)
                #预测值f(xj)
                fxj = float(np.multiply(alphas,labelMatrix).transpose() * \
                (dataMatrix * dataMatrix[j,:].transpose())) + b
                #j的预测值与真实值之差
                Ej = fxj - float(labelMatrix[j])
                #保存旧的alphas[i]和alphas[j]
                alphaIold = alphas[i].copy()
                alphaJold = alphas[j].copy()
            #保证alpha满足约束条件0< alpha <C
                if(labelMatrix[i] != labelMatrix[j]):
                    L = max(0, alphas[j] - alphas[i])
                    H = min(C, C + alphas[j] - alphas[i])
                else:
                    L = max(0, alphas[j] + alphas[i] - C)
                    H = min(C, alphas[j] + alphas[i])
                #如果L=H，跳出本次循环
                if L==H:
                    print('L==H')
                    continue
                #
                eta = 2.0 * dataMatrix[i,:] * dataMatrix[j,:].transpose() - \
                        dataMatrix[i,:] * dataMatrix[i,:].transpose() - \
                        dataMatrix[j,:] * dataMatrix[j,:].transpose()
                if eta >= 0:
                    print('eta>=0')
                    continue
                #未剪裁之前的导数值
                alphas[j] -=labelMatrix[j] * (Ei - Ej)/eta
                #对alphas[j]进行剪裁，使其落在[0,C]之间
                alphas[j] = clipAlpha(alphas[j], H, L)
                #
                if(abs(alphas[j] - alphaJold) < 0.00001):
                    print('j not moving enough')
                    continue
                #根据alphasp[j]计算alphas[i]
                alphas[i] += labelMatrix[j] * labelMatrix[i] * (alphaJold - alphas[j])
                #如果alpha是[i]落在[0,C],则选择b1,
                b1 = b -Ei -labelMatrix[i] * (alphas[i] - alphaIold) * \
                    dataMatrix[i,:] * dataMatrix[i,:].transpose() - \
                    labelMatrix[j] * (alphas[j] - alphaJold) * \
                    dataMatrix[i,:] * dataMatrix[j,:].transpose()
                #如果alpha是[j]落在[0,C],则选择b2,
                b2 = b -Ej -labelMatrix[i] * (alphas[i] - alphaIold) * \
                    dataMatrix[i,:] * dataMatrix[j,:].transpose() - \
                    labelMatrix[j] * (alphas[j] - alphaJold) * \
                    dataMatrix[j,:] * dataMatrix[j,:].transpose()
                if((alphas[i] < C) and (alphas[i] > 0)):
                    b = b1
                elif((alphas[j] < C) and (alphas[j] > 0)):
                    b = b2
                #否则选择b1,b2均值
                else:
                    b = (b1 + b2)/2.0
                alphasPairsChanged += 1
                print('iter: %d i: %d,pairs changed %d' % (iterNum, i, alphasPairsChanged))
        #检查alphas是否更新，如果有更新，iter归零继续运行程序
        if(alphasPairsChanged == 0):
            iterNum += 1
        else:
            iterNum = 0
        print('iter num is: %d' % iterNum)
    return b,alphas
     
#
class optStruct:
    def __init__(self,dataMatrix,labelMatrix,C,toler,kTup):
        self.dataMatrix  =dataMatrix
        self.labelMatrix = labelMatrix
        self.C = C
        self.toler = toler
        self.row = np.shape(dataMatrix)[0]
        self.alphas = np.mat(np.zeros((self.row, 1)))
        self.b = 0
        #第一列是是否有效的标志位，第二列是实际E值
        self.ecache = np.mat(np.zeros((self.row, 2)))
        self.kTup = np.mat(np.zeros((self.row,self.row)))
        for i in range(self.row):
            self.kTup[:, i] = kernalTrans(self.dataMatrix, self.dataMatrix[i, :], kTup)

#计算E值并返回        
def calcEk(optStr, k):
    '''
    fxk = np.multiply(optStr.alphas,optStr.labelMatrix).transpose() * \
            (optStr.dataMatrix * optStr.dataMatrix[k,:].transpose()) + optStr.b
    Ek= fxk - float(optStr.labelMatrix[k])
    '''
    fxk = np.multiply(optStr.alphas,optStr.labelMatrix).transpose() * \
            optStr.kTup[:,k]+ optStr.b
    Ek= fxk - float(optStr.labelMatrix[k])  
    return Ek
 
#选择合适的第二个alpha值，以保证每次优化中采用最大步长 
def selectJ(i, optStr, Ei):
    maxK = -1
    maxDeltaE = 0
    Ej = 0
    optStr.ecache[i] = [1,Ei]
    #nonzero返回非零的矩阵行和列信息，[0]即为非零值E对应的alpha值
    validEcacheList = np.nonzero(optStr.ecache[:,0])[0]
    
    if (len(validEcacheList)) > 1:
        for k in validEcacheList:
            if k == i:
                continue
            Ek = calcEk(optStr, k)
            deltaE = abs(Ei - Ek)
            if(deltaE > maxDeltaE):
                maxK = k
                maxDeltaE = deltaE
                Ej = Ek
        return maxK,Ej
    #如果这是第一次循环的话，随机选择一个alpha值
    else:
        j = selRand(i, optStr.row)
        Ej = calcEk(optStr, j)
    return j,Ej
 
 #计算误差E并保存起来
def updateEk(optStr, k):
    Ek = calcEk(optStr, k)
    optStr.ecache[k] = [1,Ek]
    
#
def innerL(i,optStr):
    Ei = calcEk(optStr, i)
    if(((optStr.labelMatrix[i] * Ei < -optStr.toler) and (optStr.alphas[i] < optStr.C))or \
        ((optStr.labelMatrix[i] * Ei > optStr.toler) and (optStr.alphas[i] > 0))):
        j,Ej = selectJ(i,optStr,Ei)
        alphaIold = optStr.alphas[i].copy()
        alphaJold = optStr.alphas[j].copy()
        if(optStr.labelMatrix[i] != optStr.labelMatrix[j]):
            L = max(0, optStr.alphas[j] - optStr.alphas[i])
            H = min(optStr.C, optStr.C + optStr.alphas[j] - optStr.alphas[i])
        else:
            L = max(0, optStr.alphas[j] + optStr.alphas[i] - optStr.C)
            H = min(optStr.C, optStr.alphas[j] + optStr.alphas[i])
        if(L == H):
            print('L==H')
            return 0
        #eta = 2.0 * optStr.dataMatrix[i,:] * optStr.dataMatrix[j,:].transpose() - \
        #           optStr.dataMatrix[i,:] * optStr.dataMatrix[i,:].transpose() - \
        #            optStr.dataMatrix[j,:] * optStr.dataMatrix[j,:].transpose()
        eta = 2.0 * optStr.kTup[i,j] - optStr.kTup[i,i] - optStr.kTup[j,j]
        if(eta >= 0):
            print('eta>=0')
            return 0
        optStr.alphas[j] -= optStr.labelMatrix[j] * (Ei - Ej)/eta
        optStr.alphas[j] = clipAlpha(optStr.alphas[j],H,L)
        updateEk(optStr,j)
        if(abs(optStr.alphas[j] - alphaJold) < 0.00001):
            print('j not moving enough')
            return 0
                #根据alphasp[j]计算alphas[i]
        optStr.alphas[i] += optStr.labelMatrix[j] * optStr.labelMatrix[i] * \
                                (alphaJold - optStr.alphas[j])
                #如果alpha是[i]落在[0,C],则选择b1,
        updateEk(optStr,i)
        '''
        b1 = optStr.b -Ei - optStr.labelMatrix[i] * (optStr.alphas[i] - alphaIold) * \
            optStr.dataMatrix[i,:] * optStr.dataMatrix[i,:].transpose() - \
            optStr.labelMatrix[j] * (optStr.alphas[j] - alphaJold) * \
            optStr.dataMatrix[i,:] * optStr.dataMatrix[j,:].transpose()
                #如果alpha是[j]落在[0,C],则选择b2,
        b2 = optStr.b -Ej -optStr.labelMatrix[i] * (optStr.alphas[i] - alphaIold) * \
            optStr.dataMatrix[i,:] * optStr.dataMatrix[j,:].transpose() - \
            optStr.labelMatrix[j] * (optStr.alphas[j] - alphaJold) * \
            optStr.dataMatrix[j,:] * optStr.dataMatrix[j,:].transpose()
        '''
        b1 = optStr.b - Ei - optStr.labelMatrix[i] * (optStr.alphas[i] - alphaIold) * optStr.kTup[i,i] - \
                            optStr.labelMatrix[j] * (optStr.alphas[j] - alphaJold) * optStr.kTup[i,j]
        b2 = optStr.b - Ei - optStr.labelMatrix[i] * (optStr.alphas[i] - alphaIold) * optStr.kTup[i,j] - \
                            optStr.labelMatrix[j] * (optStr.alphas[j] - alphaJold) * optStr.kTup[j,j]            
        if((optStr.alphas[i] < optStr.C) and (optStr.alphas[i] > 0)):
            optStr.b = b1
        elif((optStr.alphas[j] < optStr.C) and (optStr.alphas[j] > 0)):
            optStr.b = b2
                #否则选择b1,b2均值
        else:
            optStr.b = (b1 + b2)/2.0 
        return 1
    else:
        return 0

def smoP(dataMatrix,labelMatrix,C,toler,maxIter,kTup=('lin', 0)):
    optStr = optStruct(np.mat(dataMatrix), np.mat(labelMatrix).transpose(), C, toler, kTup)
    iterNum = 0
    entriesSet = True
    alphasPairsChanged = 0
    while((iterNum < maxIter) and (alphasPairsChanged > 0) or (entriesSet)):
        alphasPairsChanged = 0
        if entriesSet:
            for i in range(optStr.row):
                alphasPairsChanged += innerL(i, optStr)
            print("fullSet,iter: %d i: %d, pairs changed %d" % (iterNum, i, alphasPairsChanged))
            iterNum += 1
        else:
            nonBoundIS = np.nonzero((np.array(optStr.alphas) > 0) * (np.array(optStr.alphas) < C))[0]
            for i in nonBoundIS:
                alphasPairsChanged += innerL(i,optStr)
                print("nonBoundIS, iter :%d i: %d,pairs changed %d" % (iterNum, i,alphasPairsChanged))
            iterNum += 1
        if entriesSet:
            entriesSet = False
        elif (alphasPairsChanged == 0):
            entriesSet = True
        print("iternation num :%d" % iterNum)
    return optStr.b,optStr.alphas

def calcWs(alphas, dataMatrix, labelMatrix):
    dataMatrix = np.mat(dataMatrix)
    labelMatrix = np.mat(labelMatrix).transpose()
    row, col = np.shape(dataMatrix)
    w = np.zeros((col, 1))
    for i in range(row):
        w += np.multiply(alphas[i] * labelMatrix[i], dataMatrix[i,:].transpose())
    return w
    
#核函数
def kernalTrans(X, A, kTup):
    row, col = np.shape(X)
    K = np.mat(np.zeros((row, 1)))
    if kTup[0] =='lin':
        K = np.mat(X*A).transpose()
    elif kTup[0] == 'rbf':
        for i in range(row):
            deltaRow = X[i,:] - A
            K[i] = deltaRow * deltaRow.transpose()
            K[i] = exp(K[i] / (-1*kTup[1]**2))
    else:
        raise NameError('Houston we have a probles -- Taht kerbel is not recognized')
    return K
    
#径向基测试函数
def testRbf(k1=1.3):
    dataMatrix, labelMatrix =loadDataSet('testSetRBF.txt')
    b, alphas = smoP(dataMatrix,labelMatrix,200,0.0001,10000,('rbf', k1))
    dataMatrix = np.mat(dataMatrix)
    labelMatrix = np.mat(labelMatrix).transpose()
    svInd = np.nonzero(np.array(alphas) > 0 )[0]
    sVs =dataMatrix[svInd]
    labelSV = labelMatrix[svInd]
    print("there are %d support machines" % np.shape(sVs)[0])
    row, col =np.shape(dataMatrix)
    errorCount = 0
    for i in range(row):
        kernalEval = kernalTrans(sVs,dataMatrix[i,:],('rbf',k1))
        predict = kernalEval.transpose() * np.multiply(labelSV,alphas[svInd]) + b
        if np.sign(predict) != np.sign(labelMatrix[i]):
            errorCount += 1
    print("the training rate is %f" % (float(errorCount)/row))
    dataMatrix,labelMatrix = loadDataSet('testSetRBF2.txt')
    errorCount = 0
    dataMatrix = np.mat(dataMatrix)
    labelMatrix = np.mat(labelMatrix).transpose()
    row,col =np.shape(dataMatrix)
    for i in range(row):
        kernalEval = kernalTrans(sVs,dataMatrix[i,:],('rbf',k1))
        predict = kernalEval.transpose() * np.multiply(labelSV,alphas[svInd]) + b
        if np.sign(predict) != np.sign(labelMatrix[i]):
            errorCount += 1
    print("the test rate is %f" % (float(errorCount)/row))        