from .base import BaseExtractor, Torrent


SEARCH_URL = 'https://gaoqing.fm/api/search?search={}&limit=100&page=1'


class Gaoqingfm(BaseExtractor):
    """
    Grab data by REST api from http://m.gaoqing.fm/

    torrents list:
        {'count': '1',
        'films': [{'country': '美国',
        'foname': '天才游戏',
        'fupdate': '1998-09-11(美国)',
        'hash': '61ef67fad460',
        'info': '{"writer":"\\u5927\\u536b\\u00b7\\u83b1\\u7ef4\\u6069 \\/ \\u5e03\\u8d56\\u6069\\u00b7\\u79d1\\u4f69\\u5c14\\u66fc","official":"","fp":"","season":"","episode":"","slength":"","type":"\\u8fde\\u7eed\\u5267"}',
        'name': '赌王之王',
        'nd': '1998',
        'rate': '7.4',
        'subject': '1293090',
        'tvtype': True,
        'type': '剧情 / 犯罪'}]}
    
    torrent detail:
        {'cililian': [{'magnet': '9092b6e1213a20923be8f488bf947f734afb01bc',
        'meta': '',
        'name': 'Rounders.199...D.MA.5.1-FGT',
        'size': '39.2 GB'},
        {'magnet': 'e7e5289bfab11118ab0a2d2bd4e1cce403d5075d',
        'meta': '中字',
        'name': 'Rounders 199...Y-Anitafayer',
        'size': '39.3 GB'},
        {'magnet': '60d4f7b751f191d972650d1c6b8bd0f8a4703888',
        'meta': 'Remux',
        'name': '09.06.28.Rou....DD51.MySilu',
        'size': '16.3 GB'},
        {'magnet': 'f423317318e5558b49560763ec41a08e18175ba1',
        'meta': 'Remux',
        'name': 'Rounders 199...MA 5.1 - MiB',
        'size': '17 GB'}],
        'selected': 'BluRay (4)',
        'source': ['BluRay (4)', '1080P (15)', '720P (6)', '标清 (0)', '其他 (0)']}

    """
    def search(self, keyword, resolution='1080p'):
        rsl = {'1080p': '1080P (15)',
               'blueray': 'blueray'}
        res = []
        data = self.get_json(SEARCH_URL.format(keyword))
        for item in data['films']:
            hash = item['hash']
            torrent = self.get_json('https://gaoqing.fm/api/source?hash={}&type=cililian&category={}'.format(hash, rsl.get(resolution)))
            for mag in torrent['cililian']:
                magnet = 'magnet:?xt=urn:btih:{}'.format(mag['magnet'])
                torr = Torrent(magnet=magnet, title=item['name'], size=mag['size'], resolution=torrent['selected'], description=item['info'], rate=item['rate'])
                res.append(torr)
        return res
