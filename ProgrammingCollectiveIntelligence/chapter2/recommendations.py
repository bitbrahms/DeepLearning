#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-12-19 09:47:19
# @Author  : mannyxu (beilixumeng@163.com)

from math import sqrt

critics={'Lisa Rose': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.5,
 'Just My Luck': 3.0, 'Superman Returns': 3.5, 'You, Me and Dupree': 2.5, 
 'The Night Listener': 3.0},
'Gene Seymour': {'Lady in the Water': 3.0, 'Snakes on a Plane': 3.5, 
 'Just My Luck': 1.5, 'Superman Returns': 5.0, 'The Night Listener': 3.0, 
 'You, Me and Dupree': 3.5}, 
'Michael Phillips': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.0,
 'Superman Returns': 3.5, 'The Night Listener': 4.0},
'Claudia Puig': {'Snakes on a Plane': 3.5, 'Just My Luck': 3.0,
 'The Night Listener': 4.5, 'Superman Returns': 4.0, 
 'You, Me and Dupree': 2.5},
'Mick LaSalle': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0, 
 'Just My Luck': 2.0, 'Superman Returns': 3.0, 'The Night Listener': 3.0,
 'You, Me and Dupree': 2.0}, 
'Jack Matthews': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
 'The Night Listener': 3.0, 'Superman Returns': 5.0, 'You, Me and Dupree': 3.5},
'Toby': {'Snakes on a Plane':4.5,'You, Me and Dupree':1.0,'Superman Returns':4.0}}

#欧几里得评价
def sim_distance(prefs,person1,person2):
	si={}
	for item in prefs[person1]:
		if item in prefs[person2]:
			si[item]=1

	if(len(si) == 0):
		return 0
	sum_of_squres = sum([pow((prefs[person1][item] - prefs[person2][item]),2)\
		for item in si])

	return(1/(1+sqrt(sum_of_squres)))

#皮尔逊相关评价
def sim_person(prefs,person1,person2):
	si={}
	for item in prefs[person1]:
		if item in prefs[person2]:
			si[item]=1
	if len(si)==0:
		return(1)
	sum1 = sum([prefs[person1][item] for item in si])
	sum2 = sum([prefs[person2][item] for item in si])
	sum1sq = sum([pow(prefs[person1][item],2) for item in si])
	sum2sq = sum([pow(prefs[person2][item],2) for item in si])
	pSum = sum([prefs[person1][item]*prefs[person2][item] for item in si])
	n = len(si)
	num = pSum - sum1*sum2/n
	den = sqrt((sum1sq - pow(sum1,2)/n)*(sum2sq - pow(sum2,2)/n))
	if den ==0:
		return(0)
	return(num/den)

#最匹配
def topmatch(prefs,person,n=5):
	scores = [(sim_person(prefs, person, other),other) for other in prefs if other!=person]
	scores.sort()
	scores.reverse()
	return(scores[0:n])

def get_recommendations(prefs,person):
	total = {}
	simSum = {}
	for other in prefs:
		if other == person:
			continue
		sim = sim_distance(prefs, person, other)
		if sim <= 0:
			continue
		for item in prefs[other]:
			if item not in prefs[person] or prefs[person][item] == 0:
				total.setdefault(item,0)
				total[item] += prefs[other][item]*sim
				simSum.setdefault(item,0)
				simSum[item] += sim
		ranking = [(total/simSum[item],item) for item,total in total.items()]
		ranking.sort()
		ranking.reverse()
		return(ranking)

def transformPrefs(prefs):
	result = {}
	for person in prefs:
		for item in prefs[person]:
			result.setdefault(item, {})
			result[item][person] = prefs[person][item]
	return(result)

def calculateSimilarItems(prefs,n=10):
	result={}
	itemsPrefs=transformPrefs(prefs)
	num =0
	for item in itemsPrefs:
		num += 1
		if num%100==0:
			print("%d / %d" % (num,len(itemsPrefs)))
		scores =  topmatch(itemsPrefs,item,n=n)
		result[item]=scores
	return(result)

def get_recommendationsItems(prefs,itemsSet,user):
	userrating = prefs[user]
	scores = {}
	totalSim = {}

	for item,rating in userrating.items():
		for similarity,item2 in itemsSet[item]:
			if item2 in userrating:
				continue
			scores.setdefault(item2,0)
			scores[item2] += similarity*rating
			totalSim.setdefault(item2,0)
			totalSim[item2] += similarity

	ranking = [(score/totalSim[item],item) for item,score in scores.items()]

	ranking.sort(reverse=True)
	return(ranking)

def loadMovies(path='../data/ml-100k/'):
	movies = {}
	f = open(path+'u.item','r')
	for line in f.readlines():
		print(line)
		(id,title)=line.split('|')[0:2]
		movies[id]=title
	'''
	prefs = {}
	f = open(path+'u.data','r')
	for line in f.readlines():
		print(line)
		(user,id,rating,ts)=line.split('\t')
		prefs.setdefault(user,{})
		prefs[user][movies[id]]=float(rating)
	return(prefs)

prefs = loadMovies()
print(prefs['87'])

print(get_recommendations(prefs,'87')[0:30])
'''