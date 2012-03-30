from google_play.base import Item

class App(Item):
    """
    Class for App
    """
    # Can be set from original soup
    _name = None
    _url = None
    _price = None
    _category = None

    # Only on detail page, must be fetched
    _description = None

class Book(Item):
    """
    Class for Book
    """

    # Can be set from original soup
    _name = None
    _price = None
    _author = None
    _url = None

    # Only on detail page, must be fetched
    _description = None

class Movie(Item):
    """
    Class for Movie
    """

    # Can be set from original soup
    _name = None
    _price = None
    _url = None

    # Only on detail page, must be fetched
    _description = None