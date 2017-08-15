'''
Created on Mar 14, 2017
kNN: k Nearest Neighbors
Input:  inX: vector to compare to existing dataset (1xN)
        dataSet: size m data set of known vectors (NxM)
        labels: data set labels (1xM vector)
        k: number of neighbors to use for comparison (should be an odd number)
Output: the most popular class label
@author: manny
'''

from numpy import *
import operator
from os import listdir

def createDataSet():
    group = array([[1.0,1.1],[1.0,1.0],[1.0,1.0],[1.0,1.0]])
    labels = ['A','A','B','B']
    return group,labels

#近邻比较    
def classfy0(inx, dataset, labels, k):
    datasetsize = dataset.shape[0]    #shape[0] 读取行数
    diffmax = tile(inx, (datasetsize, 1)) - dataset #tile 对inx矩阵行复制datasetsize次，列复制1次
    sqdiffmax = diffmax**2 
    sqdistances = sqdiffmax.sum(axis=1) #sum()全部相加求和，sum（axis=0）按列求和， sum(axis=1),按行求和
    distances = sqdistances**0.5
    sortdistances = distances.argsort() #从小到大排序，返回索引值
    classcount = {}
    for i in range(k):
        votelabel = labels[sortdistances[i]]
        classcount[votelabel] = classcount.get(votelabel,0) + 1 #不存在返回0，存在labels对应的count+1
    #items()返回键值元组对，itemgetter()返回进行比较的第几个域，True降序排列。
    sortedclasscount = sorted(classcount.items(),key=operator.itemgetter(1),reverse=True)
    #返回对应的labels
    return sortedclasscount[0][0]

#输入文件切割转换成矩阵    
def file2matrix(filename):
    file = open(filename)
    arraylines = file.readlines()
    numoflines = len(arraylines)
    returnmatrix = zeros((numoflines, 3))
    classlabel = []
    index = 0
    for line in arraylines:
        line = line.strip() #移除头尾字符，default为空格
        listfromline = line.split()
        returnmatrix[index,:]=listfromline[0:3]
        classlabel.append(int(listfromline[-1]))
        index = index + 1
    return returnmatrix,classlabel

##数据归一化处理#    
def autoNum(dataset):
    minVal = dataset.min(0) #min(0)可以从每一列中选取最小值
    maxVal = dataset.max(0)
    ranges  = maxVal - minVal
    normdataset = zeros(shape(dataset))
    num = dataset.shape[0]
    normdataset = dataset - tile(minVal, (num,1))
    normdataset = normdataset/tile(ranges,(num,1))
    return normdataset,ranges,minVal
    
#测试代码
def testcode():
    hoRatio = 0.1
    dataset,labels = file2matrix('datingtestset.txt')
    normMatrix,ranges,minVal = autoNum(dataset)
    num = normMatrix.shape[0]
    numTestVecs = int(num*hoRatio)
    errorCount = 0.0
    for j in range(numTestVecs):
        classfy1 = classfy0(normMatrix[j,:],normMatrix[numTestVecs:num,:],labels[numTestVecs:num],3)
        print("the classfy0 come back with %d,and the real answer is %d" % (classfy1,labels[j]))
        if (classfy1 != labels[j]):
            errorCount += 1.0
    print ("the toral error rate is %f" % (errorCount/float(numTestVecs)))
    
#图像转换成向量
def img2vector(filename):
    img_vector = zeros((1,1024))
    file = open(filename)
    for i in range(32):
        lineStr = file.readline()
        for j in range(32):
            img_vector[0,32*i+j] = int(lineStr[j])
    return img_vector
    
#手写数字识别系统测试代码
def handwritingClassTest():
    hwLabels = []
    trainingFilesList = listdir('trainingDigits')
    num = len(trainingFilesList)
    trainingMat = zeros((num,1024))
    for i in range(num):
        fileNameStr = trainingFilesList[i]
        fileStr = fileNameStr.split('.')[0]
        classNumStr = int(fileStr.split('_')[0])
        hwLabels.append(classNumStr)
        trainingMat[i,:] = img2vector('trainingDigits/%s' % fileNameStr)
    testFileList = listdir('testDigits')
    errorCount = 0.0
    mtest = len(testFileList)
    for i in range(mtest):
        fileNameStr = testFileList[i]
        fileStr = fileNameStr.split('.')[0]
        classNumStr = int(fileStr.split('_')[0])
        vectorUnderTest = img2vector('testDigits/%s' % fileNameStr)
        classfyResult = classfy0(vectorUnderTest,trainingMat,hwLabels,3)
        print("the classfy0 come back with %d,and the real answer is %d" % (classfyResult,classNumStr))
        if(classfyResult != classNumStr):
            errorCount += 1.0
    print("\nthe total number of errors is :%d" % errorCount)
    print("\nthe total error rate is :%f" % (errorCount/float(mtest)))   