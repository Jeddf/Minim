import unittest
from RSSFeed import RSSobject, ViceRSS

class RSSTester(unittest.TestCase):

    def setUp(self):
        self.RSS = RSSobject('http://feeds.bbci.co.uk/news/rss.xml')

    def rss_raw_page_test(self):
        self.assert '<?xml' in self.RSS.raw

    def rss_soup_page_test(self):
        self.assert 'BBC' in self.RSS.soup.title.string

class RSSViceTester(unittest.TestCase):
    
    def setUp(self):
        self.Vice = ViceRSS()

    def vice_article_text_split_test(self):
        result = self.Vice.article_split()
        self.assertEqual(type(result), dict)
