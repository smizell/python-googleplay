import urllib

def get_raw_html(url):
    return urllib.urlopen(url).read()