#!/usr/bin/python

# we've been outputting stuff to text so now I get to wedge it into a database
# funtimes

# set up the database with `sqlite3 netflix_genres.sqlite < create_tables.sql`

import codecs
import sqlite3
import sys

conn = sqlite3.connect('netflix_genres.sqlite')
c = conn.cursor()

# for row in c.execute('SELECT id, info FROM movies'):
#     db_id = row[0]
#     info = row[1].split(',')
#     movie_id = info[0]
#     updates.append((movie_id, db_id))
# 
# # print updates
# 
# for update in updates:
#     print update
#     c.execute('UPDATE movies SET movie_id=? WHERE id=?', update)

c.execute('SELECT DISTINCT (movie_id) FROM movies ORDER BY movie_id')
movie_ids = c.fetchall()

inserts = []

for row in movie_ids:
    movie_id = row[0]
    name = cover_url = movie_url = None
    genre_ids = []
    for entry in c.execute('SELECT id, name, cover_url, movie_url, genres FROM movies WHERE movie_id = ?', (movie_id,)):
        if not name:
            name = entry[1]
        if name != entry[1]:
            print "Row %s has variant name (%s not %s)" % (entry[0], entry[1], name)
        cover_url = cover_url or entry[2]
        movie_url = movie_url or entry[3]
        genre_ids.append("%05i" % int(entry[4]))

        # print entry
    genres = ','.join(genre_ids)
    print (movie_id, name)
    inserts.append((name, cover_url, movie_url, genres))

#print inserts

print "... Inserting"

c.executemany('INSERT INTO movies_n (name, cover_url, movie_url, genres) VALUES(?,?,?,?)', inserts)

conn.commit()
conn.close()
