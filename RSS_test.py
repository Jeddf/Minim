import unittest
from RSSFeed import RSSobject, ViceRSS
from bs4.element import NavigableString
from bs4 import BeautifulSoup

class RSSViceTester(unittest.TestCase):
    
    def setUp(self):
        self.vice = ViceRSS(None)
        with open("vice.rss", "r") as f:
            self.vice.raw = f.read()
            self.vice.soup = BeautifulSoup(self.vice.raw)

    def test_vice_article_number(self):
        self.vice.article_split()
        self.assertEqual(len(self.vice.articles), 50)

    def test_vice_title_text(self):
        self.vice.article_split()
        self.assertEqual(self.vice.articles[2]['title'], "The Final Frontiers of Private-Issue New Age Music")

if __name__ == "__main__":
    unittest.main()