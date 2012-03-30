import unittest

from google_play import App, Book, Movie, GooglePlay

class AppSearch(unittest.TestCase):
    """
    Tests for GooglePlay
    """

    def setUp(self):
        self.g = GooglePlay(search='angry birds')

    def test_get_first(self):
        """
        The name field should be populated once the
        App object has been initiated.
        """
        item = self.g.get_first()
        self.assertTrue(isinstance(item, App))
        self.assertNotEqual(None, item.get_name())

    def test_get_first_page(self):
        """
        Each page should have some items.
        """
        items = self.g.get_first_page()
        self.assertGreater(len(items), 0)

    def test_fetch(self):
        """
        The fetch method for an Item object only fetches
        the detail page when a field on that page is requested.
        Description is one that is on that page, and should 
        be None before get_description() is ever ran.
        """
        item = self.g.get_first()
        before = item._description
        after = item.get_description()
        self.assertEqual(before, None)
        self.assertNotEqual(before, after)

class BookSearch(unittest.TestCase):

    def setUp(self):
        self.g = GooglePlay(search='The Hobbit', media='books')

    def test_get_first(self):
        """
        The name field should be populated once the
        Book object has been initiated.
        """
        item = self.g.get_first()
        self.assertTrue(isinstance(item, Book))
        self.assertNotEqual(None, item.get_name())

    def test_get_first_page(self):
        """
        Each page should have some items.
        """
        items = self.g.get_first_page()
        self.assertGreater(len(items), 0)

    def test_fetch(self):
        """
        The fetch method for an Item object only fetches
        the detail page when a field on that page is requested.
        Description is one that is on that page, and should 
        be None before get_description() is ever ran.
        """
        item = self.g.get_first()
        before = item._description
        after = item.get_description()
        self.assertEqual(before, None)
        self.assertNotEqual(before, after)

class MovieSearch(unittest.TestCase):

    def setUp(self):
        self.g = GooglePlay(search='Casablanca', media='movies')

    def test_get_first(self):
        """
        The name field should be populated once the
        App object has been initiated.
        """
        item = self.g.get_first()
        self.assertTrue(isinstance(item, Movie))
        self.assertNotEqual(None, item.get_name())

    def test_get_first_page(self):
        """
        Each page should have some items.
        """
        items = self.g.get_first_page()
        self.assertGreater(len(items), 0)

    def test_fetch(self):
        """
        The fetch method for an Item object only fetches
        the detail page when a field on that page is requested.
        Description is one that is on that page, and should 
        be None before get_description() is ever ran.
        """
        item = self.g.get_first()
        before = item._description
        after = item.get_description()
        self.assertEqual(before, None)
        self.assertNotEqual(before, after)

if __name__ == '__main__':
    unittest.main()
