from config.config import config
from dictionary import Info
from query import query_entry, query_index, query_voc
from query import topK_query, wildcard_query, load_and_calc

if __name__ == "__main__":
    index, voc, entries = load_and_calc(config.TIERED_INDEX_FILE)
    result = topK_query(index, voc, entries, 'review title command user land mania')
    print result