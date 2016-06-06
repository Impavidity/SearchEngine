from config.config import config
from math import log
import os, sys, re
import numpy as np
import cPickle as pickle

def calculate_weights(voc, entries):
    vlen = len(voc.tokens)

    for entry in entries:
        vector = np.zeros([1, vlen])
        for token in entry.tokens:
            if config.WEIGHT_TYPE == 'wf-idf':
                vector[0, voc.token_index[token]] = (1 + log(entry.tf[token])) * voc.idf[token]
            elif config.WEIGHT_TYPE == 'tf-idf':
                vector[0, voc.token_index[token]] = entry.tf[token] * voc.idf[token]
        entry.set_weight(vector)


class Entry(object):
    def __init__(self, doc_path):
        assert os.path.exists(doc_path), "File {} doesn't exits.".format(doc_path)
        self.docID = doc_path
        self.tokens = []
        self.tf = {}
        self.weight = np.array([])

        doc = open(self.docID, "r")
        self.get_tokens(doc)

        doc.close()

    def get_tokens(self, doc):
        token_stream = []
        token_pattern = re.compile(r'[^a-zA-Z0-9.,_]')
        for line in doc.readlines():
            pre_token_stream = re.split(token_pattern, line.replace('&lt', ' '))
            strip_token_stream = [x.strip(',.').replace(",", "").lower() for x in pre_token_stream if x != None]
            token_stream += [x.lower() for x in strip_token_stream if x != '' and x not in config.STOP_WORDS]

        print token_stream
        for item in token_stream:
            if item not in config.STOP_WORDS:
                if item not in self.tokens:
                    self.tokens.append(item)
                    self.tf[item] = 1
                else:
                    self.tf[item] += 1

    def set_weight(self, weight):
        self.weight = weight


class Voc(object):
    def __init__(self, entries):
        assert isinstance(entries, list), 'The entries is not the instance of list.'
        self.tokens = []
        self.token_index = {}
        self.tf = {}
        self.df = {}
        self.idf = {}
        self.doc_numbers = len(entries)

        # Calculate tf and df for each token
        for entry in entries:
            assert isinstance(entry, Entry), 'The entry is not the instance of Entry.'
            for token in entry.tokens:
                if token not in self.tokens:
                    self.tokens.append(token)
                    self.tf[token] = entry.tf[token]
                    self.df[token] = 1
                else:
                    self.tf[token] += entry.tf[token]
                    self.df[token] += 1

        # Calculate idf for each token
        for token in self.tokens:
            self.idf[token] = log(self.doc_numbers / self.df[token])

        self.tokens.sort()

        for index, token in enumerate(self.tokens):
            self.token_index[token] = index


class Index(object):
    def __init__(self, voc, entries):
        self.voc = voc
        self.entries = entries
        self.tiered_index = []

    def construct_tiered_index(self):
        calculate_weights(self.voc, self.entries)

        for _ in config.THRESHOLD:
            self.tiered_index.append([])

        for id1, threshold in enumerate(config.THRESHOLD):
            for id2, token in enumerate(self.voc.tokens):
                self.tiered_index[id1].append([])
                for entry in entries:
                    if token in entry.tokens and entry.tf[token] >= threshold:
                        self.tiered_index[id1][id2].append(entry)


def preprocess(database):
    docs = os.listdir(database)
    entries = []

    for index, doc in enumerate(docs):
        if config.DEBUG and index > 1000:
            break
        entries.append(Entry(database + os.sep + doc))

    return Voc(entries), entries


def get_tiered_index():
    pkl_file = open(config.TIERED_INDEX_FILE, 'r')

    tiered_index = pickle.load(pkl_file)

    return tiered_index


def construct_tiered_index(voc, entries):
    assert isinstance(voc, Voc), 'voc is not the instance of Voc.'
    assert isinstance(entries, list), 'entries is not the instance of list.'

    index = Index(voc, entries)
    index.construct_tiered_index()

    tiered_index_file = open(config.TIERED_INDEX_FILE, 'w')
    pickle.dump(index, tiered_index_file, config.PICKLE_PROTOCOL)
    print 'Success to store the index into file {}'.format(config.TIERED_INDEX_FILE)


if __name__ == '__main__':
    if not config.DEBUG:
        assert len(sys.argv) > 1, "There isn't any database."

    if config.DEBUG:
        database = config.DATABASE_PATH
    else:
        database = sys.argv[1]
    assert os.path.exists(database), "Database {} doesn't exist.".format(database)

    print 'Parsing vocabulary and entry .............'
    voc, entries = preprocess(database)
    print 'Parsed vocabulary and entry.'

    print 'Constructing tiered index ..............'
    construct_tiered_index(voc, entries)
    print 'Constructed tiered index.'
