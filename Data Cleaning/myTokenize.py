#!/usr/bin/python
from porter import PorterStemmer
import re

stop_words = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now']
#strip_punctuations = [',','.',':','?',';','(',')','[',']','&','!','*','@','#','$','%','+','<','>','\"']
#remove_punctuations = [':','?',';','(',')','[',']','&','!','*','@','#','$','%','...', '','<','>', '--','\"']
# '...' can be removed by str.strip('.')

def tokenize(inputStr):
	tokenPattern = re.compile(r'[^a-zA-Z0-9.,_]')	
#	tokenPattern = re.compile(r'[\s:?;()\[\]&!*@#$%+<>/\\\'\"]|\.(\.)+|(-)+')
	primordialTokens = re.split(tokenPattern, inputStr)
#	primordialTokens = inputStr.replace(">", " ").replace("...", " ").replace("-"," ").replace("'"," ").replace("/"," ").split(' ')
	stripPuncTokens = [x.strip(',.').replace(",","").lower() for x in primordialTokens if x != None]
	stripPuncTokens = [x for x in stripPuncTokens if x != '' and x not in stop_words]

	#stemming
	p = PorterStemmer()
	stemmedTokens = [p.stem(x, 0, len(x)-1) for x in stripPuncTokens]
	return stemmedTokens