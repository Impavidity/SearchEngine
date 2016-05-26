#!/usr/bin/python
import os
import json
import scipy.sparse
import scipy.linalg
import numpy as np
import myTokenize
import utils

"""For boolean query"""
term2tid = {}
invertedIndex = [] # element form: {'docFreq':0, 'docIDs':[]}

"""For vector space"""
tf=[]
	
docID2Name = {}

def buildIndex():
	
	filenames = [x for x in os.listdir('tmp/doc') if x[0] != '.']
	cur_tid = 0
	cur_docID = 0

	for name in filenames:

		doc = open("tmp/doc/"+name, "r")
		docID2Name[cur_docID] = name
		
		contents = doc.readlines()
		tokens = myTokenize.tokenize(contents[0][7:-1])
		tokens.extend(tokens)
	
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
		cur_docID += 1
	

	W = scipy.sparse.lil_matrix((cur_tid, cur_docID))

	for tid in range(cur_tid):
		logtf = 1 + np.log10(np.array(tf[tid]))
		cosNorm = np.sqrt(np.sum(logtf * logtf))

		logtf = logtf / cosNorm
		W[tid, invertedIndex[tid]['docIDs']] = logtf
	
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
	
	docID2NameFile = open("docID2Name.json", "w")
	json.dump(docID2Name, docID2NameFile)
	docID2NameFile.close()
	
	utils.save_sparse_csr("weightMatrix", W)
	
buildIndex()




	
	


	