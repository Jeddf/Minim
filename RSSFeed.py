import sqlite3, Minim, re, string, pdb
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
               esss = re.compile(r"’s")
               for x, i in enumerate(self.articles):
                    words = i['text'].split()
                    for t in words:
                         t = t.strip(string.punctuation + '“”‘’')
                         t = t.strip(string.punctuation + '“”‘’').capitalize()
                         t = ess.sub('', t)
                         t = esss.sub('', t)
                         if t in self.borings:
                              continue
                         if t == "":
                              continue
                         elif t in self.averages:
                              self.averages[t] += 1
                         else:
                              self.averages[t] = 1
                         self.articles[x][t] = 1
               self.cumul = sum(self.averages.values())
               
class ViceRSS(RSSobject):    # Vice Class tailored for vice.com/rss as of March 2014, returns 50 latest.

     def article_split(self):
        items = self.soup.find_all('item')
        self.articles = []
        for n, i in enumerate(items):
            i = str(i)
            i = i.replace(r'!', ' ')
            i = i.replace(r'–', ' ')
            soop = BeautifulSoup(i)
            self.articles.append({})
            self.articles[n]['title'] = soop.title.string
            self.articles[n]['href'] = soop.link.string
            self.articles[n]['date'] = soop.pubdate.string
            t = soop.get_text(" ", strip=True)
            t = t.partition('[CDATA[')[2]
            self.articles[n]['text'] = t.partition('< --')[0]
     source = 'VICE'

class VoxRSS(RSSobject):
     def article_split(self):
          items = self.soup.find_all('entry')
          self.articles = []
          for n, i in enumerate(items):
               i = str(i)
               soop = BeautifulSoup(i)
               self.articles.append({})
               self.articles[n]['title'] = soop.title.string
               self.articles[n]['href'] = soop.id.string
               self.articles[n]['date'] = soop.updated.string
               cont = BeautifulSoup(soop.content.string)
               self.articles[n]['text'] = cont.get_text(" ", strip=True)
     source = 'VOX'
     