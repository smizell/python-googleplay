# Google Play Search

This is a simple module for scraping the Google Play
search since there really isn't an API for it. There are 
several additional pieces of information that could be scraped
and added to this. 

## About

Currently, the following items are available for searching 
apps, books and movies in the Google Play store.

* Item name (name)
* Description (description)
* Url (url)
* Price (price)
* Thumbnail (thumbnail)
* Banner Icon (banner_icon)

Hopefully in the future, this will pull in the ratings and
links to screenshots.

Also, this currently only pulls the results from the first
page. Reason is this is used to find information for an item
and not for displaying search results. 

## Installation

Note: Beautiful Soup is required for scraping the HTML.

```
python setup.py install
```

## Usage

Examples for how to use this.


### For importing the module

```python
from google_play import GooglePlay
```

### Initialize the object

The default media type is 'apps'. So far, only apps, books, and
movies can be searched.

```python
app_search = GooglePlay(search='angry birds', media='apps')
book_search = GooglePlay(search='The Hobbit', media='books')
movie_search = GooglePlay(search='Casablanca', media='movies')
```

### All results from first page

```python
g = GooglePlay(search='angry birds')
g.get_first_page()
```

### Get first item in the search

```python
g = GooglePlay(search='angry birds')
app = g.get_first()
```

### Access the attributes for an item

Please refer to the about section of this file to
see what fields are available. To get the field for
an object, simply call get_attribute_name().

```python
g = GooglePlay(search='angry birds')
app = g.get_first()

app.get_name()
app.get_thumbnail()
```
