import os
import sqlite3

from flask import Flask, render_template
from flask_frozen import Freezer
from crawl import crawlSources
from collections import OrderedDict

app = Flask(__name__)

freezer = Freezer(app, True)

i = []

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'counts.db'),
    DEBUG=True,
    FREEZER_DESTINATION='/var/www/minim.li'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

sites = {
    'BBCUS': {  # Currently available site parsers
    'sitename': 'BBC News US',
    'sitefeed': "http://feeds.bbci.co.uk/news/rss.xml?edition=us",
    'sitehome': 'http://bbc.com/news'
    }, 'BBCUK': {
    'sitename': 'BBC News UK',
    'sitefeed': "http://feeds.bbci.co.uk/news/rss.xml?edition=uk",
    'sitehome': 'http://bbc.co.uk/news'
    }, 'VICE': {
    'sitename': 'Vice',
    'sitefeed': 'http://www.vice.com/rss',
    'sitehome': 'http://vice.com'
    }, 'VOX': {
    'sitename': 'Vox',
    'sitefeed': 'http://www.vox.com/rss/index.xml',
    'sitehome': 'http://vox.com'
    }
}

orderedSites = OrderedDict(sorted(sites.items(), key=lambda t: t[0]))  # order sites alphabetically 

@app.route('/')
def home():
    with sqlite3.connect('counts.db') as db:
        curs = db.cursor()
        for site in orderedSites:
            orderedSites[site]['data'] = []
            curs = db.execute("""SELECT id, cumul, articles, sitefeed, date, sitehome
                               FROM submits
                               WHERE id ==
                               (SELECT MAX(id) from submits WHERE sitename=?)
                               """, ([orderedSites[site]['sitename']]))
            i = curs.fetchall()[0]
            submit_id = i[0]
            showratio = int(i[1] / 6)

            orderedSites[site]['data'] = {'cumul': i[1], 'articles': i[2], 'date': i[4], 'showratio': showratio,
                                   'sitefeed': i[3], 'sitehome': i[5]}
            curs = db.execute("""SELECT word, count, appears, max_article
                               FROM wordage
                               WHERE submitid == ?
                               ORDER BY count DESC
                              """, ([submit_id]))
            l = curs.fetchall()
            orderedSites[site]['words'] = []
            for r in l:
                thrd = round(i[2] / 3)
                if r[2] < 3:
                    a = 1
                elif r[2] < thrd:
                    a = 2
                else:
                    a = 3
                orderedSites[site]['words'].append({'word': r[0], 'counted': r[1], 'max_article': r[3], 'appears': a})
            orderedSites[site]['articles'] = []
            curs = db.execute("""SELECT id, href, title
                                 FROM articles
                                 WHERE submitid == ?
                                 ORDER BY id ASC
                              """, ([submit_id]))
            l = curs.fetchall()
            for r in l:
                orderedSites[site]['articles'].append({'id': r[0], 'href': r[1], 'title': r[2]})
    return render_template('home.html', sites=orderedSites)


if __name__ == '__main__':
    crawlSources(orderedSites)
    freezer.freeze()  # render html file to ./build directory
    # ensure 'build' dir contains css stylesheet and favicon
    print("Done.")
