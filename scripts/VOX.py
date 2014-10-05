from ParserBase import Parser

class VoxRSS(Parser):  # Vox Class tailored for www.vox.com/rss/index.xml, typically returns 10 latest.
     
     def article_split(self, sitefeed="http://vox.com/rss/index.xml" sitename='Vox', sitehome='http://vox.com'):
          self.sitename = sitename
          self.sitehome = sitehome
          items = self.soup.find_all('entry')
          self.articles = []
          for n, i in enumerate(items):
               i = str(i)
               soop = BeautifulSoup(i, "xml")
               self.articles.append({})
               self.articles[n]['title'] = soop.title.string
               self.articles[n]['href'] = soop.id.string
               self.articles[n]['date'] = soop.updated.string
               cont = BeautifulSoup(soop.content.string, "html")
               self.articles[n]['text'] = cont.get_text(" ", strip=True)