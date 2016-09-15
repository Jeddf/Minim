import os
import sqlite3

from flask import Flask, render_template
from flask_frozen import Freezer
from crawl import crawlSources
from collections import OrderedDict

app = Flask(__name__)

freezer = Freezer(app, True)

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

orderedSites = OrderedDict(sorted(sites.items(), key=lambda t: t[0]))  # fix sites order alphabetically

@app.route('/')
def home():
    with sqlite3.connect('counts.db') as db:
        cursor = db.cursor()
        for site in orderedSites:
            orderedSites[site]['data'] = []
            cursor.execute(
                """
                    SELECT id, cumul, articles, sitefeed, date, sitehome
                    FROM submits
                    WHERE id ==
                    (SELECT MAX(id) from submits WHERE sitename=?)
                """, (
                    [orderedSites[site]['sitename']]
                )
            )
            latestData = cursor.fetchall()[0]
            submitId = latestData[0]
            showratio = int(latestData[1] / 6)

            orderedSites[site]['data'] = {
                'cumul': latestData[1],
                'articles': latestData[2],
                'date': latestData[4],
                'showratio': showratio,
                'sitefeed': latestData[3],
                'sitehome': latestData[5]
            }
            cursor = db.execute(
                """
                    SELECT word, count, appears, max_article
                    FROM wordage
                    WHERE submitid == ?
                    ORDER BY count DESC
                """, (
                    [submitId]
                )
            )
            words = cursor.fetchall()
            orderedSites[site]['words'] = []
            for word in words:
                wordArticleCount = word[2]
                thirdOfTotalArticleCount = round(orderedSites[site]['data']['articles'] / 3)
                if wordArticleCount < 3:
                    a = 1
                elif wordArticleCount < thirdOfTotalArticleCount:
                    a = 2
                else:
                    a = 3
                orderedSites[site]['words'].append({'word': word[0], 'counted': word[1], 'max_article': word[3], 'appears': a})
            orderedSites[site]['articles'] = []
            cursor = db.execute(
                """
                    SELECT id, href, title
                    FROM articles
                    WHERE submitid == ?
                    ORDER BY id ASC
                """, (
                    [submitId]
                )
            )
            articles = cursor.fetchall()
            for article in articles:
                orderedSites[site]['articles'].append({'id': article[0], 'href': article[1], 'title': article[2]})
    return render_template('home.html', sites = orderedSites)


if __name__ == '__main__':
    crawlSources(orderedSites)
    freezer.freeze()  # render html file to ./build directory
    # ensure 'build' dir contains css stylesheet and favicon
    print("Done.")
