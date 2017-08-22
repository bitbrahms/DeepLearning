'''
Created on Aug 21, 2017
@author: manny
'''
# -*- coding: utf-8 -*-

import numpy as np
from math import log

#词条集合
def loadDataSet():
    postingList=[['my', 'dog', 'has', 'flea', 'problems', 'help', 'please'],
                ['maybe', 'not', 'take', 'him', 'to', 'dog', 'park', 'stupid'],
                ['my', 'dalmation', 'is', 'so', 'cute', 'I', 'love', 'him'],
                ['stop', 'posting', 'stupid', 'worthless', 'garbage'],
                ['mr', 'licks', 'ate', 'my', 'steak', 'how', 'to', 'stop', 'him'],
                ['quit', 'buying', 'worthless', 'dog', 'food', 'stupid']]
    classVec = [0,1,0,1,0,1]
    return postingList, classVec

#文档中所有词的列表
def createVocabList(dataSet):
    vocabSet = set([])
    for doc in dataSet:
        vocabSet = vocabSet | set(doc)
    return list(sorted(vocabSet))

#输入词汇表以及文档，输出文档向量
def setWords2Vec(vocabList,inputSet):
    returnVec = [0]*len(vocabList)
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)] = 1
        else:
            print("the word %s is not in my vocabList" % word)
    return returnVec
    
#
def trainBayes(trainMatrix, trainCategory):
    numTrainDocs = len(trainMatrix)
    numWords = len(trainMatrix[0])
    p_abusive = np.sum(trainCategory)/float(numTrainDocs)
    p0_num = np.ones(numWords)
    p1_num = np.ones(numWords)
    p0_sum = 2.0
    p1_sum = 2.0
    for i in range(numTrainDocs):
        if trainCategory[i] == 1:
            p1_num += trainMatrix[i]
            p1_sum += np.sum(trainMatrix[i])
        else:
            p0_num += trainMatrix[i]
            p0_sum += np.sum(trainMatrix[i])
    #pa_sum = [p1_sum]*numWords
    #p0_sum = [p0_sum]*numWords
    p1_vec_temp = p1_num/p1_sum #log函数不能直接对矩阵进行直接操作
    p0_vec_temp = p0_num/p0_sum
    p1_vec = [log(i) for i in p1_vec_temp]
    p0_vec = [log(i) for i in p0_vec_temp]
    return p0_vec,p1_vec,p_abusive
    
#朴素贝叶斯分类函数
def classfyBayes(vec2Classfy, p0_vec, p1_vec, p_abusive):
    p1 = sum(np.array(vec2Classfy) * np.array(p1_vec)) + log(p_abusive)
    p0 = sum(np.array(vec2Classfy) * np.array(p0_vec)) + log(1-p_abusive)
    if p1 > p0:
        return 1
    else:
        return 0
        
#简单测试0
def testingBayes():
    listPosts,listClasses = loadDataSet()
    myVocabList = createVocabList(listPosts)
    trainMatrix = []
    for i in listPosts:
        trainMatrix.append(setWords2Vec(myVocabList, i))
    p0_vec,p1_vec,p_abusive = trainBayes(trainMatrix, listClasses)
    testEntry = ['love','my','dog']
    test1 = setWords2Vec(myVocabList,testEntry)
    print(test1,'classfied as: ',classfyBayes(test1,p0_vec,p1_vec,p_abusive))
   
#bag of words
def bagofWords2Vec(vocabList,inputSet):
    returnVec = [0]*len(vocabList)#创建词汇列表对应位全为0的list
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)] += 1#统计词汇出现频次
    return returnVec
    
#切割文件
def textParse(bigString):#切割文件
    listofToken = bigString.split('\W*')
    return [token.lower() for token in listofToken if len(token) > 2]

