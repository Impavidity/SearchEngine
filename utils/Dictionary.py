import os, sys
import pickle, pprint


class Entry(object):
    def __init__(self, file):
        self.file = file


def parse_arguments():
    pass


def get_tokens():
    pass


def preprocess(database):
    files = os.listdir(database)

    for file in files:
        pass


def construct_tiered_index():
    pass


if __name__ == '__main__':
    assert len(sys.argv) > 1, "There isn't any database."

    database = sys.argv[1]
    assert os.path.exists(database), "Database {} doesn't exist.".format(database)

    preprocess(database)



