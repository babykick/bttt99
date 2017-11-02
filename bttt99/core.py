"""
  API and command-line interface
"""
from . import get_extractor

default_extractor = 'gaoqingfm'


def search(keyword):
    Extractor = get_extractor(default_extractor)
    if not Extractor:
        raise TypeError('No proper extractor found by {}'.format(default_extractor))
    extractor = Extractor()
    extractor.fetch(keyword)