#垃圾邮件测试
def spamTest():
    docList = []
    classList = []
    fullText = []
    for i in range(1,26):
        wordList = textParse(open('email/spam/%d.txt' % i).read())
        docList.append(wordList)
        fullText.append(wordList)
        classList.append(1)
        
        wordList = textParse(open('email/ham/%d.txt' % i,'r',encoding='utf-8').read())
        docList.append(wordList)
        fullText.append(wordList)
        classList.append(0)
        
    vocabList = createVocabList(docList)
    trainingSet = list(range(50))
    testSet = []
    for i in range(10):
        randIndex = int(np.random.uniform(0,len(trainingSet)))
        testSet.append(trainingSet[randIndex])
        del(trainingSet[randIndex])
    trainMatrix = []
    trainCategory = []
    #创建训练矩阵以及对应的标签
    for doc in trainingSet:
        trainMatrix.append(setWords2Vec(vocabList, docList[doc]))
        trainCategory.append(classList[doc])
    #计算概率
    p0_v, p1_v, pSpam = trainBayes(trainMatrix, trainCategory)
    errorCount = 0
    for doc in testSet:
        wordVector = setWords2Vec(vocabList, docList[doc])
        if classfyBayes(wordVector,p0_v,p1_v,pSpam) != classList[doc]:
            errorCount += 1
    print('the error rate is : ', float((errorCount)/len(testSet)))
    
#高频词去除函数以及RSS源分类器
def calMostFreq(vocabList, fullText):
    import operator
    freqDict = {}
    for token in vocabList:
        freqDict[token] = fullText.count(token)
    sortedFreq = sorted(freqDict.items(), key=operator.itemgetter(1), reverse=True)
    return sortedFreq[:30]
    
def localWords(feed1, feed0):#feed0和feed1是两个rss源
    import feedparser
    docList = []
    classList = []
    fullText = []
    minLen = min(len(feed1['entries']), len(feed0['entries']))
    for i in range(minLen):
        wordList = textParse(feed1['entries'][i]['summary'])
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(1)
        wordList = textParse(feed0['entries'][i]['summary'])
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(0)
    #创建不重复词汇列表
    vocabList = createVocabList(docList)
    #滤出高频词汇
    top30Words = calMostFreq(vocabList, fullText)
    #移除词汇列表中的高频词汇
    for words in top30Words:
        if words[0] in vocabList:
            vocabList.remove(words[0])
    
    trainingSet = list(range(2*minLen))
    testSet = []
    #创建testSet
    for i in range(20):
        randIndex = int(np.random.uniform(0,len(trainingSet)))
        testSet.append(trainingSet[randIndex])
        del(trainingSet[randIndex])
        
    trainMatrix = []
    trainCategory = []
    #创建train矩阵以及标签
    for doc in trainingSet:
        trainMatrix.append(bagofWords2Vec(vocabList,docList[doc]))
        trainCategory.append(classList[doc])
    p0_v,p1_v,pSpam = trainBayes(trainMatrix,trainCategory)
    errorCount = 0.0
    #检测分类效果
    for doc in testSet:
        wordVector = bagofWords2Vec(vocabList, docList[doc])
        if classfyBayes(wordVector,p0_v,p1_v,pSpam) != classList[doc]:
            errorCount += 1
    print('the error rate is: ',float(errorCount/len(testSet)))
    return vocabList,p0_v,p1_v
    
#最具表征性函数
def getTopWords(ny,sf):
    import operator
    vocabList,p0_v,p1_v = localWords(ny,sf)
    topny = []
    topsf = []
    for i in range(len(p0_v)):
        if p0_v[i] > -6.0:
            topsf.append((vocabList[i],p0_v[i]))
        if p1_v[i] > -6.0:
            topny.append((vocabList[i],p1_v[i]))
    sortedsf = sorted(topsf, key=operator.itemgetter(1), reverse=True)
    for i in sortedsf:
        print(i[0])
    sortedny = sorted(topny, key=operator.itemgetter(1), reverse=True)
    for i in sortedny:
        print(i[0])