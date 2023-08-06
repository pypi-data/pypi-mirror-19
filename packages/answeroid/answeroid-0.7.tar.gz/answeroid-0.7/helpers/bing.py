import urllib
from bs4 import BeautifulSoup
import requests

REPLY_TEMPLATE = '''Bing says: %s'''


class Bing:
    @staticmethod
    def create_reply(self, content):
        _, *_query = content.split('BING:')
        _query = _query[0].strip()
        resp = requests.get('https://www.bing.com/search?' + urllib.parse.urlencode({'q': _query}))
        try:
            result = BeautifulSoup(resp.content, 'html.parser').find('div', {'class': 'WordContainer'})
        except AttributeError:
            result = None
        return REPLY_TEMPLATE % result if result else "Unable to compute {%s}" % _query
