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

     def __init__(self, sitefeed):
          if sitefeed:
               t = urlopen(sitefeed)
               self.raw = t.read()
               self.soup = BeautifulSoup(self.raw)
               self.sitefeed = sitefeed
          else:
               self.sitefeed = 'http://google.com'
          self.borings = []
          for f in ["conjunctions", "prepositions", "determiners", "pronouns", "otherborings"]:
               with open("/static/{}.csv".format(f), "r") as h:
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
                         if t in self.averages:
                              self.averages[t] += 1
                              if t in self.articles[x]:
                                   self.articles[x][t] += 1
                              else:
                                   self.articles[x][t] = 1
                         
                         else:
                              self.averages[t] = 1
                              self.articles[x][t] = 1
               self.cumul = len(self.averages)
               
class ViceRSS(RSSobject):    # Vice Class tailored for vice.com/rss as of March 2014, returns 50 latest.

     def article_split(self, sitename='Vice', sitehome='http://vice.com'):
          self.sitename = sitename
          self.sitehome = sitehome
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

class VoxRSS(RSSobject):
     def article_split(self, sitename='Vox', sitehome='http://vox.com'):
          self.sitename = sitename
          self.sitehome = sitehome
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

class BBCRSS(RSSobject):
     def article_split(self, sitename='BBC News US', sitehome='http://bbc.com/news', maxart=80):
          self.sitename = sitename
          self.sitehome = sitehome
          hinks = self.soup.find_all('link')
          bad = re.compile(r'(/news/\d|ws/in-pictures)')
          good = re.compile(r'ws/\S')
          links = []
          while hinks and (len(links) < maxart):
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
               self.articles.append(self.page_parse(r))
               self.articles[n]['href'] = href
     def page_parse(self, r):
          p = BeautifulSoup(r)
          article={}
          article['title'] = p.h1.get_text()
          if p.find(class_="date"):
               article['date'] = p.find(class_="date").get_text().strip()[0:11]
          else:
               article['date'] = " "
          d = p.find(class_='map-body')
          e = p.find(class_='story-inner')
          f = p.find(class_='story-body')
          g = p.find(class_='picture-gallery')
          if f:
               tex = f.find_all('p') + f.find_all('ul')
          elif d:
               tex = d.find_all('p') + e.find_all('ul')
          elif e:
               tex = e.find_all('p') + e.find_all('ul')
          elif g:
               tex = g.find_all('p')
          article['text'] = ""
          try:
               for h in tex:
                    try:
                         if 'date' in h['class']:
                              continue
                    except KeyError:
                         pass
                    article['text'] += " "+h.get_text()
          except NameError:
               article['text'] += "{}fail".format(links[n][-8:])
          return article
