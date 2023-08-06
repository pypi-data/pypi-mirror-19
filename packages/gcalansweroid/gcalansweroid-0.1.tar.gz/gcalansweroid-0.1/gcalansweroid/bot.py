from bs4 import BeautifulSoup
import requests
import urllib


REPLY_TEMPLATE = '''Google Calculator says: %s'''


class Gcal:
    def create_reply(self, content):
        _, *_query = content.split('GCAL:')
        _query = _query[0].strip()
        resp = requests.get('https://www.google.com/search?' + urllib.parse.urlencode({'q': _query}))
        try:
            result = BeautifulSoup(resp.content, 'html.parser').find('h2', {'class': 'r'}).next_element
        except AttributeError:
            result = None
        return REPLY_TEMPLATE % result if result else "Unable to compute {%s}" % _query
