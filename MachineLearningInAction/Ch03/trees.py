'''
Created on Aug 16, 2017
trees: 
Input:  inX: vector to compare to existing dataSet (1xN)
        dataSet: size m data set of known vectors (NxM)
        labels: data set labels (1xM vector)
        k: number of neighbors to use for comparison (should be an odd number)
Output: the most popular class label
@author: manny
'''

from math import log
import operator

#cal dataSet shannonEnt
def calShannonEnt(dataSet):
    numEntries = len(dataSet)
    labelCounts = {}
    for featureVec in dataSet:
        currentLabel = featureVec[-1]
        if currentLabel not in labelCounts.keys():#key为某一特征值，value为特征值出现的次数
            labelCounts[currentLabel] = 0
        labelCounts[currentLabel] += 1
    shannonEnt = 0.0
    for key in labelCounts:
        prob = float(labelCounts[key]/numEntries) #计算特征值出现概率
        shannonEnt -= prob * log(prob,2) #信息熵
    return shannonEnt
    
#create dataSet
def createdataSet():
    dataSet = [[1,1,'yes'],
    [1,1,'yes'],    
    [1,0,'yes'],
    [0,1,'no'],
    [0,1,'no']]
    labels = ['no surfacing','flippers']
    return dataSet, labels
    
#划分数据集
def splitdataSet(dataSet,axis,value):
    retdataSet = []
    for featureVec in dataSet:
        if featureVec[axis] == value:
            reducedfeatureVec = featureVec[:axis]
            reducedfeatureVec.extend(featureVec[axis+1:]) #redeuce axis 所在位置的value值，注意append和extend区别
            retdataSet.append(reducedfeatureVec)
    return retdataSet

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
        #某一维度中，某个value的信息
        for value in uniqueVals:
            subdataSet = splitdataSet(dataSet,i,value)
            prob = len(subdataSet)/float(len(dataSet))
            newEntropy += prob*calShannonEnt(subdataSet)
        infoGain = baseEntropy - newEntropy
        if(infoGain > bestInfoGain):
            bestInfoGain = infoGain
            bestFeature = i
    return bestFeature

#返回出现次数最多的分类名称
def majorityCnt(classList):
    classCount = {}
    for vote in classList:
        if vote not in classCount:
            classCount[vote] = 0
        classCount[vote] += 1
        sortedClassCount = sorted(classCount.items(),key=operator.itemgetter(1),reverse=True)
        '''item()方法把字典中每对key和value组成一个元组，
        并把这些元组放在列表中返回;key为函数，作用于对象上，
        operator提供的itemgetter函数用于获取对象哪些维的数据'''
        return sortedClassCount[0][0]
        
#创建树
def createTree(dataSet,labels):
    classList = [example[-1] for example in dataSet]
    if classList.count(classList[0]) == len(classList):
        return classList[0] #如果特征值数目等于行数
    if len(dataSet[0]) ==1:
        return majorityCnt(classList)
    bestFeature = chooseBestFeature2Split(dataSet)
    bestFeatureLabel = labels[bestFeature]
    myTree = {bestFeatureLabel:{}}
    del(labels[bestFeature]) #删除bestFeature 对应的label
    featureValues = [example[bestFeature] for example in dataSet]
    uniqueVals = set(featureValues)
    for value in featureValues:
        subLabels = labels[:] #[:],复制labels给到subLabels
        myTree[bestFeatureLabel][value] = createTree(splitdataSet(dataSet,bestFeature,value),subLabels)
    return myTree
    
#
def classfy(inputTree, featureLabels, testVec):
    firstStrtemp = list(inputTree.keys())
    firstStr = firstStrtemp[0]
    secondDict = inputTree[firstStr]
    featureIndex = featureLabels.index(firstStr)
    for key in secondDict.keys():
        if testVec[featureIndex] ==key:
            if type(secondDict[key]).__name__ == 'dict':
                classLabel = classfy(secondDict[key], featureLabels, testVec)
            else:
                classLabel = secondDict[key]
    return classLabel
    
#使用pickle模块存储决策树
def storeTree(inputTree,filename):
    import pickle
    fw = open(filename,'wb')
    pickle.dump(inputTree,fw)
    fw.close()
    
def grabTree(filename):
    import pickle
    fr = open(filename,'rb')
    return pickle.load(fr)
 
    
    
        





