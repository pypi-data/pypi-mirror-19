from bs4 import BeautifulSoup
import requests
import sympy
from sympy.core.sympify import SympifyError
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
        template = utils.TEMPLATES['GCAL']
        return template['SUCCESS'] % (
            _query, self._texify_result(result), result
        ) if result else template['FAILURE'] % _query

    def _texify_result(self, result):
        lhs, rhs = result.split('=')
        try:
            lhs = '\[%s' % sympy.latex(sympy.sympify(lhs, evaluate=False))
            rhs = '%s\]' % sympy.latex(sympy.sympify(rhs, evaluate=False))
        except SympifyError:
            pass
            # logging.warn('Unable to convert to latex %s' % result)  #FIXME Add this
        return '%s = %s' % (lhs, rhs)