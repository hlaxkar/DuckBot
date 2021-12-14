import sqlite3

conn = sqlite3.connect('youtube.db')

cur=conn.cursor()

cur.execute('select * from youtube ORDER BY rid DESC LIMIT 10')
for i in cur.fetchall():
  print(i[0],i[0:])

print('donr')
