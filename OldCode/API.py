#!/usr/bin/python
# -*- coding: utf-8 -*-


def WordSearchFileProcess(ans):
	import json
	import sys
	reload(sys)
	sys.setdefaultencoding('utf-8')
	doc = {"news":[]}
	#print ans
	count = 0
	for item in ans:
		f = open("D:/PyCode/Page/app/demo/data/"+str(item[0]+1),"r")
		url = f.readline()
		date = f.readline()
		title = f.readline()
		description = f.readline()
		url = url[:-1].decode("utf-8")
		date = date[:-1].decode("utf-8")
		title =  title[:-1].decode("utf-8")
		description = description[:-1].decode("utf-8")
		content = "     ".decode("utf-8")
		s = f.readline()
		while (len(s)>0):
			content = content + "<br>".decode("utf-8")+ "    ".decode("utf-8")+s.decode("utf-8")
			s = f.readline()
		article = {}
		article["date"] = date
		article["title"] = title
		article["url"] = url
		article["summary"] = description
		article["content"] = content
		doc["news"].append(article)
		count += 1
		if count > 20:
			break
	save = open("D:/PyCode/Page/app/demo/data/save","w")
	save.write(json.dumps(doc))
	#return doc

