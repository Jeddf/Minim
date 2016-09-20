import argparse

from collections import OrderedDict

from flask import Flask, render_template
from flask_mysqldb import MySQL
from flask_frozen import Freezer

import minimCrawler

app = Flask(__name__)
mysql = MySQL(app)

freezer = Freezer(app, True)

app.config.update(dict(
    DEBUG=True,
    FREEZER_DESTINATION='build',
    FREEZER_REMOVE_EXTRA_FILES=False
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

orderedSites = OrderedDict(sorted(minimCrawler.sites.items(), key=lambda t: t[0]))  # fix sites order alphabetically

@app.route('/')
def home():
    db = mysql.connection
    for site in orderedSites:
        orderedSites[site]['data'] = []
        cursor = db.cursor()
        cursor.execute("SELECT MAX(id) FROM submits WHERE sitename='{}'".format(orderedSites[site]['sitename']))
        submitId = cursor.fetchone()[0]
        print("SELECT MAX(id) FROM submits WHERE sitename='{}'".format(orderedSites[site]['sitename']))
        cursor.close()
        cursor = db.cursor()
        cursor.execute(
            """
                SELECT id, cumul, articles, sitefeed, date, sitehome
                FROM submits
                WHERE id = {}
            """.format(
                submitId
            )
        )
        latestData = cursor.fetchall()[0]
        cursor.close()
        showratio = int(latestData[1] / 6)

        orderedSites[site]['data'] = {
            'cumul': latestData[1],
            'articles': latestData[2],
            'date': latestData[4],
            'showratio': showratio,
            'sitefeed': latestData[3],
            'sitehome': latestData[5]
        }
        cursor = db.cursor()
        cursor.execute(
            """
                SELECT word, count, appears, max_article
                FROM wordage
                WHERE submitid = {}
                ORDER BY count DESC
            """.format(submitId)
        )
        words = cursor.fetchall()
        cursor.close()
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
        cursor = db.cursor()
        cursor.execute(
            """
                SELECT id, href
                FROM articles
                WHERE submitid = {}
                ORDER BY id ASC
            """.format(submitId)
        )
        articles = cursor.fetchall()
        cursor.close()
        for article in articles:
            orderedSites[site]['articles'].append({'id': article[0], 'href': article[1]})
    return render_template('home.html', sites = orderedSites)

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Render out HTML minim page from a mysql source.')
    parser.add_argument('--host', default='localhost', help='mysql host')
    parser.add_argument('--user', default='localhost', help='mysql user')
    parser.add_argument('--password', default='localhost', help='mysql password')
    parser.add_argument('--db', default='db', help='mysql db')

    args = parser.parse_args()

    app.config.update(dict(
        MYSQL_HOST=args.host,
        MYSQL_USER=args.user,
        MYSQL_PASSWORD=args.password,
        MYSQL_DB=args.db
    ))

    freezer.freeze()  # render html file to ./build directory
    print("Done.")
