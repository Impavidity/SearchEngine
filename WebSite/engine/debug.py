import cPickle as pickle
import os
from config.config import config
from dic import parse, Info
from query import topK_query, wildcard_query, load_and_calc

if __name__ == "__main__":
    if not os.path.exists(config.TIERED_INDEX_FILE) or not os.path.exists(config.ID_HTML_FILE):
        info, id_html = parse()
        tiered_index_file = open(config.TIERED_INDEX_FILE, 'w')
        pickle.dump(info, tiered_index_file, config.PICKLE_PROTOCOL)
        id_html_file = open(config.ID_HTML_FILE, 'w')
        pickle.dump(id_html, id_html_file, config.PICKLE_PROTOCOL)

    pkl_file = open(config.TIERED_INDEX_FILE, 'r')
    info = pickle.load(pkl_file)
    index, voc, entries = load_and_calc(info)

    pkl_file = open(config.ID_HTML_FILE, 'r')
    id_html = pickle.load(pkl_file)
    print '------------------------- top k --------------------------------'

    result = topK_query(index, voc, entries, 'board beverage operations')
    html = []
    for item in result:
        print item, id_html[item[0]]
    print '------------------------- top k --------------------------------'

    print '------------------------- wild --------------------------------'

    result = wildcard_query(index, voc, entries, 'board beverage opera*')
    html = []
    for item in result:
        print item, id_html[item[0]]

    print '------------------------- wild --------------------------------'
