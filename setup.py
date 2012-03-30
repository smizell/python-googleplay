import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "google_play",
    version = "0.1",
    author = "Stephen Mizell",
    author_email = "smizell@gmail.com",
    description = ("Simple module for scraping Google Play search"),
    license = "http://www.gnu.org/licenses/gpl.html",
    keywords = "google play",
    url = "https://github.com/smizell/python-googleplay",
    packages=['google_play'],
    long_description=read('README.md'),
    install_requires=['BeautifulSoup']
)