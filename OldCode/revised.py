#!/usr/bin/python
# -*- coding: utf-8 -*-

from nltk.corpus import wordnet

def Levenshtein_Dist(s1,s2):
	m = [[0 for col in range(len(s2)+1)] for row in range(len(s1)+1)]
	for i in range(len(s1)+1):
		m[i][0] = i
	for j in range(len(s2)+1):
		m[0][j] = j
	for i in range(len(s1)):
		for j in range(len(s2)):
			if s1[i] == s2[j]:
				m[i+1][j+1] = min(m[i][j+1],m[i+1][j],m[i][j])
			else:
				m[i+1][j+1] = min(m[i][j+1]+1, m[i+1][j]+1, m[i][j]+1)
	return m[len(s1)][len(s2)]


def Revised(s,word2id):
	#import a dictionay as correct_dictionary
	if s in word2id:
		return s
	sys = wordnet.synsets(s)
	distance = 100
	word = ""
	correct_dictionary = {}
	#correct_dictionary["systm"] = "system"
	if len(sys) == 0:
		if (s in correct_dictionary):
			return correct_dictionary[s]
		else:
			for item in word2id:
				dist = Levenshtein_Dist(s,item)
				if dist<distance:
					distance = dist
					word = item
			return word
	else:
		return s
		#if not (s in word2id):
		#	net