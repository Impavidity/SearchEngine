#!/usr/bin/python
import json
import utils
import booleanQuery
import cosineSimilarityQuery
from time import time

if __name__ == '__main__':
	
	docID2NameFile = open("docID2Name.json", "r")
	docID2Name = json.load(docID2NameFile)
	docID2NameFile.close()
	
	booleanQuery.initBooleanQuery()
	cosineSimilarityQuery.initCosSimQuery()
	
	print("Welcome to the IR world!")
	
	a=1
	while a:
		a-=1
		choice = input("Choose a search method: (0:boolean | 1:cos similarity)\n")
#		choice = 1
		if choice == 0:
			print "The form of a boolean query should be: [X AND Y AND NOT Z ... OR P OR Q ...]"
			print "with priority: NOT > AND > OR"
			print "For boolean query, please do not input punctuation!"

			query = raw_input("input your boolean query: \n")
			if len(query.strip(' ')) == 0:
				print "query cannot be empty"
			t = time()
			res = booleanQuery.booleanQuery(query)
			t = time() - t
			
		elif choice == 1:
			query = raw_input("input your query: \n")
			if len(query.strip(' ')) == 0:
				print "query cannot be empty"
						
			k = input("input the number of results you want: \n")
#			query = "European showers Greece agricultural"
#			k = 10
			t = time()
			r = cosineSimilarityQuery.cosSimQuery(query, k)
			t = time() - t
		
		res = [docID2Name[str(docID)] for docID in r[0]]
		print "resultDocs: ", res
		print "resultScores: ", r[1]
		print "search time: ", t