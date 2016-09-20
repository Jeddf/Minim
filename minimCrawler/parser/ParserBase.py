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
        rawSite = urlopen(self.sitefeed)
        self.raw = rawSite.read()
        self.soup = BeautifulSoup(self.raw, "xml")

    # Step through words in each article, form overall counts. Expects: list of dictionaries at self.articles, each containing 'text' string.
    def average_words(self, boringWords):
        if self.articles:
            self.averages = {}
            pluralPattern1 = re.compile(r"'s")  # down with esses!
            pluralPattern2 = re.compile(r"’s")  # and essses.
            aposterousPattern = re.compile(r"'")
            for x, i in enumerate(self.articles):
                words = i['text'].split()
                for word in words:
                    word = word.strip(string.punctuation + '“”‘’\'')
                    word = word.strip(string.punctuation + '“”‘’\'').capitalize()
                    word = pluralPattern1.sub('', word)
                    word = pluralPattern2.sub('', word)
                    word = aposterousPattern.sub('', word)
                    if word in boringWords:
                        continue
                    if "='" in word:
                        continue
                    if word == "":
                        continue
                    if word in self.averages:
                        self.averages[word] += 1
                        if word in self.articles[x]:
                            self.articles[x][word] += 1
                        else:
                            self.articles[x][word] = 1

                    else:
                        self.averages[word] = 1
                        self.articles[x][word] = 1
            self.cumul = len(self.averages)