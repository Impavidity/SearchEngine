from easydict import EasyDict
import os

config = EasyDict()

config.DEBUG = True

config.DATABASE_PATH = 'D:\\Dataset\\Reuters'

config.ROOT = '..' + os.sep

config.ENTRIES_FILE = 'entries.txt'

config.VOCABULLARY_FILE = 'vocabullary.txt'

config.TIRED_INDEX_FILE = 'tired_index.txt'

config.PARA_TOP_K = 20

config.THRESHOLD = [5, 10, 20]
