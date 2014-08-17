CREATE TABLE submits(
       id INTEGER PRIMARY KEY NOT NULL, 
       sitename TEXT,
       cumul NUMBER,
       articles NUMBER,
       sitefeed TEXT,
       sitehome TEXT, 
       date TEXT
);

CREATE TABLE wordage (
       submitid INTEGER NOT NULL,
       word TEXT NOT NULL,
       count INTEGER,
       max_article INTEGER NOT NULL,
       appears INTEGER,
       FOREIGN KEY(submitid) REFERENCES submits(id) ON DELETE CASCADE
);

CREATE TABLE articles (
       submitid INTEGER NOT NULL,
       id INTEGER NOT NULL,
       href TEXT NOT NULL,
       title TEXT,
       body TEXT,
       FOREIGN KEY(submitid) REFERENCES submits(id) ON DELETE CASCADE
);