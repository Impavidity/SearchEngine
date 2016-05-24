#!/usr/bin/python
# -*- coding: utf-8 -*-
from nltk.tokenize import word_tokenize
from nltk import collocations
import os
from nltk.corpus import stopwords
from nltk.stem.lancaster import LancasterStemmer
from nltk.stem import WordNetLemmatizer
from gensim import corpora, models, similarities
import logging
import pprint
import json
from nltk.corpus import wordnet
import re
WordNetLemmatizer = WordNetLemmatizer()
LancasterStemmer = LancasterStemmer()
english_stopwords = stopwords.words('english')
import nltk
prog_num = re.compile("\d.*")
english_punctuations = [',','.',':','?',';','(',')','[',']','&','!','*','@','#','$','%','...']

stop_words = nltk.corpus.stopwords.words('english') + [
'--',
u'\u2014',
u'\u2019',
u'\u201d',
'"',
'-',
'}',
'{',
] + english_punctuations


def Tokenize(s):
	print "change the file into token"
	#text_tokenized = [[word.lower().strip(u'\u201c\u201d\u2018') for word in word_tokenize(document)] for document in s]
	text_tokenized = [[word.lower().strip(u'\u201c\u201d') for word in word_tokenize(document) if not re.match(prog_num, word)] for document in s]
	#print text_tokenized
	return text_tokenized

def Filter(s):
	print "remove the stop word"
	text_filtered = [[word.strip(',.') for word in document if word not in stop_words] for document in s]
	return text_filtered

# def RemovePunctuation(s):
# 	print "remove the punctuation"
# 	text_without_pun = [[word for word in document if not word in english_punctuations] for document in s]
# 	return text_without_pun

def Stemmer(s):
	print "stemmer"
	text_stemmed = [[LancasterStemmer.stem(word) for word in document] for document in s]
	return text_stemmed

def Lemmatizer(s):
	print "Lemmatizer"
	text_lemmatized = [[WordNetLemmatizer.lemmatize(word) for word in document] for document in s]
	return text_lemmatized


def RemoveTermAppearOnce(s):
	print "remove the term appear once"
	all_stems = sum(s,[])
	stems_once = set(stem for stem in set(all_stems) if all_stems.count(stem) == 1)
	texts = [[stem for stem in document if stem not in stems_once] for document in s]
	return texts


def phrase_list(filename):
	article = open(filename,'r').readlines()
	try:
		data = article[2:]
		content = data[0].decode("utf-8")[:-1]
		for paragraph in data[1:]:
				content = content + " " + paragraph.decode("utf-8")[:-1]
	except:
		return []

	txt = content
	sentences = [s for s in nltk.tokenize.sent_tokenize(txt)]
	normalized_sentences = [s.lower() for s in sentences]

	words = [w for sentence in normalized_sentences for w in nltk.tokenize.word_tokenize(sentence) if w not in stop_words and not re.match(prog_num, w)]
	words = [w.strip(u'\u201c\u201d\u2018') for w in words]
	words = [w.strip(',.') for w in words]
	#print words
	#words = Lemmatizer([words])
	#print words


	bigram_measures = collocations.BigramAssocMeasures()
	bigram_finder = collocations.BigramCollocationFinder.from_words(words)
	#bigram_finder.apply_freq_filter(BIGRAM_FILTER)

	threshold = min(int(0.05*len(words)), 100)
	phrase = []
	for bigram in bigram_finder.score_ngrams(bigram_measures.raw_freq)[:threshold]:
		phrase.append(bigram[0])

	return phrase
