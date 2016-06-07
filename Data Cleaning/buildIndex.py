#!/usr/bin/python
import os
import json
import scipy.sparse
import scipy.linalg
import numpy as np
import myTokenize
import utils


def buildIndex():
	"""For boolean query"""
	term2tid = {}
	invertedIndex = [] # element form: {'docFreq':0, 'docIDs':[]}

	"""For vector space"""
	tf=[]
	
	docID2NameFile = open("docID2Name.json", "r")
	docID2Name = json.load(docID2NameFile)
	docID2NameFile.close()
	
	total_docs = len(docID2Name)
		
	cur_tid = 0
	
	for cur_docID in xrange(total_docs):
		name = docID2Name[str(cur_docID)]
		doc = open("tmp/doc/"+name, "r")
		
		contents = doc.readlines()
		tokens = myTokenize.tokenize(contents[0][7:-1])
		tokens.extend(tokens) # add the title tokens twice, consider comment it?
	
		tokens.extend(myTokenize.tokenize(contents[1][9:-1]))
		
		for token in tokens:
			if token not in term2tid:
				term2tid[token] = cur_tid
				invertedIndex.append({
#					'term':token, 
					'docFreq':0, 
					'docIDs':[]})
				
				tf.append([])

				cur_tid = cur_tid + 1
							
			tid = term2tid[token]
			if( len(invertedIndex[tid]['docIDs'])==0 or invertedIndex[tid]['docIDs'][-1] != cur_docID):
				invertedIndex[tid]['docIDs'].append(cur_docID)
				invertedIndex[tid]['docFreq'] = invertedIndex[tid]['docFreq'] + 1
				tf[tid].append(1)
			else:
				tf[tid][-1] = tf[tid][-1] + 1
		doc.close()
	
	idf = np.zeros(cur_tid, dtype = np.float64)
	W = scipy.sparse.lil_matrix((cur_tid, total_docs))

	for tid in xrange(cur_tid):
		logtf = 1 + np.log10(np.array(tf[tid]))
		cosNorm = np.sqrt(np.sum(logtf * logtf))

		logtf = logtf / cosNorm
		W[tid, invertedIndex[tid]['docIDs']] = logtf
		
		idf[tid] = np.log10(total_docs * 1.0 / invertedIndex[tid]['docFreq'])
		
	
	W = scipy.sparse.csr_matrix(W)
		
#	terms = sorted([key for key in term2tid])
#	termsFile = open("terms.json", "w")
#	json.dump(terms, termsFile)
#	termsFile.close()
		
	term2tidFile = open("term2tid.json", "w")
	json.dump(term2tid, term2tidFile)
	term2tidFile.close()

	indexFile = open("invertedIndex.json", "w")
	json.dump(invertedIndex, indexFile)
	indexFile.close()
	
	np.save('idf.npy', idf)
	
	utils.save_sparse_csr("weightMatrix", W)
	
buildIndex()




	
	


	