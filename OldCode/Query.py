#!/usr/bin/python
# -*- coding: utf-8 -*-
from Boolean import *
from CosineSimilarity import *
from LSIModel import *
from LDAModel import *
from PivotFrequent import *
from API import *
from Tired import *

import sys
from gensim import corpora, models, similarities

def WordSearch(op,query,word2id,Frequent,PostingList,dictionary,corpus_tfidf,tfidf,lsi,lda,index,corpus_tfidf2):
	if op == "1":
		ans = BooleanQuery(query,word2id,Frequent,PostingList)
		WordSearchFileProcess(ans)
	if op == "2":
		ans = CosineQuery(query,PostingList,dictionary,corpus_tfidf,tfidf,word2id)
		WordSearchFileProcess(ans)
	if op == "3":
		ans = LSIQuery(query,dictionary,lsi,index,word2id)
		WordSearchFileProcess(ans)
	if op == "4":
		ans = PivotCosineQuery(query,corpus_tfidf2,PostingList,dictionary,word2id)
		WordSearchFileProcess(ans)

def ArticleSearch(op,query,dictionary,corpus_tfidf,tfidf,word2id):
	if op == "1":
		summary =  summraize(query)
		q = summary[0]+" "+summary[1]
		ans = CosineQuery(q,PostingList,dictionary,corpus_tfidf,tfidf,word2id)
		WordSearchFileProcess(ans)

def main():
	print "load file"
	with open("tmp/Word2Id") as word2id_file:
		word2id = json.load(word2id_file)
	with open("tmp/Frequent") as frequent_file:
		Frequent = json.load(frequent_file)
	with open("tmp/PostingList") as postinglist_file:
		PostingList = json.load(postinglist_file)
	dictionary = corpora.Dictionary.load('tmp/dict')
	with open("tmp/corpus_tfidf") as corpus_tfidf_file:
		corpus_tfidf = json.load(corpus_tfidf_file)
	index = similarities.docsim.MatrixSimilarity.load('tmp/LSI.index')
	lsi = models.lsimodel.LsiModel.load('tmp/LsiModel')
	tfidf = models.tfidfmodel.TfidfModel.load('tmp/tfidf_model')
	lda = models.ldamodel.LdaModel.load('tmp/LdaModel')
	with open("tmp/corpus_tfidf2") as corpus_tfidf2_file:
		corpus_tfidf2 = json.load(corpus_tfidf2_file)
	with open("tmp/First_PostingList") as First_PostingList_file:
		First_PostingList = json.load(First_PostingList_file)
	with open("tmp/Sec_PostingList") as Second_PostingList_file:
		Second_PostingList = json.load(Second_PostingList_file)



	print "load file finished"

	while (True):
		q = sys.stdin.readline()
		op = sys.stdin.readline()
		if op == "1\n":
			BooleanQuery(q,word2id,Frequent,PostingList)

		if op == "2\n":
			#print "process cosine"
			CosineQuery(q,PostingList,dictionary,corpus_tfidf,tfidf,word2id)

		if op == "3\n":
			LSIQuery(q,dictionary,lsi,index,word2id)

		if op == "4\n":
			LDAQuery(q,dictionary,lda,word2id)

		if op == "5\n":
			PivotCosineQuery(q,corpus_tfidf2,PostingList,dictionary,word2id)

		if op == "6\n":
			TiredCosineQuery(q,corpus_tfidf,PostingList,First_PostingList,Second_PostingList,dictionary,word2id)

if __name__=='__main__':
	main()