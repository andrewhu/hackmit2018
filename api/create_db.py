import sqlite3
import os

open("tweets.sqlite", 'w').close()

conn = sqlite3.connect("tweets.sqlite")
c = conn.cursor()

c.execute('''CREATE TABLE tweets
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
             tweet_id TEXT,
             created_at TEXT,
              coords TEXT,
              body TEXT)''')
conn.commit()
conn.close()