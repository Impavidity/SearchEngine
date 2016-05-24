#!/usr/bin/python
# -*- coding: utf-8 -*-
from gensim import corpora, models, similarities
from BasicProcess import *
from revised import *


def LDAModelTrain():
	print "begin to train LDA model"
	corpus = corpora.MmCorpus('tmp/corpus.mm')
	dictionary = corpora.Dictionary.load('tmp/dict')
	lda = models.ldamodel.LdaModel(corpus=corpus, id2word=dictionary, num_topics=60)
	lda.save('tmp/LdaModel')
	print "train Finished and save finished"






def LDAQuery(query,dictionary,lda,word2id):
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
	q_bow = dictionary.doc2bow(q)
	topic = lda[q_bow]
	print "lda:",topic

	print lda.print_topic(int(topic[0][0]))
	print lda.print_topics()

	return 