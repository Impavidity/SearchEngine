#!/usr/bin/python
import json
import scipy.sparse
import scipy.linalg
import numpy as np
import myTokenize
import utils
from collections import Counter

def initCosSimQuery():
	term2tidFile = open("term2tid.json", "r")
	indexFile = open("invertedIndex.json", "r")
	global W
	W = utils.load_sparse_csr("weightMatrix.npz")
	
	global term2id
	term2id = json.load(term2tidFile)
	global invertedIndex
	invertedIndex = json.load(indexFile)
	
	term2tidFile.close()
	indexFile.close()
	
	global docCount
	docCount = np.size(W, 1)

initCosSimQuery()	
	

def cosSimQuery(query, k):
	queryTokens = myTokenize.tokenize(query)
	queryTokensCounter = Counter(queryTokens)
	
	scores = np.zeros(docCount, dtype = np.float64)
	
	for queryToken in queryTokensCounter:
		tid = term2id[queryToken]
		for docID in range(docCount):
			scores[docID] += W[tid, docID] \
			 * np.log10(docCount * 1.0 / invertedIndex[tid]['docFreq']) \
			 * (1 + np.log10(queryTokensCounter[queryToken]))
	
	resDocIDs = np.argsort(scores)[-k:][::-1]
	resScores = scores[resDocIDs]
	
	print "correspondent scores: ", resScores
	return resDocIDs
			
		
		