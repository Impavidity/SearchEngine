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

def LSIModelTrain():
	print "begin to train LSI model"
	corpus = corpora.MmCorpus('tmp/corpus.mm')
	dictionary = corpora.Dictionary.load('tmp/dict')
	lsi = models.lsimodel.LsiModel(corpus=corpus, id2word=dictionary, num_topics=60)
	lsi.save('tmp/LSIModel')
	print "train Finished and save finished"
	index = similarities.docsim.MatrixSimilarity(lsi[corpus])
	index.save('tmp/LSI.index')
	print "save the index finished"






def LSIQuery(query,dictionary,lsi,index,word2id):
	query_tokens = Tokenize([query])
	query_filtered = Filter(query_tokens)
	#query_without_pun = RemovePunctuation(query_filtered)
	query_Lemmatized = Lemmatizer(query_tokens)
	print "basic process finished"
	q = query_Lemmatized[0]
	#revised
	i = 0
	while i<len(q):
		q[i] = Revised(q[i],word2id)
		i+=1
	q_bow = dictionary.doc2bow(q)
	query_lsi = lsi[q_bow]
	#print query_lsi
	sims = index[query_lsi]
	print sims
	sort_sims = sorted(enumerate(sims), key = lambda item: -item[1])
	i = 0
	while i<10:
		print sort_sims[i]
		i+=1
	return sort_sims
	