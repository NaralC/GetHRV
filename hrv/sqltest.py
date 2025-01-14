import sqlite3

conn = sqlite3.connect('measures.db')
c = conn.cursor()

c.execute("SELECT * FROM measures")
print(c.fetchall())

