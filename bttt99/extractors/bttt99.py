"""
  Grab the torrent from bttt99 website.
"""
from .base import BaseExtractor


class Bttt99Extractor(BaseExtractor):

    def search(self, name):
        html = self.get_html(SEARCH_URL, params={'q': name})
        doc = lxml.html.fromstring(html)
        xp = doc.xpath('//div[@class="taginfo"]//a')
        if xp:
            founds = [(a.attrib['href'], a.text_content()) for a in xp]
            while 1:
                for i, (url, title) in itertools.chain(enumerate(founds, 1),  [('q', ('Quit', 'Quit'))]):
                    print('{}: {}'.format(i, title))

                choice = input('Please have a choice: ')
                if choice == 'q':
                    exit(0)
                try:
                    uri, _ = founds[int(choice) - 1]
                    url = urllib.parse.urljoin(BASE_URL, uri)
                    torrents = list(get_torrents(url))
                except (IndexError, ValueError): 
                    print('Input invalid')
        else:
            print('No result')

        return torrents