from config.config import config
import re
import numpy as np
from math import log


def comp_tuple(x, y):
    assert isinstance(x, tuple) and isinstance(y, tuple), 'x and y are not tuple.'
    assert len(x) == len(y) == 2, 'lengths of x and y are not right.'
    if x[1] < y[1]:
        return 1
    elif x[1] > y[1]:
        return -1
    else:
        return 0


def weights(v1, v2):
    assert len(v1) == len(v2), 'The length of two vector is not equal.'

    return np.sum(v1 * v2)


def tokenlize(string):
    token_pattern = re.compile(r'[^a-zA-Z0-9.,_]')
    pre_token_stream = re.split(token_pattern, string.replace('&lt', ' '))
    strip_token_stream = [x.strip(',.').replace(",", "").lower() for x in pre_token_stream if x != None]
    return [x.lower() for x in strip_token_stream if x != '' and x not in config.STOP_WORDS]


def tokens_to_vector(index, input_tokens):
    # Pre-process input tokens
    tf = {}
    tokens = []
    for token in input_tokens:
        if token in tokens:
            tf[token] += 1
        else:
            tf[token] = 1
            tokens.append(token)

    # Construct the vector
    vlen = len(index.voc.tokens)
    vector = np.zeros([1, vlen])

    for token in tokens:
        if token in index.voc.tokens:
            if config.WEIGHT_TYPE == 'wf-idf':
                vector[0, index.voc.token_index[token]] = (1 + log(tf[token])) * index.voc.idf[token]
            elif config.WEIGHT_TYPE == 'tf-idf':
                vector[0, index.voc.token_index[token]] = tf[token] * index.voc.idf[token]

    return vector, tokens
