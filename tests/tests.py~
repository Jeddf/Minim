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
    def test_article_href_record_vice(self):
        self.assertEqual('http://www.vice.com/read/cliven-bundy-is-now-americas-nightmare', self.vice.articles[2]['href'])

class BBCTest(unittest.TestCase):
    def setUp(self):
        self.bbc = RSSFeed.BBCRSS(None)
        with open('bbcus.xml', 'r') as rss:
            self.bbc.raw = rss.read()
            self.bbc.soup = BeautifulSoup(self.bbc.raw)
        self.bbc.article_split('BBC News US', 'http://bbc.co.uk/news', 5)
        self.bbc.average_words()
        with open('bbcarticlemay14.html', 'r') as art:
            self.art = art.read()
        self.artic = self.bbc.page_parse(self.art)
    def test_number_of_articles_bbc(self):
        self.assertEqual(len(self.bbc.articles), 5)
    def test_article_href_record_bbc(self):
        self.assertEqual('http://m.bbc.co.uk/news/magazine-27188642', self.bbc.articles[3]['href'])
    def test_title_parse_bbc(self):
        self.assertEqual('Turkey mine disaster: Tear gas fired at Soma protesters', self.artic['title'])
    def test_date_parse_bbc(self):
        self.assertEqual('16 May 2014', self.artic['date'])
    def test_text_content_bbc(self):
        self.assertEqual("ined' Several thousand demonstrators gathered in the ce", self.artic['text'][645:700])
    def test_text_length_bbc(self):
        self.assertEqual(2174, len(self.artic['text']))
        
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
    def test_article_href_record_vox(self):
        self.assertEqual('http://www.vox.com/2014/5/1/5671288/jobs-day-is-coming', self.vox.articles[1]['href'])

if __name__ == '__main__':
    unittest.main()