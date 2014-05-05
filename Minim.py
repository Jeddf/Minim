from bs4 import BeautifulSoup
from flask import Flask, url_for, render_template, g
import os
import sqlite3
import RSSFeed

app = Flask(__name__)

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'counts.db'),
    DEBUG=False,
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

@app.route('/refresh/<offline>')
def crawl(offline=0):
    if not os.path.isfile("counts.db"):
        with sqlite3.connect('counts.db') as db:
            curs = db.cursor()
            with open('schema.sql', mode='r') as f:
                curs.executescript(f.read())
    i = []
    if offline == 1:
        vice = RSSFeed.ViceRSS(None)
        with open("vice.xml", "r") as f:
            vice.raw = f.read()
            vice.soup = BeautifulSoup(vice.raw)
        i.append(vice)
        vox = RSSFeed.VoxRSS(None)
        with open("index.xml", "r") as f:
            vox.raw = f.read()
            vox.soup = BeautifulSoup(vox.raw)
        i.append(vox)
        with open("bbcus.xml") as f:
            bbc.raw = f.read()
            bbc.soup = BeautifulSoup(bbc.raw)
        i.append(bbc)
    else:
        i.append(RSSFeed.BBCRSS('http://feeds.bbci.co.uk/news/rss.xml?edition=us'))
        i.append(RSSFeed.ViceRSS('http://www.vice.com/rss'))
        i.append(RSSFeed.VoxRSS('http://www.vox.com/rss/index.xml'))
    for t in i:
        t.article_split()
        t.average_words()
        if t.url:
            url = t.url
        else:
            url = 'http://google.com'
        with sqlite3.connect('counts.db') as db:
            curs = db.cursor()
            if curs.execute("""
                        SELECT source FROM submits
                        WHERE source = ? AND date=date('now')
                        ;""", ([t.source])).fetchall():
                return 'Already populated today.'
            else:
                curs.execute("""
                                INSERT into submits (source, cumul, articles, url, date)
                                VALUES(?, ?, ?, ?, date('now')
                                );"""
                            , (t.source, t.cumul, len(t.articles), url))
                for a in t.averages:
                    x=0
                    for r in t.articles:
                        if a in r:
                                x += 1
                    curs.execute("""
                             INSERT into wordage (word, count, appears, submitid)
                             VALUES(?, ?, ?, (SELECT id FROM submits
                             WHERE source=? AND date=date('now')))
                             ;""", (a, t.averages[a], x, t.source))
    return 'Refreshed.'

@app.route('/')
def home():
    sites=['BBCNEWS', 'VICE', 'VOX']
    logs={}
    with sqlite3.connect('counts.db') as db:
        curs = db.cursor()
        for site in sites:
            logs[site]=[]
            curs = db.execute("""SELECT id, cumul, articles, url, date
                               FROM submits
                               WHERE id ==
                               (SELECT MAX(id) from submits WHERE source=?)
                               """, ([site]))
            i = curs.fetchall()[0]
            submit_id = i[0]
            showratio = int(i[1]/10)
            logs[site].append({'cumul':i[1], 'articles':i[2], 'date':i[4], 'showratio':showratio, 'url':i[3]})
            curs = db.execute("""SELECT word, count, appears
                               FROM wordage
                               WHERE submitid == ?
                               ORDER BY count DESC
                              """, ([submit_id]))
            g = curs.fetchall()
            for r in g:
                thrd = round(i[2]/3)
                if r[2] < 3:
                    a = 1
                elif r[2] < thrd:
                    a = 2
                else:
                    a = 3
                logs[site].append({'word':r[0], 'counted':r[1], 'appears':a})
    return render_template('home.html', logs=logs, sites=sites)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
