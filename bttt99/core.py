"""
  API and command-line interface
"""


def search(keyword):
    from .extractors.gaoqingfm import Gaoqingfm
    extractor = Gaoqingfm()
    extractor.fetch(keyword)
