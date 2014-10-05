from bs4 import BeautifulSoup
from flask import Flask, render_template
import os, sqlite3, sources
from flask_frozen import Freezer
from crawl import crawlSources

app = Flask(__name__)

freezer = Freezer(app, False)

i = []

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'counts.db'),
    DEBUG=False
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

sites={'BBC News US':"http://feeds.bbci.co.uk/news/rss.xml?edition=us", 
    'BBC News UK':"http://feeds.bbci.co.uk/news/rss.xml?edition=uk", 
    'Vice':'http://www.vice.com/rss', 
    'Vox':'http://www.vox.com/rss/index.xml'} #Currently available site parsers

@app.route('/')
def home():
    logs={}
    with sqlite3.connect('counts.db') as db:
        curs = db.cursor()
        for site in sites:
            logs[site] = {}
            logs[site]['data'] = []
            curs = db.execute("""SELECT id, cumul, articles, sitefeed, date, sitehome
                               FROM submits
                               WHERE id ==
                               (SELECT MAX(id) from submits WHERE sitename=?)
                               """, ([site]))
            i = curs.fetchall()[0]
            submit_id = i[0]
            showratio = int(i[1]/3)
            logs[site]['data'] = {'cumul':i[1], 'articles':i[2], 'date':i[4], 'showratio':showratio, 'sitefeed':i[3], 'sitehome':i[5]}
            curs = db.execute("""SELECT word, count, appears, max_article
                               FROM wordage
                               WHERE submitid == ?
                               ORDER BY count DESC
                              """, ([submit_id]))
            l = curs.fetchall()
            logs[site]['words'] = []
            for r in l:
                thrd = round(i[2]/3)
                if r[2] < 3:
                    a = 1
                elif r[2] < thrd:
                    a = 2
                else:
                    a = 3
                logs[site]['words'].append({'word':r[0], 'counted':r[1], 'max_article':r[3], 'appears':a})
            logs[site]['articles'] = []
            curs = db.execute("""SELECT id, href, title
                                 FROM articles
                                 WHERE submitid == ?
                                 ORDER BY id ASC
                              """, ([submit_id]))
            l = curs.fetchall()
            for r in l:
                logs[site]['articles'].append({'id':r[0], 'href':r[1], 'title':r[2]})
    return render_template('home.html', logs=logs, sites=sites)

if __name__ == '__main__':
    crawlSources()
    freezer.freeze() # render html file to ./build directory
    # ensure 'build' dir contains css stylesheet and favicon
    print("Done.")