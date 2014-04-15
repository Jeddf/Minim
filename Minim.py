from bs4 import BeautifulSoup
from flask import Flask, url_for, render_template, g
import os
import sqlite3
import RSSFeed

app = Flask(__name__)

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'counts.db'),
    DEBUG=True,
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

@app.route('/initdb')
def init_db():
    with sqlite3.connect('counts.db') as db:
        curs = db.cursor()
        with open('schema.sql', mode='r') as f:
            curs.executescript(f.read())
        db.commit()
    return 'initiated'

@app.route('/refresh')
def crawl():
    i = []
    i.append(RSSFeed.ViceRSS('http://www.vice.com/rss'))
    for t in i:
        t.article_split()
        t.average_words()
        with sqlite3.connect('counts.db') as db:
            curs = db.cursor()
            if curs.execute("""
                        SELECT source FROM submits
                        WHERE source = ? AND date=date('now')
                        ;""", ([t.source])).fetchall():
                return
            else:
                curs.execute("""
                         INSERT into submits (source, date)
                         VALUES(?, date('now')
                     );""", ([t.source]))
                for p in t.averages:
                    curs.execute("""
                             INSERT into wordage (word, count, submitid)
                             VALUES(?, ?, (SELECT id FROM submits
                             WHERE source=? AND date=date('now')))
                             ;""", (p, t.averages[p], t.source))
    return 'Refreshed.'
    
@app.route('/')
def home():
    sites=['VICE']
    logs={}
    with sqlite3.connect('counts.db') as db:
        curs = db.cursor()
        for site in sites:
            curs = db.execute("""SELECT word
                               FROM wordage
                               WHERE submitid ==
                               (SELECT MAX(id) from submits WHERE source=?)
                               ORDER BY count DESC
                               LIMIT 20""", ([sites[0]]))
            logs[site] = curs.fetchall()
            curs = db.execute("""SELECT count
                                FROM wordage
                                WHERE submitid ==
                                (SELECT MAX(id) from submits WHERE source=?)
                                ORDER BY count DESC
                                LIMIT 20""", ([sites[0]]))
            logs[site].extend(curs.fetchall())
    return render_template('home.html', logs=logs, sites=sites)

if __name__ == '__main__':
    app.run(host='0.0.0.0')