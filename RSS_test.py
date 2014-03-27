import unittest
from RSSFeed import RSSobject, ViceRSS
from bs4.element import NavigableString
from bs4 import BeautifulSoup

class RSSTester(unittest.TestCase):

    def setUp(self):
        self.RSS = RSSobject('http://feeds.bbci.co.uk/news/rss.xml')

    def test_rss_raw_page(self):
        assert '<?xml' in self.RSS.raw

    #def rss_soup_page_test(self):
    #    assert 'BBC' in self.RSS.soup.title.string

class RSSViceTester(unittest.TestCase):
    
    def setUp(self):
        self.vice = ViceRSS(None)
        with open("vice.rss", "r") as f:
            self.vice.raw = f.read()
            self.vice.soup = BeautifulSoup(self.vice.raw)


    def test_vice_article_list(self):
        self.vice.article_split()
        self.assertEqual(type(self.vice.articles), list)

    def test_vice_article_text(self):
        self.vice.article_split()
        self.assertEqual(type(self.vice.articles[0]['title']), NavigableString)

if __name__ == "__main__":
    unittest.main()
