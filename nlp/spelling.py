# -*- coding: utf-8 -*-
import collections


class Spelling(object):
    ALPHA = "abcdefghijklmnopqrstuvwxyz"
    PUNCTUATION = [',','.',':','?',';','(',')','[',']','&','!','*','@','#','$','%','+','<','>','\"']

    def __init__(self, path):
        self.path = path
        self.feature = []

    def load(self):
        for path in self.path:
            fin = open(path)
            for item in fin.readlines():
                self.feature.append(item.strip())
        

    def train(self):
        '''
        Counts the words in the given corpora
        '''
        n = len(self.feature)
        self.model = collections.defaultdict(lambda:1)
        for f in self.feature:
            self.model[f.lower()] += 1
        
    def edit1(self, word):
        '''
        Return a set of words with edit distance 1 from the given word.
        '''
        n = len(word)
        deletetion = [word[0:i]+word[i+1:] for i in range(n)]
        transposition = [word[0:i]+word[i+1]+word[i]+word[i+2:] for i in range(n-1)]
        alteration = [word[0:i]+c+word[i+1:] for i in range(n) for c in Spelling.ALPHA]
        insertion = [word[0:i]+c+word[i:] for i in range(n+1) for c in Spelling.ALPHA]
        return set(deletetion + transposition + alteration + insertion)

    def edit2(self, word):
        '''
        Return a set of words with edit distance 2 from the given word.
        '''
        return set(e2 for e1 in self.edit1(word) for e2 in self.edit1(e1))

    def know(self, words):
        return set(w for w in words if w in self.model)

    def correct(self, word):
        word = word.lower()
        if len(word) == 1:
            return [(word, 1.0)] # I
        if word in Spelling.PUNCTUATION:
            return [(word, 1.0)] # .?!
        if word.replace(".", "").isdigit():
            return [(word, 1.0)] # 1.5
        candidates = self.know([word]) or self.know(self.edit1(word)) or self.know(self.edit2(word)) or set([word])
        candidates = [(self.model[c], c) for c in candidates]
        s = float(sum(p for p, word in candidates))
        candidates = sorted(((p / s, word) for p, word in candidates), reverse=True)
        print candidates
        return candidates[0]
        #return max()




if __name__=="__main__":
    corrector = Spelling(["../corpora/words_extend","../corpora/words_domain"])
    corrector.load()
    corrector.train()
    print corrector.correct("tape")
