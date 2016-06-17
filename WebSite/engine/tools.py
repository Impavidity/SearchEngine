from engine.config.config import config
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
    token_pattern = re.compile(r'[^a-zA-Z0-9.,_*]')
    pre_token_stream = re.split(token_pattern, string.replace('&lt', ' '))
    strip_token_stream = [x.strip(',.').replace(",", "").lower() for x in pre_token_stream if x != None]
    tokens = [x.lower() for x in strip_token_stream if x != '' and x not in config.STOP_WORDS]

    result = {}
    for token in tokens:
        if token in result:
            result[token] += 1
        else:
            result[token] = 1

    return result



