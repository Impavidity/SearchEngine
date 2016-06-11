from config.config import config
from dictionary import Info
from query import query_entry, query_index, query_voc
from query import topK_query, wildcard_query, load_and_calc
import cPickle as pickle

if __name__ == "__main__":
    index, voc, entries = load_and_calc(config.TIERED_INDEX_FILE)
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
