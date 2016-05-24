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


K = 100
def TiredCosine(q,doc):
	f = 0
	xy= 0 
	x2 = 0
	y2 = 0
	q_pointer=0
	doc_pointer=0
	#print "len q:",len(q),"len doc",len(doc)
	while (q_pointer<len(q) and doc_pointer<len(doc)):
		if q[q_pointer][0] == doc[doc_pointer][0]:
			#print "same word id:",q_pointer,"q word tfidf:",q[q_pointer],"doc word tfidf:",doc[doc_pointer]
			xy = xy + (q[q_pointer][1])*(doc[doc_pointer][1])
			x2 = x2 + (q[q_pointer][1])*(q[q_pointer][1])
			y2 = y2 + (doc[doc_pointer][1])*(doc[doc_pointer][1])
			q_pointer += 1
			doc_pointer += 1
		else: 
			if q[q_pointer][0]<doc[doc_pointer][0]:
				x2 = x2 + (q[q_pointer][1])*(q[q_pointer][1])
				q_pointer += 1
			else:
				y2 = y2 + (doc[doc_pointer][1])*(doc[doc_pointer][1])
				doc_pointer += 1
	if (q_pointer<len(q)):
		x2 = x2 + (q[q_pointer][1])*(q[q_pointer][1])
	if (doc_pointer<len(doc)):
		y2 = y2 + (doc[doc_pointer][1])*(doc[doc_pointer][1])
		doc_pointer += 1
	#print "xy:",xy,"x2:",x2,"y2:",y2
	if (x2==0) or (y2==0):
		return 0
	f = xy/math.sqrt(x2)/math.sqrt(y2)
	return f

def TiredCosineSimilarity(q,dlist,d):
	Rate = {}
	n = 0
	for i in dlist:
		doc = d[i]

		cos = TiredCosine(q,doc)
		#print "doc:",n,"cos:",cos
		#print cos
		Rate[i] = cos
		n += 1

	anslist = sorted(Rate.iteritems(), key = lambda d:d[1], reverse = True)
	print anslist
	i = 0
	ans = []
	while i<len(anslist):
		ans.append(anslist[i])
		i+=1
	print ans
	return ans
#	count = 0
#	for item in anslist:
#		if count >20:
#			break
#		if item[1] == 0:
#			break
#		print item
#		count += 1
	

def GetQDfidf(q,PostingList,DocNum = 3721):
	sumdf = 0
	ans = []
	#for item in q:
	#	sumdf = math.log10(float(item[1])) + sumdf + 1
	for item in q:
		t = (math.log10((item[1]))+1)
		#t = t/sumdf
		#t = t*len(q)
		#t = t/(1+0.0118*len(q))
		t = t*math.log10((DocNum)/len(PostingList[str(item[0])]))
		ans.append((item[0],t))
		print item[0],t
	return ans

def TiredCosineQuery(query,corpus_tfidf,PostingList,First_PostingList,Second_PostingList,dictionary,word2id):

	query_tokens = Tokenize([query])
	query_filtered = Filter(query_tokens)
	#query_without_pun = RemovePunctuation(query_filtered)
	query_Lemmatized = Lemmatizer(query_tokens)
	print "basic process finished"
	q = query_Lemmatized[0]
	#revised
	i = 0
	if len(q)<10:		
		while i<len(q):
			q[i] = Revised(q[i],word2id)
			i+=1

	q_bow = dictionary.doc2bow(q)
	q_bow_dfidf = GetQDfidf(q_bow,PostingList)

	first_dlist = set([])
	for w in q:
		if w in word2id:
			if str(word2id[w]) in First_PostingList:
				first_dlist |= set(First_PostingList[str(word2id[w])])
	print first_dlist
	res = TiredCosineSimilarity(q_bow_dfidf, first_dlist, corpus_tfidf)
	if(len(res) >= K):
		return res

	second_dlist = set([])
	for w in q:
		if w in word2id:
			if str(word2id[w]) in Second_PostingList:	
				second_dlist |= set(Second_PostingList[str(word2id[w])])
	print second_dlist
	res2 = TiredCosineSimilarity(q_bow_dfidf, second_dlist, corpus_tfidf)
	return (set(res) | set(res2))



	#print "q:",q_bow_dfidf
	#print q_bow


