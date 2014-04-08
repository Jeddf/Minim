import urllib2
from bs4 import BeautifulSoup
import sqlite3

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
               t = urllib2.urlopen(url)
               self.raw = t.read()
               self.soup = BeautifulSoup(self.raw)
          with open("conjunctions.csv", "r") as h:
               t = h.read()               
               self.borings = t.split()
          with open("prepositions.csv", "r") as h:
               t = h.read()
               self.borings.extend(t.split())
          with open("determiners.csv", "r") as h:
               t = h.read()
               self.borings.extend(t.split())
          with open("pronouns.csv", "r") as h:
               t = h.read()
               self.borings.extend(t.split())
          with open("otherborings.csv", "r") as h:
               t = h.read()
               self.borings.extend(t.split())
               
     def average_words(self):
          if self.articles:
               self.averages = {}
               for i in self.articles:
                    words = i['text'].split()
                    for t in words:
                         t = t.strip(' (),.:;[]{}"\'').title()
                         if t in self.borings:
                              continue
                         if t == "":
                              continue
                         elif t in self.averages:
                              self.averages[t] += 1
                         else:
                              self.averages[t] = 1
               
               with sqlite3.connect("counts1.db") as conn:
                    cursin = conn.cursor()
                    if cursin.execute("""
                                      SELECT source FROM submits
                                      WHERE source = ? AND date=date('now')
                                      ;""", ([self.source])).fetchall():
                         return
                    else:
                         cursin.execute("""
                              INSERT into submits (source, date)
                              VALUES(?, date('now')
                              );""", ([self.source]))
                         for i in self.averages:
                              cursin.execute("""
                                  INSERT into wordage (word, count, submitid)
                                  VALUES(?, ?, (SELECT id FROM submits WHERE source=? AND date=date('now')))
                                  ;""", (i, self.averages[i], self.source))

class ViceRSS(RSSobject):    # Vice Class tailored for vice.com/rss as of March 2014, returns 50 latest.

     def article_split(self):
        items = self.soup.find_all('item')
        self.articles = []
        for n, i in enumerate(items):
            i = str(i)
            i = i.replace(r'!', ' ')
            i = i.decode("utf-8").replace(u'\u2019', "'").replace('   ', ' ').encode("utf-8")
            soop = BeautifulSoup(i)
            self.articles.append({'title': soop.title.string})
            t = soop.get_text(" ", strip=True)
            t = t.partition('[CDATA[')[2]
            self.articles[n]['text'] = t.partition('< --')[0]
     source = 'VICE'