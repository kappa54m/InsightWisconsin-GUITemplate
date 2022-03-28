import os
import sys
from typing import List, Set
import json
import logging
import pathlib

#import yaml


uis_path = ''


config = {}


def load(path, encoding='utf-8'):
    #with open(path, encoding=encoding) as f:
    #    global config
    #    config = yaml.full_load(f)
    pass


# Init logger (TODO add file handler)
lg = logging.getLogger('UniversalUI')
lg.setLevel(logging.DEBUG)

stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setLevel(logging.DEBUG)
lg.addHandler(stream_handler)

