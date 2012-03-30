import urllib
from decimal import Decimal

from BeautifulSoup import BeautifulSoup

from google_play.conf import *
from google_play.decorators import requires_fetch
from google_play.utils import get_raw_html

class Item(object):

    # Only fetch if needed
    _is_fetched = False

    def __init__(self, soup):
        self._set(soup)

    def _fetch_details(self, soup):
        self._set_description(soup)
        self._set_banner_icon(soup)

    def _set(self, soup):
        self._set_name(soup)
        self._set_url(soup)
        self._set_price(soup)
        self._set_thumbnail(soup)

    def _fetch(self):
        """
        Fetches detail page for app
        """
        self._is_fetched = True

        raw_html = get_raw_html(self.get_url())
        soup = BeautifulSoup(raw_html)

        if hasattr(self, '_fetch_details'):
            self._fetch_details(soup)

    def _set_name(self, soup):
        link = soup('a', {'class': 'title'})[0]
        self._name = link.contents[0]

    def _set_url(self, soup):
        raw_url = soup('a', {'class': 'title'})[0]['href']
        url = "%s%s" % (BASE_URL, raw_url)
        self._url = url

    def _set_price(self, soup):
        price = soup('span', {'class': 'buy-button-price'})[0].contents[0]
        if price == 'Install' or price == 'Free':
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