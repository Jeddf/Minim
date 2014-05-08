import unittest, RSSFeed, re
from bs4 import BeautifulSoup

class ViceTest(unittest.TestCase):
    def setUp(self):
        self.vice = RSSFeed.ViceRSS(None)
        with open('vice.xml', 'r') as rss:
            self.vice.raw = rss.read()
            self.vice.soup = BeautifulSoup(self.vice.raw)
        self.vice.article_split()
        self.vice.average_words()
    def test_number_of_articles_vice(self):
        self.assertEqual(len(self.vice.articles), 50)

class BBCTest(unittest.TestCase):
    def setUp(self):
        self.bbcus = RSSFeed.BBCRSS(None)
        with open('bbcus.xml', 'r') as rss:
            self.bbcus.raw = rss.read()
            self.bbcus.soup = BeautifulSoup(self.bbcus.raw)
        self.bbcus.article_split(5)
        self.bbcus.average_words()
    def test_number_of_articles_bbc(self):
        self.assertEqual(len(self.bbcus.articles), 5)

class VoxTest(unittest.TestCase):
    def setUp(self):
        self.vox = RSSFeed.VoxRSS(None)
        with open('vox.xml', 'r') as rss:
            self.vox.raw = rss.read()
            self.vox.soup = BeautifulSoup(self.vox.raw)
        self.vox.article_split()
        self.vox.average_words()
    def test_number_of_articles_vox(self):
        self.assertEqual(len(self.vox.articles), 10)
if __name__ == '__main__':
    unittest.main()