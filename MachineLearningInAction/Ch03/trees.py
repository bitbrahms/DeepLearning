'''
Created on Aug 16, 2017
trees: 
Input:  inX: vector to compare to existing dataset (1xN)
        dataSet: size m data set of known vectors (NxM)
        labels: data set labels (1xM vector)
        k: number of neighbors to use for comparison (should be an odd number)
Output: the most popular class label
@author: manny
'''

from math import log

#cal dataset shannonEnt
def calShannonEnt(dataSet):
    numEntries = len(dataSet)
    labelCounts = {}
    for featVec in dataSet:
        currentLabel = featVec[-1]
        if currentLabel not in labelCounts.keys():
            labelCounts[currentLabel] = 0
        labelCounts[currentLabel] += 1
    shannonEnt = 0.0
    for key in labelCounts:
        prob = float(labelCounts[key]/numEntries)
        shannonEnt -= prob * log(prob,2)
    return shannonEnt
    
#create dataset
def createDataset():
    dataSet = [[1,1,'yes'],
    [1,1,'yes'],
    [1,0,'no'],
    [0,1,'no'],
    [0,1,'no']]
    labels = ['no surfacing','flippers']
    return dataSet, labels
    
#划分数据集
def splitDataSet(dataSet,axis,value):
    retDataSet = []
    for featVec in dataSet:
        if featVec[axis] == value:
            reducedFeatVec = featVec[:axis]
            reducedFeatVec.extend(featVec[axis+1:]) #redeuce axis 所在位置的value值，注意append和extend区别
            retDataSet.append(reducedFeatVec)
    return retDataSet

#选择最好的数据集划分方式
def chooseBestFeature2Split(dataSet):
    numFeatures = len(dataSet[0]) - 1 #特征值数目
    baseEntropy = calShannonEnt(dataSet) #计算原始香浓熵
    bestInfoGain = 0.0
    bestFeature = -1
    for i in range(numFeatures):
        featureList = [example[i] for example in dataSet]
        uniqueVals = set(featureList) #set,集合中所有值互不相同
        newEntropy = 0.0
        for value in uniqueVals:
            subDataSet = splitDataSet(dataSet,i,value)
            prob = len(subDataSet)/float(len(dataSet))
            newEntropy += prob*calShannonEnt(subDataSet)
        infoGain = baseEntropy - newEntropy
        if(infoGain > bestInfoGain):
            bestInfoGain = infoGain
            bestFeature = i
    return bestFeature
    




