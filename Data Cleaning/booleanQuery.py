#!/usr/bin/python
#import time
import json
import os
import tokenize
from porter import PorterStemmer
import utils

def inverseList(termDict):
	"""NOT 1 posting list--> return a list"""
	return {
#		'term':'', 
		'docFreq':wholeLen - termDict['docFreq'], 
		'docIDs':[x for x in wholeList if x not in termDict['docIDs']]
		}
	
def disjunct2Lists(l1, l2):
	"""OR 2 posting lists --> return a list"""
	p1 = p2 = 0
	resultDocs = []
	
	while p1 < len(l1) and p2 < len(l2):
		if l1[p1] == l2[p2]:
			resultDocs.append(l1[p1])
			p1 = p1 + 1
			p2 = p2 + 1
		elif (l1[p1]) < (l2[p2]):
			resultDocs.append(l1[p1])
			p1 = p1 + 1
		else:
			resultDocs.append(l2[p2])
			p2 = p2 + 1
			
	if p1 < len(l1):
		resultDocs.extend(l1[p1:])
	elif p2 < len(l2):
		resultDocs.extend(l2[p2:])
		
	return resultDocs

def intersect2Lists(l1, l2):
	"""AND 2 posting lists --> return a list"""
	p1 = p2 = 0
	resultDocs = []
	while p1 < len(l1) and p2 < len(l2):
		if l1[p1] == l2[p2]:
			resultDocs.append(l1[p1])
			p1 = p1 + 1
			p2 = p2 + 1
		elif (l1[p1]) < (l2[p2]):
			p1 = p1 + 1
		else:
			p2 = p2 + 1
	return resultDocs
	
def intersect(postingLists):
	"""AND several posting lists --> return a list"""
	sortedPostingLists = sorted(postingLists, cmp=lambda l1, l2: cmp(l1['docFreq'], l2['docFreq']))
	resultDocs = sortedPostingLists[0]['docIDs']

	for i in xrange(1, len(sortedPostingLists)):
		resultDocs = intersect2Lists(resultDocs, sortedPostingLists[i]['docIDs'])
	return resultDocs	
	
def disjunct(postingLists):
	"""OR several posting lists, and return expect length --> return a dict"""	
	resultDocs = postingLists[0]['docIDs']

	for i in xrange(1, len(postingLists)):
		resultDocs = disjunct2Lists(resultDocs, postingLists[i]['docIDs'])
		
	return {
#		'term': '',
		'docFreq': sum([pl['docFreq'] for pl in postingLists]),
		'docIDs': resultDocs
		}

def parseOR(ORpart):
	ORpart = ORpart.strip(' ')
	isNOTPart = False
	isSTOPWORD = False
	
	if "NOT" in ORpart:
		ORpart = ORpart[4:]
		isNOTPart = True
		
	ORpartStemed = ORpart.strip("".join(tokenize.strip_punctuations)).lower()
	if ORpartStemed in tokenize.stop_words:
		print "Term: " + ORpart + " is a stop word. We assume this word exists in all documents."
		isSTOPWORD = True
	else:
		ORpartStemed = p.stem(ORpartStemed, 0, len(ORpartStemed)-1)
			
		
	if isSTOPWORD or (ORpartStemed not in term2id):
		print "Term: " + ORpart + " is not in the dictionary, we treat this term as a stop word!"
		if isNOTPart:
			return {
#				'term':'', 
				'docFreq': 0, 
				'docIDs':[]}
		else:
			return {
#				'term':'', 
				'docFreq': wholeLen, 
				'docIDs':wholeList}
 	else:
		if isNOTPart:
			return inverseList(invertedIndex[term2id[ORpartStemed]])
		else:
			return invertedIndex[term2id[ORpartStemed]]		

	
def parseAND(ANDpart):
	ORparts = [x for x in ANDpart.strip(' ').split("OR") if x != '']
	postingListsToOR = [parseOR(ORpart) for ORpart in ORparts]
#	print "postingListsToOR"
#	print postingListsToOR
#	print "disjunct(postingListsToOR)"
#	print disjunct(postingListsToOR)
	return disjunct(postingListsToOR)
	
	
def initBooleanQuery():
	#start_time = time.time()
	term2tidFile = open("term2tid.json", "r")
	indexFile = open("invertedIndex.json", "r")

	global term2id
	term2id = json.load(term2tidFile)
	global invertedIndex
	invertedIndex = json.load(indexFile)
	#print("--- %s seconds ---" % (time.time() - start_time))
	
	term2tidFile.close()
	indexFile.close()

	global wholeList
	wholeList = range(utils.docCount)
	global wholeLen
	wholeLen = utils.docCount
	global p
	p = PorterStemmer()
	
	
def booleanQuery(query):

	ANDparts = [x for x in query.strip(' ').split("AND") if x != '']
	
	postingListsToAND = [parseAND(ANDpart) for ANDpart in ANDparts]
#	print "postingListsToAND"
#	print postingListsToAND
	resultDocIDs = intersect(postingListsToAND)

	return resultDocIDs



