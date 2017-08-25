# -*- coding: utf-8 -*-
'''
Created on Aug 22, 2017
@author: manny
'''
import numpy as np


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
    def __init__(self,dataMatrix,labelMatrix,C,toler):
        self.dataMatrix  =dataMatrix
        self.labelMatrix = labelMatrix
        self.C = C
        self.toler = toler
        self.row = np.shape(dataMatrix)[0]
        self.alphas = np.mat(np.zeros((self.row, 1)))
        self.b = 0
        #第一列是是否有效的标志位，第二列是实际E值
        self.ecache = np.dataMatrix(np.zeros((self.row, 2)))

#计算E值并返回        
def calcEk(optStruct, k):
    fxk = np.multiply(optStruct.alphas,optStruct.labelMatrix).transpose() * \
            (optStruct.dataMatrix * optStruct.dataMatrix[i,:].transpose()) + optStruct.b
    Ek= fxk - float(optStruct.labelMatrix[k])
    return Ek
 
#选择合适的第二个alpha值，以保证每次优化中采用最大步长 
def selectJ(i, optStruct, Ei):
    maxK = -1
    maxDeltaE = 0
    Ej = 0
    optStruct.ecache[i] = [1,Ei]
    #nonzero返回非零的矩阵行和列信息，[0]即为非零值E对应的alpha值
    validEcacheList = np.nonzeros(optStruct.ecache[:,0])[0]
    
    if (len(validEcacheList)) > 1:
        for k in validEcacheList:
            if k == i:
                continue
            Ek = calcEk(optStruct, k)
            deltaE = abs(Ei - Ek)
            if(deltaE > maxDeltaE):
                maxK = k
                maxDeltaE = deltaE
                Ej = Ek
        return maxK,Ej
    #如果这是第一次循环的话，随机选择一个alpha值
    else:
        j = selRand(i, optStruct.row)
        Ej = calcEk(optStruct, j)
    return j,Ej
 
 #计算误差E并保存起来
def updateEk(optStruct, k):
    Ek = calcEk(optStruct, k)
    optStruct.ecache[k] = [1,Ek]
    
#
def innerL(i,optStruct):
    Ei = calcEk(optStruct, i)
    if(((optStruct.labelMatrix[i] * Ei < -optStruct.toler) and (optStruct.alphas[i] < optStruct.C))or \
        ((optStruct.labelMatrix[i] * Ei > optStruct.toler) and (optStruct.alphas[i] > 0))):
        j,Ej = selectJ(i,optStruct,Ei)
        alphaIold = optStruct.alphas[i].copy()
        alphaJold = optStruct.alphas[j].copy()
        if(optStruct.labelMatrix[i] != optStruct.labelMatrix[j]):
            L = max(0, optStruct.alphas[j] - optStruct.alphas[i])
            H = min(optStruct.C, optStruct.C + optStruct.alphas[j] - optStruct.alphas[i])
        else:
            L = max(0, optStruct.alphas[j] + optStruct.alphas[i] - optStruct.C)
            H = min(optStruct.C, optStruct.alphas[j] + optStruct.alphas[i])
        if(L == H):
            print('L==H')
            continue
        eta = 2.0 * optStruct.dataMatrix[i,:] * optStruct.dataMatrix[j,:].transpose() - \
                    optStruct.dataMatrix[i,:] * optStruct.dataMatrix[i,:].transpose() - \
                    optStruct.dataMatrix[j,:] * optStruct.dataMatrix[j,:].transpose()
        if(eta >= 0):
            print('eta>=0')
            return 0
        optStruct.alphas[j] -= optStruct.labelMatrix[j] * (Ei - Ej)/eta
        optStruct.alphas[j] = clipAlpha(optStruct.alphas[j],H,L)
        updateEk(optStruct,j)
        if(abs(optStruct.alphas[j] - alphaJold) < 0.00001):
            print('j not moving enough')
            continue
                #根据alphasp[j]计算alphas[i]
        optStruct.alphas[i] += optStruct.labelMatrix[j] * optStruct.labelMatrix[i] * \
                                (alphaJold - optStruct.alphas[j])
                #如果alpha是[i]落在[0,C],则选择b1,
        updateEk(optStruct,i)
        b1 = optStruct.b -Ei - optStruct.labelMatrix[i] * (optStruct.alphas[i] - alphaIold) * \
            optStruct.dataMatrix[i,:] * optStruct.dataMatrix[i,:].transpose() - \
            optStruct.labelMatrix[j] * (optStruct.alphas[j] - alphaJold) * \
            optStruct.dataMatrix[i,:] * optStruct.dataMatrix[j,:].transpose()
                #如果alpha是[j]落在[0,C],则选择b2,
        b2 = optStruct.b -Ej -optStruct.labelMatrix[i] * (optStruct.alphas[i] - alphaIold) * \
            optStruct.dataMatrix[i,:] * optStruct.dataMatrix[j,:].transpose() - \
            optStruct.labelMatrix[j] * (optStruct.alphas[j] - alphaJold) * \
            optStruct.dataMatrix[j,:] * optStruct.dataMatrix[j,:].transpose()
        if((optStruct.alphas[i] < optStruct.C) and (optStruct.alphas[i] > 0)):
            optStruct.b = b1
        elif((optStruct.alphas[j] < optStruct.C) and (optStruct.alphas[j] > 0)):
            optStruct.b = b2
                #否则选择b1,b2均值
        else:
            optStruct.b = (b1 + b2)/2.0 
        return 1
    else:
        return 0
        
def smoP(dataMatrix,labelMatrix,C,toler,maxIter,kTup=('lin', 0)):
    optStruct = optStruct(np.mat(dataMatrix), np.mat(labelMatrix).transpose(), C, toler)
    iterNum = 0
    entriesSet = True
    alphasPairsChanged = 0
    while((iterNum < maxIter) and (alphasPairsChanged > 0) or (entriesSet)):
        alphasPairsChanged = 0
        if entriesSet:
            for i in range(optStruct.row):
                alphasPairsChanged += innerL(i, optStruct)
            print("fullSet,iter: %d i: %d, pairs changed %d" % (iterNum, i, alphasPairsChanged))
            iterNum += 1
        else:
            nonBoundIS = np.nonzore((optStruct.alphas > 0) * (optStruct.alphas < C))[0]
            for i in nonBoundIS:
                alphasPairsChanged += innerL(i,optStruct)
                print("nonBoundIS, iter :%d i: %d,pairs changed %d" % (iterNum, i,alphasPairsChanged))
            iterNum += 1
        if entriesSet:
            entriesSet = False
        elif (alphasPairsChanged == 0):
            entriesSet = True
        print("iternation num :%d" % iterNum)
    return optStruct.b,optStruct.alphas