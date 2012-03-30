import unittest

from google_play import App, GooglePlay

class TestSearch(unittest.TestCase):
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
        app = self.g.get_first()
        self.assertTrue(isinstance(app, App))
        self.assertNotEqual(None, app.get_name())

    def test_get_first_page(self):
        """
        Each page should have 24 apps on it.
        """
        apps = self.g.get_first_page()
        self.assertEqual(len(apps), 24)

    def test_fetch_for_app(self):
        """
        The fetch method for an App object only fetches
        the detail page when a field on that page is requested.
        Description is one that is on that page, and should 
        be None before get_description() is ever ran.
        """
        app = self.g.get_first()
        before = app._description
        after = app.get_description()
        self.assertEqual(before, None)
        self.assertNotEqual(before, after)

if __name__ == '__main__':
    unittest.main()
