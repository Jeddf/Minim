# RUN TO INITIATE DATABASE SCHEMA
import sqlite3

with sqlite3.connect("counts1.db") as conn:
    cursin = conn.cursor()
    cursin.execute("""CREATE TABLE submits
                   (id INTEGER PRIMARY KEY, source TEXT, date TEXT
                   );""")
    cursin.execute("""CREATE TABLE wordage
                   (submitid INTEGER,
                   word TEXT,
                   count TEXT,
                   FOREIGN KEY(submitid) REFERENCES submits(id)
                   );""")