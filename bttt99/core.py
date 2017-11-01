"""
  API and command-line interface
"""
import re
import urllib.parse

import requests
import lxml.html as H


DOWNLOAD_BASE_URL = 'http://assrt.net/'
SUBTITLE_SEARCH_URL = 'http://assrt.net/sub/?searchword={}'

session = requests.session()
session.headers = {
  'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.18 Safari/537.36'
  }


def search(keyword):
    from .extractors.gaoqingfm import Gaoqingfm
    extractor = Gaoqingfm()
    extractor.fetch(keyword)


def find_subtitle(keyword):
    r = session.get(SUBTITLE_SEARCH_URL.format(keyword))
    doc = H.fromstring(r.text)
    els = doc.xpath('//div[@class="subitem"]/a')
    if len(els) > 2:
        el = els[2]
        url = re.search("javascript:location.href='(.*?)'", el.get('onclick')).group(1)
        return urllib.parse.urljoin(DOWNLOAD_BASE_URL, url)
    else:
      return None
