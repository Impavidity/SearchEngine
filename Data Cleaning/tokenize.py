#!/usr/bin/python

name="1"
doc = open("tmp/doc/"+name, "r")
contents = doc.readlines()
passage = contents[2][9:]
primordialTokens = passage.split(' ')
stripPuncTokens = [x.strip(',.+').lower().replace(",","") for x in primordialTokens if x != '']

for i in range(len(stripPuncTokens)):
	if '/' in stripPuncTokens[i]:
		toProcess = stripPuncTokens.pop(i)
		stripPuncTokens.extend(toProcess.split('/'))
		
print stripPuncTokens
