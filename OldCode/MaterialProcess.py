#!/usr/bin/python
# -*- coding: utf-8 -*-
from BasicProcess import *
from DataStructure import *
from FileProcess import *
from LDAModel import *
from LSIModel import *
from PivotFrequent import *
import sys
def main():
	FileNum = int(sys.argv[1])
	FileMake(FileNum)

	documents = []
	layer1_doc = []
	layer2_doc = []
	
	dist = {}
	filenum = 0
	filename = "corpus"

	with open("data/"+filename) as f:
		corpus_doc = json.load(f)
		
	Count = 1

	content = ""
	layer1 = ""
	layer2 = ""
	

	print "File in start"

	for item in corpus_doc:

		layer1 = corpus_doc[str(Count)]["title"] + " " + corpus_doc[str(Count)]["title"] + " " + corpus_doc[str(Count)]["title"] + " " + corpus_doc[str(Count)]["title"]
		layer1 += corpus_doc[str(Count)]["description"] + " " + corpus_doc[str(Count)]["description"] 
		layer1 += corpus_doc[str(Count)]["first_para"] + " " + corpus_doc[str(Count)]["first_para"]

		layer2 = corpus_doc[str(Count)]["content"]

		content = layer1 + " " + layer2

		# layer1_doc.append(layer1)
		# layer2_doc.append(layer2)
		documents.append(content)

		Count += 1

	print "File in Finish"

	print "Basic process begins"

	documents_tokens = Tokenize(documents)
	#print documents_tokens
	#f = open("token","w")
	#f.write(json.dumps(f))
	documents_filtered = Filter(documents_tokens)
	#print documents_filtered

	#documents_without_pun = RemovePunctuation(documents_filtered)
	
	#print documents_without_pun

	#we do not do stem beccause lose to much information
	#documents_stemmed = Stemmer(documents_without_pun)
	#print documents_stemmed


	documents_Lemmatized = Lemmatizer(documents_filtered)
	#print documents_Lemmatized

	#if we need we can remove the term appear once for accuracy
	#documents_removetermappearonce = RemoveTermAppearOnce(documents_Lemmatized)
	#print documents_removetermappearonce
	# layer1_tokens = Tokenize(layer1_doc)
	# layer1_filtered = Filter(layer1_tokens)
	# layer1_lemmatized = Lemmatizer(layer1_filtered)

	# layer2_tokens = Tokenize(layer2_doc)
	# layer2_filtered = Filter(layer2_tokens)
	# layer2_lemmatized = Lemmatizer(layer2_filtered)

	print "Basic process ends"


	dictionary = ConvertIntoDict(documents_Lemmatized)
	# layer1_dict = ConvertIntoDict(layer1_lemmatized)
	# layer2_dict = ConvertIntoDict(layer2_lemmatized)


	#make index
	MakeDictionaryWord2Id()

	ChangeCorpusToMapping()

	MakePostingList()

	

	GetTfidf()

	LSIModelTrain()

	LDAModelTrain()

	PivotTrain(FileNum)




if __name__=='__main__':
	main()
