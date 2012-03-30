import urllib
from decimal import Decimal

from BeautifulSoup import BeautifulSoup

from google_play.decorators import requires_fetch
from google_play.utils import get_raw_html

BASE_URL = 'https://play.google.com'
SEARCH_URL = '%s/store/search' % BASE_URL

QUERY_STRING = {
    'q': None,
    'c': 'apps',
}

class App(object):
    """
    Class for App

    TODO: Get ratings
    """
    # Can be set from original soup
    _name = None
    _url = None
    _price = None
    _category = None

    # Only on detail page, must be fetched
    _description = None

    # Only fetch if needed
    _is_fetched = False

    def __init__(self, soup):
        self._set(soup)

    def _fetch(self):
        """
        Fetches detail page for app
        """
        self._is_fetched = True

        raw_html = get_raw_html(self.get_url())
        soup = BeautifulSoup(raw_html)

        self._set_description(soup)
        self._set_banner_icon(soup)

    def _set(self, soup):
        self._set_name(soup)
        self._set_url(soup)
        self._set_price(soup)
        self._set_thumbnail(soup)

    def _set_name(self, soup):
        link = soup('a', {'class': 'title'})[0]
        self._name = link.contents[0]

    def _set_url(self, soup):
        raw_url = soup('a', {'class': 'title'})[0]['href']
        url = "%s%s" % (BASE_URL, raw_url)
        self._url = url

    def _set_price(self, soup):
        price = soup('span', {'class': 'buy-button-price'})[0].contents[0]
        if price == 'Install':
            price = Decimal('0.00')
        else:
            p = price.split(' ')[0]
            if p.startswith('$'):
                price = Decimal(str(p[1:]))
            else:
                price = Decimal(str(p))
        self._price = price

    def _set_thumbnail(self, soup):
        thumbnail_div = soup('div', {'class': 'thumbnail-wrapper goog-inline-block'})[0]
        thumbnail = thumbnail_div('img')[0]['src']
        self._thumbnail = thumbnail

    def _set_description(self, soup):
        div = soup('div', {'class': 'doc-description toggle-overflow-contents'})[0]
        self._description = div.contents[0]

    def _set_banner_icon(self, soup):
        div = soup('div', {'class': 'doc-banner-icon'})[0]
        banner_icon = div('img')[0]['src']
        self._banner_icon = banner_icon

    def get_name(self):
        return self._name

    def get_url(self):
        return self._url

    def get_price(self):
        return self._price

    def get_thumbnail(self):
        return self._thumbnail

    @requires_fetch
    def get_description(self):
        return self._description

    @requires_fetch
    def get_banner_icon(self):
        return self._banner_icon

class Page(object):
    """
    Class for one page of search results
    """

    apps = []

    def __init__(self, page, query_string):
        self.page = page
        self.query_string = query_string

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

    def get_all_apps(self):
        """
        Gets all the apps on the page
        """
        apps = []
        items = self._get_items()
        for item in items:
            apps.append(App(item))
        return apps

class GooglePlay(object):
    """
    Class for searching the Google Play site

    This scrapes the site listed above under BASE_URL.

    TODO: Iterate over all pages
    """

    page = None

    def __init__(self, search=None):
        self.raw = None
        self.search = search
        self.query_string = QUERY_STRING
        self.query_string['q'] = search

    def _get_page(self, page):
        self.page = Page(page=page, query_string=self.query_string)
        return self.page

    def get_first_page(self):
        """
        Gets the first page of apps
        """
        page = self._get_page(1)
        return page.get_all_apps()

    def get_first(self):
        """
        Gets the first app on the first page
        """
        page = self._get_page(1)
        return page.get_all_apps()[0]