import RSSFeed
import pdb
from bs4 import BeautifulSoup

g = RSSFeed.ViceRSS(None)
with open("vice.rss", "r") as f:
    g.raw = f.read()
    g.soup = BeautifulSoup(g.raw)
g.article_split()
g.average_words()
print len(g.averages)