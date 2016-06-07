#!/usr/bin/python
import os
import json
import utils

def genName2docID():
	name2docID = {}
	docID2Name = {}
	
	cur_docID = 0
	filenames = [x for x in os.listdir('tmp/doc') if x[0] != '.']
	for name in filenames:
		name2docID[name] = cur_docID
		docID2Name[cur_docID] = name
		cur_docID += 1
		
	name2docIDFile = open("name2docID.json", "w")
	json.dump(name2docID, name2docIDFile)
	name2docIDFile.close()	
	
	docID2NameFile = open("docID2Name.json", "w")
	json.dump(docID2Name, docID2NameFile)
	docID2NameFile.close()

genName2docID()