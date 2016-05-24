#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

FileNum = int(sys.argv[1])
i = 1
File = 1
while (i<=FileNum):
	try:
		fr = open("Mining/"+str(i),"r")
		line = fr.readline()
		count = 1
		content = line
		while (len(line)>0):
			line = fr.readline()
			content = content + line
			count += 1
		if count>=6:
			fw = open("data/"+str(File),"w")
			fw.write(content)
			File += 1
		i += 1
	except:
		print "FileNum:",i
		i +=1
		if i>FileNum:
			break
		continue