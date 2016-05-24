#!/usr/bin/python
# -*- coding: utf-8 -*-

from nltk.tokenize import word_tokenize
import os
from nltk.corpus import stopwords
from nltk.stem.lancaster import LancasterStemmer
from nltk.stem import WordNetLemmatizer
from gensim import corpora, models, similarities
import logging
import pprint
import json
from nltk.corpus import wordnet
from revised import *
from BasicProcess import *
'''
logging.basicConfig(formate='%(asctime)s:%(levelname)s:%(message)s', level=logging.INFO)
WordNetLemmatizer = WordNetLemmatizer()
LancasterStemmer = LancasterStemmer()
english_stopwords = stopwords.words('english')
english_punctuations = [',','.',':','?',';','(',')','[',']','&','!','*','@','#','$','%','...']
'''



def BooleanQuery(s,word2id,Frequent,PostingList,DocNum = 9663):



	query_tokens = Tokenize([s])
	query_filtered = Filter(query_tokens)
	#query_without_pun = RemovePunctuation(query_filtered)
	query_Lemmatized = Lemmatizer(query_tokens)
	print "finished Basic query process"
	#print query_Lemmatized
	#print DocNum
	andansset = set(range(0,DocNum))
	oransset = set([])
	andfrequent = {}
	orfrequent = {}
	for query in query_Lemmatized:
		for item in query:
			if not item in word2id:
				item = Revised(item,word2id)
			if item in word2id:
				andansset = andansset & set(PostingList[str(word2id[item])])
				oransset = oransset | set(PostingList[str(word2id[item])])

			
	for query in query_Lemmatized:
		for item in query:
			if not item in word2id:
				item = Revised(item,word2id)
			if item in word2id:
				for document in andansset:
					if document in andfrequent:
						andfrequent[document] += Frequent[document][str(word2id[item])] 
					else:
						andfrequent[document] = Frequent[document][str(word2id[item])]
				for document in oransset:
					if not document in andansset:
						if word2id[item] in Frequent[document]: 
							if document in orfrequent:
								orfrequent[document] += Frequent[document][str(word2id[item])]
							else:
								orfrequent[document] = Frequent[document][str(word2id[item])]

	#print andfrequent
	#print orfrequent					

	ans1 = sorted(andfrequent.iteritems(), key = lambda d:d[1], reverse = True)
	ans2 = sorted(orfrequent.iteritems(), key = lambda d:d[1], reverse = True)

	ans = ans1+ans2

	count = 0
	for item in ans:
		print item
		if count > 20:
			break
		count += 1
	
	return ans
	

	