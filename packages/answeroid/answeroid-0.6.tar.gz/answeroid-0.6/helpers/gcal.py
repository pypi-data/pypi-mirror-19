from bs4 import BeautifulSoup
import requests
import urllib
from helpers import utils


class Gcal:
    def create_reply(self, content):
        _, *_query = content.split('GCAL:')
        _query = _query[0].strip()
        resp = requests.get('https://www.google.com/search?' + urllib.parse.urlencode({'q': _query}))
        try:
            result = BeautifulSoup(resp.content, 'html.parser').find('h2', {'class': 'r'}).next_element
        except AttributeError:
            result = None
        return utils.SUCCESS_TEMPLATE % result if result else utils.FAILURE_TEMPLATE % _query
