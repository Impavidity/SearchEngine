#!/usr/bin/python
import json
import scipy.sparse
import scipy.linalg
import numpy as np
import myTokenize
import utils
from collections import Counter

#term2id = {}
#invertedIndex =[]
#W = scipy.sparse.lil_matrix((1, 1))
#docCount = 0
#idf = np.array([])

def initCosSimQuery():
	
	global term2id
	global invertedIndex
	global W
	global docCount
	global termCount
	global idf
	
	term2tidFile = open("term2tid.json", "r")
	indexFile = open("invertedIndex.json", "r")
	
	term2id = json.load(term2tidFile)
	invertedIndex = json.load(indexFile)
	
	term2tidFile.close()
	indexFile.close()
	
	W = utils.load_sparse_csr("weightMatrix.npz")
	idf = np.load('idf.npy')
	docCount = np.size(W, 1)
	termCount = len(term2id)
	

def cosSimQuery(query, k):
	queryTokens = myTokenize.tokenize(query)
	queryTokensCounter = Counter(queryTokens)
	queryTidTf = {term2id[queryToken]:1 + np.log10(termCountInQUery) for (queryToken, termCountInQUery) in queryTokensCounter.items()}
	
# csr version:
	queryVec = scipy.sparse.lil_matrix((1, termCount))
	queryVec[0, queryTidTf.keys()] = queryTidTf.values()
	queryVec = scipy.sparse.csr_matrix(queryVec)
	
	scores = queryVec * W
	scores = scores.toarray()[0]

# ndarray * csr version:
#	queryVec = np.empty(termCount)
#	queryVec[queryTidTf.keys()] = queryTidTf.values()
#	scores = queryVec * W


#	scores = np.zeros(docCount, dtype = np.float64)
#	
#	for tid in queryTidTf:
#		for docID in xrange(docCount):
#			scores[docID] += W[tid, docID] \
#			 * idf[tid] \
#			 * queryTidTf[tid]
	
	resDocIDs = np.argsort(scores)[-k:][::-1]
	resScores = scores[resDocIDs]
	
#	print "correspondent scores: ", resScores
	return (resDocIDs, resScores)
			
		
		