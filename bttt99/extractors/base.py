import re
import urllib.parse
import concurrent.futures
import itertools
import reprlib
from collections import namedtuple

import lxml.html
import requests
import pyperclip


BASE_URL = 'http://www.bttt99.com/'
TAGS_URL = 'http://www.bttt99.com/tag/'
SEARCH_URL = 'http://www.bttt99.com/s'
UA = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36'

torrents_re = re.compile('<a href="(.*?)" title=".*?" target="_self">(.*?)</a>')

session = requests.Session()
session.headers.update({'user-agent': UA})

Torrent = namedtuple('Torrent', 'link title description rate')


class BaseExtractor(object):
    
    def __init__(self):
        self._session = requests.session()

    def search(self, keyword, resolution):
        raise NotImplementedError
    
    def fetch_torrents(self, keyword):
        self.show_torrents(self.search(keyword))

    def get_json(self, url):
        return self._session.get(url).json()

    def get_html(self, url):
        return self._session.get(url).text

    def get_torrents(self, url):
        _id = url.rstrip('/').rsplit('/', 1)[-1]
        page = session.get(url).content.decode('utf8')
        doc = lxml.html.fromstring(page)
        for a in doc.xpath('//div[@class="download"]/ul/li/a'):
            link = a.attrib['href']
            title = a.text_content()
            description = doc.xpath('//div[@class="summary"]')[0].text_content().strip()
            rate = doc.xpath('//span[@class="rate"]')[0].text_content()
            yield Torrent(link=link, title=title, description=description, rate=rate)


    def copy_to_clipboard(self, text):
        pyperclip.copy(text)


    def grab(self):
        r = session.get(BASE_URL)
        futures = []
        if r.ok:
            html = r.text
            with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
                for link in set(re.findall(r'/tv/\d+/', html)):
                    url = urllib.parse.urljoin(BASE_URL, link)
                    print(url)
                    future = executor.submit(get_torrent, url)
                    futures.append(future)
                for fu in concurrent.futures.as_completed(futures):
                    result = fu.result()
                    print(result)


    def show_torrents(self, torrents):
        if torrents:
            for i, tor in enumerate(torrents, 1):
                print('\n{}: {}\n{}'.format(i, tor.link, tor.title))
            print('简介:', torrents[0].description)
            print('Rate: ', torrents[0].rate)
            which = int(input('Which one?'))
            torrent = torrents[which - 1]
            copy_to_clipboard(torrent.link)
            print('Copied to clipboard')
            return torrent
        else:
            print("未找到查询的种子")


