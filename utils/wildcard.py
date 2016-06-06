import re

def wildcard_query(dictionary, voc, query):
    regex = re.compile(query)
    match_tokens = [string for string in voc.tokens if re.match(regex, string)]
