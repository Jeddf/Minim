import re
import string
from urllib.request import urlopen

from bs4 import BeautifulSoup


class Parser(object):
    """Base article parser class.
        Attributes:
          raw (str): raw code of RSS feed pull.
          soup (bs4.BeautifulSoup): Soup class instance of web pull.
          averages (dict: sorted dictionary of words and their count in all articles of web pull.
   """

    # Pull URL contents to self.raw[str] and soup it to self.soup[str]. read filter words into list object[list of str's].
    def __init__(self, sitefeed, sitename, sitehome):
        self.sitefeed = sitefeed
        self.sitehome = sitehome
        self.sitename = sitename
        t = urlopen(self.sitefeed)
        self.raw = t.read()
        self.soup = BeautifulSoup(self.raw, "xml")

    # Step through words in each article, form overall counts. Expects: list of dictionaries at self.articles, each containing 'text' string.
    def average_words(self, borings):
        if self.articles:
            self.averages = {}
            ess = re.compile(r"'s")  # down with esses!
            esss = re.compile(r"’s")  # and essses.
            for x, i in enumerate(self.articles):
                words = i['text'].split()
                for t in words:
                    t = t.strip(string.punctuation + '“”‘’')
                    t = t.strip(string.punctuation + '“”‘’').capitalize()
                    t = ess.sub('', t)
                    t = esss.sub('', t)
                    if t in borings:
                        continue
                    if "='" in t:
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
