import json
import nltk
import numpy

stop_words = nltk.corpus.stopwords.words('english') + [
'.',
',',
'--',
'\'s',
u'\u2019s',
u'\u2014',
'?',
')',
'(',
':',
'\'',
'\'re',
'"',
'-',
'}',
'{',
u'$',
u'\u201d'
]


N = 100
CLUSTER_THRESOHLD = 5
TOP_SENTENCES = 5

def _score_sentences(sentences, important_words):
	scores = []
	sentence_idx = -1

	for s in [nltk.tokenize.word_tokenize(s) for s in sentences]:
		sentence_idx += 1
		word_idx = []

		for w in important_words:
			try:
				word_idx.append(s.index(w))
			except ValueError, e:
				pass

		word_idx.sort()

		if len(word_idx)==0: continue

		clusters = []
		cluster = [word_idx[0]]
		i = 1
		while i<len(word_idx):
			if word_idx[i] - word_idx[i - 1] < CLUSTER_THRESOHLD:
				cluster.append(word_idx[i])
			else:
				clusters.append(cluster[:])
				cluster = [word_idx[i]]
			i += 1
		cluster.append(cluster)

		max_cluster_score = 0
		for c in clusters:
			siginificant_words_in_cluster = len(c)
			total_words_in_cluster = c[-1] - c[0] + 1
			score = 1.0 * siginificant_words_in_cluster * siginificant_words_in_cluster / total_words_in_cluster

			if score > max_cluster_score:
				max_cluster_score = score

		scores.append((sentence_idx, score))

	return scores

def summarize(txt):
	sentences = [s for s in nltk.tokenize.sent_tokenize(txt)]
	normalized_sentences = [s.lower() for s in sentences]

	words = [w for sentence in normalized_sentences for w in nltk.tokenize.word_tokenize(sentence) if w not in stop_words]
	#words = [w for sentence in sentences for w in words if w not in stop_words]

	fdist = nltk.FreqDist(words)

	top_n_words = [w[0] for w in fdist.most_common(N)]

	scored_sentences = _score_sentences(normalized_sentences, top_n_words)

	avg = numpy.mean([s[1] for s in scored_sentences])
	std = numpy.std([s[1] for s in scored_sentences])
	mean_scored = [(sent_idx, score) for (sent_idx, score) in scored_sentences if score > avg + 0.5 * std]

	top_n_scored = sorted(scored_sentences, key=lambda s: s[1])[-TOP_SENTENCES:]
	top_n_scored = sorted(top_n_scored, key = lambda s: s[0])

	return ([sentences[idx] for (idx, score) in top_n_scored], [sentences[idx] for (idx, score) in mean_scored])

def abstract(filename)
	article = open(filename,'r').readlines()
	data = article[2:]
	content = data[0].decode("utf-8")[:-1]
	for paragraph in data[1:]:
		content = content + " " + paragraph.decode("utf-8")[:-1]

	new_content = summarize(content)

	print article[2]
	print
	print 'Top N Summary'
	print '--------------'
	print ' '.join(new_content[0])
	print
	print 'Mean Scored Summary'
	print '--------------'
	print ' '.join(new_content[1])

	return(' '.join(new_content[0]), ' '.join(new_content[1]))



