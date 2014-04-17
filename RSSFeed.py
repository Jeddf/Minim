import sqlite3, Minim, re, string
from bs4 import BeautifulSoup
from urllib.request import urlopen

class RSSobject(object):
     """Base RSS parser class.
         Attributes:
           raw (str): raw code of website pull.
           soup (bs4.BeautifulSoup): Soup class instance of web pull.
           averages (collections.OrderedDict): sorted dictionary of words and their count in all articles of web pull.
           borings (list of strings): collected words to exclude
    """

     def __init__(self, url):
          if url:
               t = urlopen(url)
               self.raw = t.read()
               self.soup = BeautifulSoup(self.raw)
          self.borings = []
          for f in ["conjunctions", "prepositions", "determiners", "pronouns", "otherborings"]:
               with open("static/{}.csv".format(f), "r") as h:
                    t = h.read()               
                    self.borings.extend(t.split())
               
     def average_words(self):
          if self.articles:
               self.averages = {}
               ess = re.compile(r"'s")
               for i in self.articles:
                    words = i['text'].split()
                    for t in words:
                         t = t.strip(string.punctuation + '“”‘’')
                         t = t.strip(string.punctuation + '“”‘’').capitalize()
                         t = ess.sub('', t)
                         if t in self.borings:
                              continue
                         if t == "":
                              continue
                         elif t in self.averages:
                              self.averages[t] += 1
                         else:
                              self.averages[t] = 1
               
class ViceRSS(RSSobject):    # Vice Class tailored for vice.com/rss as of March 2014, returns 50 latest.

     def article_split(self):
        items = self.soup.find_all('item')
        self.articles = []
        for n, i in enumerate(items):
            i = str(i)
            i = i.replace(r'!', ' ')
            i = i.replace(u'\u2019', "'").replace('   ', ' ')
            soop = BeautifulSoup(i)
            self.articles.append({'title': soop.title.string})
            t = soop.get_text(" ", strip=True)
            t = t.partition('[CDATA[')[2]
            self.articles[n]['text'] = t.partition('< --')[0]
     source = 'VICE'