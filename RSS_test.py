import unittest
from rss import RSSobject

class RSStester(unittest.Testcase):
    def setUp(self):
        self.RSS = RSSobject()

    def rss_connection_test(self):
        self.RSS.raw('http://feeds.bbci.co.uk/news/rss.xml')
        assert '<html>' in self.RSS.rss_page
