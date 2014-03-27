import RSSFeed
import pdb

g = RSSFeed.ViceRSS('http://www.jeddfenner.com/vice.xml')
g.article_split()
g.average_words()
print 'raw type: ', type(g.raw)
print 'soup type: ', type(g.soup)
print 'averages type: ', type(g.averages)