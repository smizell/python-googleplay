import urllib
from decimal import Decimal

from BeautifulSoup import BeautifulSoup

from google_play.base import Item
from google_play.conf import *
from google_play.decorators import requires_fetch
from google_play.items import App, Book, Movie
from google_play.utils import get_raw_html

class Page(object):
    """
    Class for one page of search results
    """

    apps = []

    item_types = {
        'apps': App,
        'books': Book,
        'movies': Movie,
    }

    def __init__(self, page, query_string):
        self.page = page
        self.query_string = query_string

        self.obj = self.item_types[query_string['c']]

        self._build_query_string()
        self._fetch_page()

    def previous(self):
        if self.page == 1:
            return None
        return self.page - 1

    def next(self):
        return self.page + 1

    def _build_query_string(self):
        """
        Page 1 is:
        https://play.google.com/store/search?q=scrabble&c=apps
        
        Page 2 is:
        https://play.google.com/store/search?q=scrabble&c=apps&start=48&num=24
        """
        if self.page != 1:
            self.query_string['start'] = (self.page - 1) * 24
            self.query_string['num'] = 24
        return self.query_string

    def _fetch_page(self):
        """
        Fetches the raw html of the page
        """
        url = '%s?%s' % (SEARCH_URL, 
                         urllib.urlencode(self.query_string))
        self.raw_html = get_raw_html(url)
        return self.raw_html

    def _get_items(self):
        """
        Gets the items for all the apps on the page
        """
        soup = BeautifulSoup(self.raw_html)
        items = soup('li', {'class': 'search-results-item'})
        return items

    def get_all(self):
        """
        Gets all the apps on the page
        """
        item_list = []

        items = self._get_items()
        for item in items:
            item_list.append(self.obj(item))

        return item_list

class GooglePlay(object):
    """
    Class for searching the Google Play site

    This scrapes the site listed above under BASE_URL.

    Defaults to app search

    TODO: Iterate over all pages
    """

    page = None

    def __init__(self, search=None, media=MEDIA['apps']):
        self.raw = None
        self.search = search
        self.query_string = {
            'q': search,
            'c': media,
        }

    def _get_page(self, page):
        self.page = Page(page=page, query_string=self.query_string)
        return self.page

    def get_first_page(self):
        """
        Gets the first page of apps
        """
        page = self._get_page(1)
        return page.get_all()

    def get_first(self):
        """
        Gets the first app on the first page
        """
        page = self._get_page(1)
        return page.get_all()[0]