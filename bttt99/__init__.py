__author__ = """Stephen Chen"""
__email__ = 'noemail@noemail.com'
__version__ = '0.1'

from .extractors.gaoqingfm import Gaoqingfm


EX_mapping = {
    'gaoqingfm': Gaoqingfm
}


def get_extractor(name):
    return EX_mapping.get(name)
