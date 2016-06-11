from config.config import config
from dictionary import Info
from utils.tools import weights
from tools import tokenlize, comp_tuple
from math import log
import numpy as np
import cPickle as pickle
import re


class query_voc(object):
    def __init__(self, tokens, dic):
        self.tokens = tokens
        self.dic = dic


class query_entry(object):
    def __init__(self, doc_id, tokens, voc):
        self.docID = doc_id
        self.tokens = tokens
        self.vector = np.array([1, len(voc.tokens)])

        for token in self.tokens:
            if config.WEIGHT_TYPE == 'wf-idf':
                self.vector[0, voc.tokens[token]['index']] = (1 + log(self.tokens[token])) * voc.tokens[token]['idf']
            elif config.WEIGHT_TYPE == 'tf-idf':
                self.vector[0, voc.tokens[token]['index']] = self.tokens[token] * voc.tokens[token]['idf']


class query_index(object):
    def __init__(self, tiered_index):
        self.tiered_index = tiered_index


def load_and_calc(pkl_path):
    assert isinstance(pkl_path, str), "pkl_path is not the instance of string.\n"

    pkl_file = open(pkl_path, 'r')
    info = pickle.load(pkl_file)

    voc = query_voc(info.voc_tokens, info.voc_dic)
    tiered_index = query_index(info.tiered_index)
    entries = []
    for doc_id, tokens in enumerate(info.entry_tokens):
        entries.append(query_entry(doc_id, tokens, voc))

    return tiered_index, voc, entries


def construct_query_vector(tokens, voc):
    query_vector = np.array([1, len(voc.tokens)])
    for token in tokens:
        if token in voc.tokens:
            query_vector[0, voc.dic[token]['index']] = tokens[token]
    return query_vector


def topK_get_result(index, voc, entries, tokens):
    result = []
    query_vector = construct_query_vector(tokens, voc)

    for level in index.tiered_index:
        for token in tokens:
            docs = level[voc.dic[token]['index']]
            for doc_id in docs:
                if doc_id not in result:
                    weight = weights(query_vector, entries[doc_id].weight)
                    result.append((doc_id, weight))

        if len(result) >= config.PARA_TOP_K:
            return result[:config.PARA_TOP_K]

    if config.DEBUG:
        print '----------------query result--------------------'
        print result
        print '------------------------------------------------'
    return result


def topK_query(index, voc, entries, query, index_type='tiered'):
    result = []
    if index_type == 'tiered':
        result = topK_get_result(index, voc, entries, tokenlize(query))
    result.sort(comp_tuple)

    return result


def wildcard_query(index, voc, entries, query, index_type='tiered'):
    tokens = tokenlize(query)
    query_match = [[]]
    for token in tokens:
        regex = re.compile(token)
        match_tokens = [string for string in voc.tokens if re.match(regex, string)]
        tmp = []
        if len(match_tokens) > 0:
            for t1 in match_tokens:
                for t2 in query_match:
                    tmp.append(t2 + [t1])
            query_match = tmp

    result = []
    match_id = []
    if index_type == 'tiered':
        for match in query_match:
            result.append(topK_get_result(index, voc, entries, match))

    result.sort(comp_tuple)

    match = []
    for doc in result:
        if doc[0] in match_id:
            continue
        else:
            match_id.append(doc[0])
            match.append(doc)

        if len(match_id) > config.PARA_TOP_K:
            return match
    return match