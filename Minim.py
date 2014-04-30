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
        g = RSSFeed.ViceRSS(None)
        with open("vice.rss", "r") as f:
            g.raw = f.read()
            g.soup = BeautifulSoup(g.raw)
        i.append(g)
    else:
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
                return 'Already populated today.'
            else:
                curs.execute("""
                                INSERT into submits (source, cumul, articles, date)
                                VALUES(?, ?, ?, date('now')
                                );"""
                            , (t.source, t.cumul, len(t.articles)))
                for a in t.averages:
                    x=0
                    for r in t.articles:
                        if a in r:
                            if x < 8:
                                x += 1
                    curs.execute("""
                             INSERT into wordage (word, count, appears, submitid)
                             VALUES(?, ?, ?, (SELECT id FROM submits
                             WHERE source=? AND date=date('now')))
                             ;""", (a, t.averages[a], x, t.source))
    return 'Refreshed.'

@app.route('/')
def home():
    sites=['VICE']
    logs={}
    with sqlite3.connect('counts.db') as db:
        curs = db.cursor()
        for site in sites:
            logs[site]=[]
            curs = db.execute("""SELECT id, cumul, articles, date
                               FROM submits
                               WHERE id ==
                               (SELECT MAX(id) from submits WHERE source=?)
                               """, ([site]))
            i = curs.fetchall()[0]
            submit_id = i[0]
            logs[site].append({'cumul':i[1], 'articles':i[2], 'date':i[3]})
            curs = db.execute("""SELECT word, count, appears
                               FROM wordage
                               WHERE submitid == ?
                               ORDER BY count DESC
                              """, ([submit_id]))
            g = curs.fetchall()
            for i in g:
                logs[site].append({'word':i[0], 'counted':i[1], 'appears':i[2]})
    return render_template('home.html', logs=logs, sites=sites)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
