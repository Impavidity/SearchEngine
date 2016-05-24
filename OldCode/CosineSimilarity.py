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
import math


def Cosine(q,doc):
	f = 0
	q_pointer = 0
	doc_pointer = 0
	while (q_pointer<len(q) and doc_pointer<len(doc)):
		if q[q_pointer][0] == doc[doc_pointer][0]:
			f = f + q[q_pointer][1]*doc[doc_pointer][1]
			q_pointer += 1
			doc_pointer += 1
		else: 
			if q[q_pointer][0]<doc[doc_pointer][0]:
				q_pointer += 1
			else:
				doc_pointer += 1
	return f

def CosineSimilarity(q,dlist,d):
	#print "calc cos"
	Rate = {}
	n = 0
	for i in dlist:
		doc = d[i]
		cos = Cosine(q,doc)
		#print n,":",cos
		Rate[i] = cos
		n += 1
	#print Rate
	anslist = sorted(Rate.iteritems(), key = lambda d:d[1], reverse = True)

	count = 0
	for item in anslist:
		if count >20:
			break
		if item[1] == 0:
			break
		print item
		count += 1

	return anslist

'''
def AdjustedCosine(q,doc):
	f = 0
	xy= 0 
	x2 = 0
	y2 = 0
	q_pointer = 0
	doc_pointer = 0
	while (q_pointer<len(q) and doc_pointer<len(doc)):
		if q[q_pointer][0] == doc[doc_pointer][0]:
			avg = (q[q_pointer][1]+doc[doc_pointer][1])/2
			avg = 0
			xy = xy + (q[q_pointer][1]-avg)*(doc[doc_pointer][1]-avg)
			x2 = x2 + (q[q_pointer][1]-avg)*(q[q_pointer][1]-avg)
			y2 = y2 + (doc[doc_pointer][1]-avg)*(doc[doc_pointer][1]-avg)
			q_pointer += 1
			doc_pointer += 1
		else: 
			if q[q_pointer][0]<doc[doc_pointer][0]:
				q_pointer += 1
			else:
				doc_pointer += 1
	if x2==0 or y2==0:
		return 0
	f = xy/math.sqrt(x2)/math.sqrt(y2)
	return f

def AdjustedCosineSimilarity(q,d):
	Rate = {}
	n = 0
	for doc in d:
		cos = AdjustedCosine(q,doc)
		#print cos
		Rate[n] = cos
		n += 1

	anslist = sorted(Rate.iteritems(), key = lambda d:d[1], reverse = True)
	#print anslist
	count = 0
	for item in anslist:
		if count >20:
			break
		if item[1] == 0:
			break
		print item
		count += 1
'''
def CosineQuery(query,PostingList,dictionary,corpus_tfidf,tfidf,word2id):

	query_tokens = Tokenize([query])
	query_filtered = Filter(query_tokens)
	#query_without_pun = RemovePunctuation(query_filtered)
	query_Lemmatized = Lemmatizer(query_tokens)
	print "basic process finished"
	q = query_Lemmatized[0]
	#revised
	i = 0
	if (len(q)<10):
		while i<len(q):
			q[i] = Revised(q[i],word2id)
			i+=1
	print q
	dlist=set([])
	for w in q:
		if w in word2id:
			if str(word2id[w]) in PostingList:
				dlist |= set(PostingList[str(word2id[w])])
	print dlist
	q_bow = dictionary.doc2bow(q)
	q_bow_dfidf = tfidf[q_bow]
	#print q_bow
	return CosineSimilarity(q_bow_dfidf, dlist,corpus_tfidf)
	
'''
def AdjustedCosineQuery(query,dictionary,corpus_tfidf_without_normalization,tfidf):

	query_tokens = Tokenize([query])
	query_filtered = Filter(query_tokens)
	query_without_pun = RemovePunctuation(query_filtered)
	query_Lemmatized = Lemmatizer(query_without_pun)
	print "basic process finished"
	q = query_Lemmatized[0]
	#revised
	i = 0
	while i<len(q):
		q[i] = Revised(q[i])
		i+=1
	q_bow = dictionary.doc2bow(q)
	q_bow_dfidf = tfidf[q_bow]
	#print q_bow
	AdjustedCosineSimilarity(q_bow_dfidf, corpus_tfidf_without_normalization)

'''