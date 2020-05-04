import sqlite3
import os

# open("tweets.sqlite", 'w').close()

conn = sqlite3.connect("tweets.sqlite")
c = conn.cursor()

c.execute('''ALTER TABLE tweets
              ADD sentiment TEXT NULL''')
conn.commit()
conn.close()