import urllib2
from bs4 import BeautifulSoup

class RSSobject(object):
    def __init__(self, url):
        f = urllib2.urlopen(url)
        self.raw = f.read()
