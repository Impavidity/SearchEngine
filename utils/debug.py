from dictionary import *
import topK, wildcard

if __name__ == "__main__":
    index = get_tiered_index()
    print topK.topK_query(index, 'bania review')