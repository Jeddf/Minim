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
          if url:
               t = urllib2.urlopen(url)
               self.raw = t.read()
               self.soup = BeautifulSoup(self.raw)

     def average_words(self):
          if self.articles:
               self.averages = {}
               for i in self.articles:
                    words = i['text'].split()
                    for t in words:
                         t = t.strip('(),.:;[]{}}]').title()
                         if t in self.averages:
                              self.averages[t] += 1
                         else:
                              self.averages[t] = 1
          self.averages = OrderedDict(sorted(self.averages.items(), key=lambda t: t[1]))

class ViceRSS(RSSobject):    # Vice Class tailored for vice.com/rss as of March 2014, returns 50 latest.
    def article_split(self):
        items = self.soup.find_all('item')
        self.articles = []
        for n, i in enumerate(items):
            i = str(i)
            i = i.replace(r'!', ' ')
            soop = BeautifulSoup(i)
            self.articles.append({'title': soop.title.string})
            t = soop.get_text(" ", strip=True)
            t = t.partition('[CDATA[')[2]
            self.articles[n]['text'] = t.partition('< --')[0]