import urllib
from decimal import Decimal

from BeautifulSoup import BeautifulSoup

from google_play.conf import *
from google_play.decorators import requires_fetch
from google_play.utils import get_raw_html

class Item(object):

    # Only fetch if needed
    _is_fetched = False

    # Soup of the results page
    results_soup = None

    # Soup of the details page
    details_soup = None

    def __init__(self, soup):
        self.results_soup = soup
        self._set()

    def _fetch_details(self):
        self._set_description()
        #self._set_banner_icon()

    def _set(self):
        self._set_name()
        self._set_url()
        self._set_price()
        self._set_thumbnail()

    def _fetch(self):
        """
        Fetches detail page for app
        """
        self._is_fetched = True

        raw_html = get_raw_html(self.url)
        self.details_soup = BeautifulSoup(raw_html)

        if hasattr(self, '_fetch_details'):
            self._fetch_details()

    def _get_name(self):
        return self._name

    def _set_name(self):
        link = self.results_soup('a', {'class': 'title'})[0]
        self._name = link.contents[0]

    name = property(_get_name)

    def _get_url(self):
        return self._url

    def _set_url(self):
        raw_url = self.results_soup('a', {'class': 'title'})[0]['href']
        url = "%s%s" % (BASE_URL, raw_url)
        self._url = url

    url = property(_get_url)

    def _get_price(self):
        return self._price

    def _set_price(self):
        price = self.results_soup('span', {'class': 'buy-button-price'})[0].contents[0]
        if price == 'Install' or price == 'Free':
            price = Decimal('0.00')
        else:
            p = price.split(' ')[0]
            if p.startswith('$'):
                price = Decimal(str(p[1:]))
            else:
                price = Decimal(str(p))
        self._price = price

    price = property(_get_price)

    def _get_thumbnail(self):
        return self._thumbnail

    def _set_thumbnail(self):
        thumbnail_div = self.results_soup('div', {'class': 'thumbnail-wrapper goog-inline-block'})[0]
        thumbnail = thumbnail_div('img')[0]['src']
        self._thumbnail = thumbnail

    thumbnail = property(_get_thumbnail)

    @requires_fetch
    def _get_description(self):
        return self._description

    def _set_description(self):
        try:
            div = self.details_soup('div', {'class': 'doc-description toggle-overflow-contents'})[0]
            self._description = div.contents[0]
        except:
            self._description = ""

    description = property(_get_description)

    @requires_fetch
    def _get_banner_icon(self):
        return self._banner_icon

    def _set_banner_icon(self):
        div = self.details_soup('div', {'class': 'doc-banner-icon'})[0]
        banner_icon = div('img')[0]['src']
        self._banner_icon = banner_icon

    banner_icon = property(_get_banner_icon)
