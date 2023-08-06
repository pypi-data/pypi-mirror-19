import urllib
from bs4 import BeautifulSoup
import requests
from helpers import utils

REPLY_TEMPLATE = '''Bing says: %s'''
EXCLUDED_SUBEXPRESSIONS = ["Text under", "\u2026"]
EXCLUDED_EXPRESSIONS = ["\u00B7", ""]  

class Bing:
    @staticmethod
    def create_reply(content):
        _, *_query = content.split('BING:')
        _query = _query[0].strip()
        resp = requests.get('https://www.bing.com/search?' + urllib.parse.urlencode({'q': _query}))
        result = BeautifulSoup(resp.content, 'html.parser').find('div', {'class': 'b_subModule'})
        result = result if result else BeautifulSoup(resp.content, 'html.parser').find('div', {'class': 'WordContainer'})
        try:
            results = [s.strip() for s in result.strings if all(s.strip() != expr for expr in EXCLUDED_EXPRESSIONS) and all(expr not in s for expr in EXCLUDED_SUBEXPRESSIONS)]
            result = "\n".join(results)
            print(results)
        except AttributeError as e:
            print(e)
            result = None
        template = utils.TEMPLATES['BING']
        return template['SUCCESS'] % (_query, result) if result else template['FAILURE'] % _query

