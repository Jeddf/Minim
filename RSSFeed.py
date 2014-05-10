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
               self.url = url
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
               
class ViceRSS(RSSobject):    # Vice Class tailored for vice.com/rss as of May 2014.
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

class VoxRSS(RSSobject):    # Vox Class tailored for vox.com/rss/index.xml as of May 2014
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

class BBCRSS(RSSobject):    # BBCNews Class tailored for feeds.bbci.co.uk/news/rss.xml as of May 2014
     def article_split(self):
          hinks = self.soup.find_all('link')
          bad = re.compile(r'(/news/\d|ws/in-pictures)')
          good = re.compile(r'ws/\S')
          links = []
          while hinks:
               a = hinks.pop()
               a = a.string
               a = a.partition('#')[0]
               a = a.replace('//www.', '//m.')
               if bad.search(a):
                    pass
               elif good.search(a):
                    links.append(a)
          big = " "
          self.articles=[]
          for n, href in enumerate(links):
               b = urlopen(href)
               r = b.read()
               p = BeautifulSoup(r)
               self.articles.append({})
               self.articles[n]['title'] = p.h1.string
               self.articles[n]['href'] = links[n]
               self.articles[n]['date'] = p.find(class_="date").string
               e = p.find(class_='story-inner')
               try:
                    tex = e.find_all('p') + e.find_all('ul')
               except AttributeError:
                    try:
                         e = p.find(class_='picture-gallery')
                         tex = e.find_all('p')
                    except AttributeError:
                         self.article[n]['text'] = "picture"
                         continue
               self.articles[n]['text'] = ""
               for h in tex[1:]:
                    self.articles[n]['text'] += " "+h.get_text()
     source = 'BBCNEWS'