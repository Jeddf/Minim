from bs4 import BeautifulSoup

from ParserBase import Parser


class ViceRSS(Parser):    # Vice Class tailored for vice.com/rss, typically returns 50 latest.

    def article_split(self):
        items = self.soup.find_all('item')
        self.articles = []
        for index, item in enumerate(items):
            item = str(item)
            itemSoup = BeautifulSoup(item, "xml")
            self.articles.append({})
            self.articles[index]['title'] = itemSoup.title.string
            self.articles[index]['href'] = itemSoup.link.string
            try:
                self.articles[index]['date'] = itemSoup.pubdate.string
            except AttributeError:
                self.articles[index]['date'] = itemSoup.pubDate.string
            mainText = itemSoup.encoded.string
            mainTextSoup = BeautifulSoup(mainText, "html")
            self.articles[index]['text'] = mainTextSoup.get_text(" ", strip=True)