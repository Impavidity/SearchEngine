import re
from config.config import config
from utils.tools import weights
from tools import tokenlize, tokens_to_vector, comp_tuple

def wildcard_query(index , query):
    regex = re.compile(query)
    match_tokens = [string for string in index.voc.tokens if re.match(regex, string)]
