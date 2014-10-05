from BBCUK import BBCRSSUK, 
from BBCUS import BBCRSSUS
from VICE import ViceRSS
from VOX import VoxRSS 
import sqlite3

# Crawl function, assumes 

def crawlSources(sites):
    borings = []
    for f in ["conjunctions", "prepositions", "determiners", "pronouns", "otherborings"]:
    with open("words/{}.csv".format(f), "r") as h:
        t = h.read()
        borings.extend(t.split())
    if not os.path.isfile("counts.db"):
        with sqlite3.connect('counts.db') as db:
            curs = db.cursor()
            with open('schema.sql', mode='r') as f:
                curs.executescript(f.read())
    i = []
    i.append(BBCRSSUK())
    i.append(BBCRSSUS())
    i.append(ViceRSS())
    i.append(VoxRSS())
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