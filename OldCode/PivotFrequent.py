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

def PivotTrain(DocNum):
	import operator
	with open("tmp/Frequent") as frequent_file:
		Frequent = json.load(frequent_file)
	with open("tmp/PostingList") as postinglist_file:
		PostingList = json.load(postinglist_file)
	print "open file finished"
	Count = 0
	corpus_tfidf2 = []
	for document in Frequent:
		sumdf = 0
		for key,value in document.iteritems():
			sumdf = math.log10(float(value)) + sumdf + 1
		for key,value in document.iteritems():
			t = (math.log10((value))+1)
			t = t/sumdf
			t = t*len(document)
			t = t/(1+0.0118*len(document))
			#print (DocNum)/len(PostingList[str(key)])
			t = t*math.log10((DocNum)/len(PostingList[str(key)]))
			if len(corpus_tfidf2)<Count+1:
				corpus_tfidf2.append([(int(key),t)])
			else:
				corpus_tfidf2[Count].append((int(key),t))
		if len(corpus_tfidf2)<Count+1:
			corpus_tfidf2.append([])
		corpus_tfidf2[Count].sort(key=lambda x:x[0])
		Count+=1

	corpus_tfidf2_file = open("tmp/corpus_tfidf2","w")
	corpus_tfidf2_file.write(json.dumps(corpus_tfidf2 , indent = 4))



def PivotCosine(q,doc):
	f = 0
	q_pointer=0
	doc_pointer=0
	#print "len q:",len(q),"len doc",len(doc)
	while (q_pointer<len(q) and doc_pointer<len(doc)):
		if q[q_pointer][0] == doc[doc_pointer][0]:
			#print "same word id:",q_pointer,"q word tfidf:",q[q_pointer],"doc word tfidf:",doc[doc_pointer]
			f = f + (q[q_pointer][1])*(doc[doc_pointer][1])
			q_pointer += 1
			doc_pointer += 1
		else: 
			if q[q_pointer][0]<doc[doc_pointer][0]:
				q_pointer += 1
			else:
				doc_pointer += 1
	return f

def PivotCosineSimilarity(q,dlist, d):
	Rate = {}
	n = 0
	for i in dlist:
		doc = d[i]
		cos = PivotCosine(q,doc)
		#print "doc:",n,"cos:",cos
		#print cos
		Rate[i] = cos
		n += 1

	anslist = sorted(Rate.iteritems(), key = lambda d:d[1], reverse = True)
	print anslist[:20]
	return anslist

def PivotCosineQuery(query,corpus_tfidf2,PostingList,dictionary,word2id):

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
	dlist=set([])
	for w in q:
		if w in word2id:
			if str(word2id[w]) in PostingList:
				dlist |= set(PostingList[str(word2id[w])])
	q_bow = dictionary.doc2bow(q)
	#q_bow_dfidf = GetQDfidf(q_bow,PostingList)
	#print "q:",q_bow_dfidf
	#print q_bow
	return PivotCosineSimilarity(q_bow, dlist,corpus_tfidf2)