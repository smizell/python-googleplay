import unittest

from google_play import App, Book, Movie, GooglePlay

class ItemSearchTest(unittest.TestCase):

    def setUp(self):
        self.g = GooglePlay(search='angry birds')

    def test_get_first(self):
        """
        The name field should be populated once the
        Item object has been initiated.
        """
        item = self.g.get_first()
        self.assertNotEqual(None, item.name)

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
        after = item.description
        self.assertEqual(before, None)
        self.assertNotEqual(before, after)

class ItemSearch(unittest.TestCase):

    def test_app(self):
        g = GooglePlay(search='angry birds')
        item = g.get_first()
        self.assertTrue(isinstance(item, App))

    def test_book(self):
        g = GooglePlay(search='The Hobbit', media='books')
        item = g.get_first()
        self.assertTrue(isinstance(item, Book)) 
        
    def test_movie(self):
        g = GooglePlay(search='Casablanca', media='movies')
        item = g.get_first()
        self.assertTrue(isinstance(item, Movie))


if __name__ == '__main__':
    unittest.main()
