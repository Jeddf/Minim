from bs4 import BeautifulSoup
import pdb
from .ParserBase import Parser


class VoxRSS(Parser):  # Vox Class tailored for www.vox.com/rss/index.xml, typically returns 10 latest.

    def article_split(self):
          entries = self.soup.find_all('entry')
          self.articles = []
          for index, entry in enumerate(entries):
               try:
                   entry = str(entry)
                   entrySoup = BeautifulSoup(entry, "lxml")
                   self.articles.append({})
                   self.articles[index]['title'] = entrySoup.title.string
                   self.articles[index]['href'] = entrySoup.id.string
                   self.articles[index]['date'] = entrySoup.updated.string
                   textSoup = BeautifulSoup(entrySoup.content.string, "html")
                   self.articles[index]['text'] = textSoup.get_text(" ", strip=True)
               except AttributeError:
                   pdb.set_trace()