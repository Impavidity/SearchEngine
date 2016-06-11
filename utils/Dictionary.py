from config.config import config
import os, sys, re
import cPickle as pickle


class Entry(object):
    def __init__(self, doc_id, doc_path):
        assert os.path.exists(doc_path), "File {} doesn't exits.".format(doc_path)
        self.docID = doc_id
        self.tokens = {}

        doc = open(doc_path, "r")
        self.get_tokens(doc)

        doc.close()

    def get_tokens(self, doc):
        token_stream = []
        token_pattern = re.compile(r'[^a-zA-Z0-9.,_]')
        for line in doc.readlines():
            pre_token_stream = re.split(token_pattern, line.replace('&lt', ' '))
            strip_token_stream = [x.strip(',.').replace(",", "").lower() for x in pre_token_stream if x != None]
            token_stream += [x.lower() for x in strip_token_stream if x != '' and x not in config.STOP_WORDS]

        for item in token_stream:
            if item not in config.STOP_WORDS:
                if item not in self.tokens:
                    self.tokens[item] = 1
                else:
                    self.tokens[item] += 1

    def set_weight(self, weight):
        self.weight = weight


class Voc(object):
    def __init__(self, entries):
        assert isinstance(entries, list), 'The entries is not the instance of list.'
        self.tokens = []
        self.dic = {}
        self.doc_numbers = len(entries)

        # Calculate tf and df for each token
        for entry in entries:
            assert isinstance(entry, Entry), 'The entry is not the instance of Entry.'
            for token in entry.tokens:
                if token not in self.tokens:
                    self.tokens.append(token)
                    self.dic[token]={
                        'tf': entry.tokens[token],
                        'df': 1
                    }
                else:
                    self.dic[token]['tf'] += entry.tokens[token]
                    self.dic[token]['df'] += 1

        self.tokens.sort()
        # Calculate idf and set the index for each token
        for index, token in enumerate(self.tokens):
            self.dic[token]['idf'] = self.doc_numbers / self.dic[token]['df']
            self.dic[token]['index'] = index


class Index(object):
    def __init__(self, voc, entries):
        self.voc = voc
        self.entries = entries
        self.tiered_index = []

    def construct_tiered_index(self):
        # calculate_weights(self.voc, self.entries)

        for _ in config.THRESHOLD:
            self.tiered_index.append([])

        for id1, threshold in enumerate(config.THRESHOLD):
            for id2, token in enumerate(self.voc.tokens):
                self.tiered_index[id1].append([])
                for entry in entries:
                    if token in entry.tokens and entry.tokens[token] >= threshold:
                        self.tiered_index[id1][id2].append(entry.docID)


class Info(object):
    def __init__(self, voc, entries, index):
        self.voc_tokens = voc.tokens
        self.voc_dic = voc.dic
        self.entry_tokens = {}
        self.tiered_index = index.tiered_index

        for entry in entries:
            self.entry_tokens[entry.docID] = entry.tokens

def preprocess(database):
    docs = os.listdir(database)
    entries = []

    id_html = {}
    for index, doc in enumerate(docs):
        if config.DEBUG and index > 300:
            break
        id_html[index] = doc
        entries.append(Entry(index, database + os.sep + doc))

    if config.DEBUG:
        id_html_file = open(config.ID_HTML_FILE, 'w')
        pickle.dump(id_html, id_html_file, config.PICKLE_PROTOCOL)
    return Voc(entries), entries


def construct_tiered_index(voc, entries):
    assert isinstance(voc, Voc), 'voc is not the instance of Voc.'
    assert isinstance(entries, list), 'entries is not the instance of list.'

    index = Index(voc, entries)
    index.construct_tiered_index()
    info = Info(voc, entries, index)

    tiered_index_file = open(config.TIERED_INDEX_FILE, 'w')
    pickle.dump(info, tiered_index_file, config.PICKLE_PROTOCOL)
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
