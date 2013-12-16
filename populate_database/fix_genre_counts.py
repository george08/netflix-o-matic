#!/usr/bin/python

# we've been outputting stuff to text so now I get to wedge it into a database
# funtimes

# set up the database with `sqlite3 netflix_genres.sqlite < create_tables.sql`

import codecs
import sqlite3
import sys

conn = sqlite3.connect('netflix.sqlite')
c = conn.cursor()

c.execute('SELECT genre_id, name, movie_count FROM genres WHERE name != "" ORDER BY name')
genres = c.fetchall()

updates = []

for genre in genres:
    (genre_id, name, movie_count) = genre

    genre_str = '%'+'%05i'% genre_id+'%'
    c.execute("SELECT COUNT(1) FROM movies WHERE genres LIKE ?", (genre_str,))
    result = c.fetchone()[0]

    if result > movie_count or movie_count == '':
        updates.append((result, genre_id))
        # print genre_id, result, movie_count, name

print updates

print "... Inserting"

c.executemany('UPDATE genres SET movie_count = ? WHERE genre_id = ?', updates)

conn.commit()
conn.close()
