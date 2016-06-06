from config.config import config
from utils.tools import weights
from tools import tokenlize, tokens_to_vector, comp_tuple


def get_result(index, tokens, query_vector):
    result = []
    tokens = [token for token in tokens if token in index.voc.tokens]

    for level in index.tiered_index:
        for token in tokens:
            id = index.voc.token_index[token]
            docs = level[id]
            for doc in docs:
                if doc not in result:
                    weight = weights(query_vector, doc.weight)
                    result.append((doc, weight))
                    if len(result) > config.PARA_TOP_K:
                        return result
    if config.DEBUG:
        print '----------------query result--------------------'
        print result
        print '------------------------------------------------'
    result.sort(comp_tuple)
    return result


def topK_query(index, query, index_type='tiered'):
    query_vector, tokens = tokens_to_vector(index, tokenlize(query))

    result = []
    if index_type == 'tiered':
        result = get_result(index, tokens, query_vector)

    return result
