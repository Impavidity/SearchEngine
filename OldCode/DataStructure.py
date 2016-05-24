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

BOUNDERY = 20 # 1st layer & 2nd layer

def ConvertIntoDict(s):
	print "convert into dictionary (id,word)"
	dictionary = corpora.Dictionary(s)
	print "convert into dictionary (id,word) finish"
	print "save dictionary begins"
	dictionary.save('tmp/dict')
	print "save dictionary ends"
	print "Frequent matrix process begins"
	corpus = [dictionary.doc2bow(document, allow_update = True) for document in s]
	print "Frequent matrix process ends"
	print "save the matrix begins"
	corpora.MmCorpus.serialize('tmp/corpus.mm',corpus)
	print "save the matrix ends"
	return corpus


def MakeDictionaryWord2Id():
	print "Make dictionary Word to id"
	dictionary = corpora.Dictionary.load('tmp/dict')
	#print dictionary
	#items = dictionary.items()
	word2id = {}
	num = 0
	for item in dictionary.iteritems():	
		word2id[item[1]] = item[0]
	word2id_file = open("tmp/Word2Id","w")
	word2id_file.write(json.dumps(word2id, sort_keys = True, indent =4 ))
	print "save the word to id dictionary"
	#print json.dumps(word2id, sort_keys = True, indent =2 )
	#print dictionary.get(0)
	#print word2id["diff"]


def ChangeCorpusToMapping():
	print "Mapping corpus word frequent"
	corpus = corpora.MmCorpus('tmp/corpus.mm')
	Frequent = []
	for document in corpus:
		add = {}
		for item in document:
			add[item[0]] = item[1]
		Frequent.append(add)

	frequent = open("tmp/Frequent","w")
	frequent.write(json.dumps(Frequent, sort_keys = True, indent = 4))
	print "Mapping finish"

def MakePostingList():
	print "make posting list just with document num"
	corpus = corpora.MmCorpus('tmp/corpus.mm')
	# with open("tmp/Frequent") as frequent_file:
	# 	Frequent = json.load(frequent_file)
	PostingList = {}
	First_PostingList = {}
	Sec_PostingList = {}
	DocNum = 0
	for document in corpus:
		for item in document:
			if (item[1]>0):
				if not (item[0] in PostingList):
					PostingList[item[0]] = [DocNum]
				else:
					PostingList[item[0]].append(DocNum)
				
				if item[1] > BOUNDERY:
					if not (item[0] in First_PostingList):
						First_PostingList[item[0]] = [DocNum]
					else:
						First_PostingList[item[0]].append(DocNum)
				else:
					if not (item[0] in Sec_PostingList):
						Sec_PostingList[item[0]] = [DocNum]
					else:
						Sec_PostingList[item[0]].append(DocNum)

		DocNum = DocNum + 1
	#print PostingList
	#print len(corpus[0])
	postinglist = open("tmp/PostingList","w")
	postinglist.write(json.dumps(PostingList, sort_keys = True, indent = 4))
	First_postinglist = open("tmp/First_PostingList","w")
	First_postinglist.write(json.dumps(First_PostingList, sort_keys = True, indent = 4))
	Sec_postinglist = open("tmp/Sec_PostingList","w")
	Sec_postinglist.write(json.dumps(Sec_PostingList, sort_keys = True, indent = 4))
	print "Posting list build finish"



def wlocal_ours(freq):
	return (1 + freq) * 1.2

def GetTfidf():
	print "Train tfidf model"
	corpus = corpora.MmCorpus('tmp/corpus.mm')
	tfidf = models.TfidfModel(corpus,wlocal=wlocal_ours)
	print "train finish"
	print "make corpus to vector"
	corpus_tfidf = tfidf[corpus]
	print "make corpus to vector finish"
	
	tfidf.save('tmp/tfidf_model')

	corpus_tfidf_file = open("tmp/corpus_tfidf","w")
	corpus_tfidf_file.write(json.dumps(list(corpus_tfidf), sort_keys = True, indent = 4))
	print "save the tfidf model and corpus tfidf"
