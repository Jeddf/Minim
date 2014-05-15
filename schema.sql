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
       count NUMBER,
       appears NUMBER,
       FOREIGN KEY(submitid) REFERENCES submits(id) ON DELETE CASCADE
);