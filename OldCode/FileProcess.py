#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
def FileMake(FileNum):
	print "File Combine"
	i=1
	corpus = {}
	while i<=FileNum:
		f = open("data/"+str(i),"r")
		url = f.readline()
		date = f.readline()
		title = f.readline()
		description = f.readline()
		url = url[:-1].decode("utf-8")
		date = date[:-1].decode("utf-8")
		title =  title[:-1].decode("utf-8")
		content = ""
		first_para = f.readline()
		first_para = first_para[:-1].decode("utf-8")
		s = f.readline()
		while (len(s)>0):
			content = content + s[:-1].decode("utf-8")
			s = f.readline()
		article = {}
		article["date"] = date
		article["title"] = title
		article["url"] = url
		article["description"] = description
		article["content"] = content
		article["first_para"] = first_para
		corpus[i] = article
		i += 1

	filename = "corpus"
	f = open("data/"+filename,"w")
	f.write(json.dumps(corpus, indent =4))
	print "File Combine Finish"

