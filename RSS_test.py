import unittest
from RSSFeed import RSSobject, ViceRSS

class RSSTester(unittest.TestCase):

    def setUp(self):
        self.RSS = RSSobject('http://feeds.bbci.co.uk/news/rss.xml')

    def rss_raw_page_test(self):
        assert '<?xml' in self.RSS.raw

    #def rss_soup_page_test(self):
    #    assert 'BBC' in self.RSS.soup.title.string

class RSSViceTester(unittest.TestCase):
    
    def setUp(self):
        self.vice = ViceRSS('http://www.vice.com/rss')

    def vice_article_list_test(self):
        self.vice.article_split()
        self.assertEqual(type(self.vice.articles), list)

    def vice_article_text_test(self):
        self.vice.article_split()
        self.assertEqual(type(self.vice.articles[0]['title']), str)
