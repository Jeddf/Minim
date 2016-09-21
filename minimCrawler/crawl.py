import sys
import os
import pdb
import argparse
import pymysql.cursors

import parser as minimParser


def crawl(host, user, password, db, init):
    boringWords = []
    for wordType in ["conjunctions", "prepositions", "determiners", "pronouns", "otherborings"]:
        with open(os.path.abspath(sys.path[0] + "/words/{}.csv".format(wordType)), "r") as boringWordsNew:
            boringWordsNew = boringWordsNew.read()
            boringWords.extend(boringWordsNew.split())

    connection = pymysql.connect(host=host,
                                 user=user,
                                 password=password,
                                 db=db,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

    if init:
        with open(os.path.abspath(sys.path[0] + '/schema.sql'), 'r') as schema:
            with connection.cursor() as cursor:
                cursor.execute(schema.read())
    siteParsers = []
    siteParsers.append(minimParser.BBCRSS(**minimParser.sites['BBCUK']))
    siteParsers.append(minimParser.BBCRSS(**minimParser.sites['BBCUS']))
    siteParsers.append(minimParser.ViceRSS(**minimParser.sites['VICE']))
    siteParsers.append(minimParser.VoxRSS(**minimParser.sites['VOX']))
    try:
        for siteParser in siteParsers:
            siteParser.article_split()
            siteParser.average_words(boringWords)
            print(siteParser.sitename,siteParser.cumul,len(siteParser.articles),siteParser.sitefeed,siteParser.sitehome)
            with connection.cursor() as cursor:
                cursor.execute(
                    """INSERT into submits (sitename, cumul, articles, sitefeed, date, sitehome) VALUES('{0}', {1}, {2}, '{3}', NOW(), '{4}');""".format(
                        siteParser.sitename,
                        siteParser.cumul,
                        len(siteParser.articles),
                        siteParser.sitefeed,
                        siteParser.sitehome
                    )
                )
            connection.commit()
            with connection.cursor() as cursor:
                cursor.execute("SELECT MAX(id) FROM submits WHERE sitename='{}'".format(siteParser.sitename))
                submitId = cursor.fetchone()['MAX(id)']
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
                with connection.cursor() as cursor:
                    cursor.execute(
                        """INSERT into wordage (submitid, word, count, appears, max_article) VALUES({0}, \'{1}\', {2}, {3}, {4});""".format(
                            submitId,
                            word,
                            siteParser.averages[word],
                            x,
                            maxCountIndex
                        )
                    )
            for index, article in enumerate(siteParser.articles):
                with connection.cursor() as cursor:
                    cursor.execute(
                        """INSERT into articles (submitid, id, href) VALUES({0}, {1}, \'{2}\');""".format(
                            submitId,
                            index,
                            article['href']
                        )
                    )
            connection.commit()
    finally:
        connection.close()
    return 'Refreshed.'

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Crawl the webs and save to an sql database.')
    parser.add_argument('--host', help='mysql host')
    parser.add_argument('--user', help='mysql user')
    parser.add_argument('--password', help='mysql password')
    parser.add_argument('--db', help='mysql db')
    parser.add_argument('--init', default=False, help='initialize tables in database')

    args = parser.parse_args()

    crawl(**vars(args))
    print("Done.")