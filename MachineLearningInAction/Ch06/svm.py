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
                    