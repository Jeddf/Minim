import pdb
from bs4 import BeautifulSoup
from flask import Flask, url_for, render_template, g
import os
import sqlite3
import RSSFeed

app = Flask(__name__)

i = []

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'counts.db'),
    DEBUG=True,
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

sites=['BBC News US', 'BBC News UK', 'Vice', 'Vox']

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
        bbcus = RSSFeed.BBCRSS(None)
        with open("bbcus.xml") as f:
            bbcus.raw = f.read()
            bbcus.soup = BeautifulSoup(bbcus.raw)
        i.append(bbcus)
    else:
        i.append(RSSFeed.BBCRSS('http://feeds.bbci.co.uk/news/rss.xml?edition=us'))
        i.append(RSSFeed.BBCRSS('http://feeds.bbci.co.uk/news/rss.xml?edition=uk'))
        i.append(RSSFeed.ViceRSS('http://www.vice.com/rss'))
        i.append(RSSFeed.VoxRSS('http://www.vox.com/rss/index.xml'))
    for n, t in enumerate(i):
        t.article_split(sitename=sites[n])
        t.average_words()
        with sqlite3.connect('counts.db') as db:
            curs = db.cursor()
            curs.execute("""
                                INSERT into submits (sitename, cumul, articles, sitefeed, date, sitehome)
                                VALUES(?, ?, ?, ?, date('now'), ?
                                );"""
                         , (t.sitename, t.cumul, len(t.articles), t.sitefeed, t.sitehome))
            for a in t.averages:
                x=0
                max_freq=0
                appear=0
                for u, r in enumerate(t.articles):
                    if a in r:
                        if r[a] > appear:
                            max_freq=u
                            appear = r[a]
                        x += 1
                curs.execute("""
                             INSERT into wordage (word, count, appears, max_article, submitid)
                             VALUES(?, ?, ?, ?,(SELECT MAX(id) FROM submits
                             WHERE sitename=?))
                             ;""", (a, t.averages[a], x, max_freq, t.sitename))
                max_freq=0
                appear=0
            for u, r in enumerate(t.articles):
                curs.execute("""
                             INSERT into articles (submitid, id, href, title, body)
                             VALUES((SELECT MAX(id) FROM submits WHERE sitename=?), ?, ?, ?, ?)
                             ;""", (t.sitename, u, r['href'], r['title'], r['text']))
    return 'Refreshed.'

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
            showratio = int(i[1]/10)
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
    app.run(host='0.0.0.0')
