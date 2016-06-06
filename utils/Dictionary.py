from config.config import config
import os, sys, re
import numpy as np
import pickle, pprint


class Entry(object):
    def __init__(self, doc_path):
        assert os.path.exists(doc_path), "File {} doesn't exits.".format(doc_path)
        self.docID = doc_path
        self.tokens = []
        self.tf = {}

        doc = open(self.docID, "r")
        self.get_tokens(doc)

        doc.close()

    def get_tokens(self, doc):
        token_stream = []
        for line in doc.readlines():
            token_stream += line.replace('&lt', ' ').replace('<', ' ').replace('>', ' ')\
                .replace('/', ' ').replace('(', ' ').replace(')', ' ').replace(',', ' ')\
                .replace(':', ' ').replace('\'', ' ').replace('\"', ' ').replace('?', ' ')\
                .strip().split()

        for item in token_stream:
            if item.lower() not in config.STOP_WORDS:
                if item.lower() not in self.tokens:
                    self.tokens.append(item.lower())
                    self.tf[item.lower()] = 1
                else:
                    self.tf[item.lower()] += 1


class Voc(object):
    def __init__(self, entries):
        assert isinstance(entries, list), 'The entries is not the instance of list.'
        self.tokens = []
        self.tf = {}

        for entry in entries:
            assert isinstance(entry, Entry), 'The entry is not the instance of Entry.'
            for item in entry.tokens:
                if item not in self.tokens:
                    self.tokens.append(item)
                    self.tf[item] = 1
                else:
                    self.tf[item] += 1

        self.tokens.sort()


def parse_arguments():
    pass


def preprocess(database):
    files = os.listdir(database)
    entries = []

    for index, file in  enumerate(files):
        if config.DEBUG and index > 2000:
            break
        entries.append(Entry(database + os.sep + file))

    return Voc(entries), entries


def construct_tiered_index(voc, entries):
    assert isinstance(voc, Voc), 'voc is not the instance of Voc.'
    assert isinstance(entries, list), 'entries is not the instance of list.'
    pass


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



