import sqlite3
import os

from BBCUK import BBCRSSUK
from BBCUS import BBCRSSUS
from VICE import ViceRSS
from VOX import VoxRSS


def crawlSources(sites):
    boringWords = []
    for wordType in ["conjunctions", "prepositions", "determiners", "pronouns", "otherborings"]:
        with open("words/{}.csv".format(wordType), "r") as boringWordsNew:
            boringWordsNew = boringWordsNew.read()
            boringWords.extend(boringWordsNew.split())
    if not os.path.isfile("counts.db"):
        with sqlite3.connect('counts.db') as db:
            cursor = db.cursor()
            with open('schema.sql', mode='r') as wordType:
                cursor.executescript(wordType.read())
    siteParsers = []
    siteParsers.append(BBCRSSUK(**sites['BBCUK']))
    siteParsers.append(BBCRSSUS(**sites['BBCUS']))
    siteParsers.append(ViceRSS(**sites['VICE']))
    siteParsers.append(VoxRSS(**sites['VOX']))
    for siteParser in siteParsers:
        siteParser.article_split()
        siteParser.average_words(boringWords)
        with sqlite3.connect('counts.db') as db:
            cursor = db.cursor()
            cursor.execute(
                """
                    INSERT into submits (sitename, cumul, articles, sitefeed, date, sitehome)
                    VALUES(?, ?, ?, ?, date('now'), ?
                    );
                """, (
                siteParser.sitename,
                siteParser.cumul,
                len(siteParser.articles),
                siteParser.sitefeed,
                siteParser.sitehome)
            )
            for word in siteParser.averages:
                x=0
                maxCountIndex=0
                maxCount=0
                for index, article in enumerate(siteParser.articles):
                    if word in article:
                        if article[word] > maxCount:
                            maxCountIndex = index
                            maxCount = article[word]
                        x += 1
                cursor.execute(
                    """
                        INSERT into wordage (word, count, appears, max_article, submitid)
                        VALUES(?, ?, ?, ?,(SELECT MAX(id) FROM submits
                        WHERE sitename=?));
                    """, (
                    word,
                    siteParser.averages[word],
                    x,
                    maxCountIndex, siteParser.sitename)
                )
            for index, article in enumerate(siteParser.articles):
                cursor.execute(
                    """
                        INSERT into articles (submitid, id, href, title, body)
                        VALUES((SELECT MAX(id) FROM submits WHERE sitename=?), ?, ?, ?, ?);
                    """, (
                    siteParser.sitename,
                    index,
                    article['href'],
                    article['title'],
                    article['text'])
                )
    return 'Refreshed.'