#!/usr/bin/python
import numpy as np
import scipy.sparse

docCount = 10788

def showDoc(name):
	doc = open("tmp/doc/"+name, "r")
	contents = doc.readlines()
	title = contents[0]
	print title
	passage = contents[1][9:]
	print passage
	doc.close()
"""
showers: [1, 10388, 11536, 15043, 19262, 6114, 6142, 6153, 8705]
showers AND rice: [11536, 6114, 6153]
"""	

def save_sparse_csr(filename,array):
	np.savez(filename, 
		data = array.data ,
		indices = array.indices,
		indptr = array.indptr, 
		shape = array.shape )

def load_sparse_csr(filename):
	loader = np.load(filename)
	return scipy.sparse.csr_matrix(
	(  loader['data'], loader['indices'], loader['indptr']),
	shape = loader['shape'] )
