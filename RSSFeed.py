import urllib2
from bs4 import BeautifulSoup
from collections import OrderedDict

class RSSobject(object):
     """Base RSS parser class.
         Attributes:
           raw (str): raw code of website pull.
           soup (bs4.BeautifulSoup): Soup class instance of web pull.
           averages (collections.OrderedDict): sorted dictionary of words           and their count in all articles of web pull.
    """
     def __init__(self, url):
          t = urllib2.urlopen(url)
          self.raw = t.read()
          self.soup = BeautifulSoup(self.raw)

     def average_words(self):
          if self.articles:
               self.averages = {}
               for i in self.articles:
                    words = i['text'].split()
               for t in words:
                    if t in self.averages:
                         self.averages[t] += 1
                    else:
                         self.averages[t] = 1
          self.averages = OrderedDict(sorted(self.averages.items(), key=lambda t: t[1]))

class ViceRSS(RSSobject):    # Vice Class tailored for site structure
    def article_split(self):    # Split feed into articles
        items = self.soup.find_all('item')    # <item> contents into list
        self.articles = []   # Initiate dump for data
        for n, i in enumerate(items):
            i = str(i)    # Convert soup object to string
            i = i.replace(r'!', ' ')    # Takeout ! so soup will parse
            soop = BeautifulSoup(i)    # Cook soup
            self.articles.append({'title': soop.title.string})    # Title save
            t = soop.get_text(" ", strip=True)    # Get contents of all tags and return in 1 string seperated by space
            t = t.partition('[CDATA[')[2]    # Trim leading and following fluff
            self.articles[n]['text'] = t.partition('< --')[0]