import RSSFeed
import pdb

g = RSSFeed.ViceRSS('http://www.jeddfenner.com/vice.xml')
g.article_split()
g.average_words()
print g.averages