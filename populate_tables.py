#!/usr/bin/python

# we've been outputting stuff to text so now I get to wedge it into a database
# funtimes

# set up the database with `sqlite3 netflix_genres.sqlite < create_tables.sql`

import codecs

import sqlite3
conn = sqlite3.connect('netflix_genres.sqlite')

c = conn.cursor()
genres = []
movies = []

# handle extended results
f = codecs.open('extended_results_10000-12345', 'r', encoding='utf-8')
for line in f:
    if not line.startswith('\t'):
        # genre
        skipped = False
        movie_count = 0

        line = line.strip()

        if 'Skipped' in line and '(' not in line:
            skipped = True
            genre_id = int(line.replace('Skipped ', ''))
            genre_url = "http://movies.netflix.com/WiAltGenre?agid=%s" % genre_id

            genres.append((genre_id, 'null', genre_url, 'null', 'null', skipped))
            continue

        (genre, genre_id) = line.strip().split('(')
        genre = genre.strip()

        if genre == '':
            continue

        # no movies?
        if "no movies" in genre_id:
            movie_count = 0

        genre_id = int(genre_id[:genre_id.index(')')])

        if 'Subgenres' in genre:
            genre = genre[:genre.index('Subgenres')]
            print "Genre %s (%s) has subgenres" % (genre_id, genre)

        genre_url = "http://movies.netflix.com/WiAltGenre?agid=%s" % genre_id
    
        # enough to write
        genres.append((genre_id, genre, genre_url, 'null', movie_count, False))

    else:
        # movie
        # turns out I posted these badly so you know let's not bother
        
        # line = line.strip()
        # print line
        # (name, info) = line.split('(')
        # 
        # name = name.strip()
        # info = info[:info.index(')')]
        # 
        # movies.append((name, info))
        # # TODO collect genres

f.close()

c.executemany('INSERT INTO genres VALUES (?,?,?,?,?,?)', genres)
c.executemany('INSERT INTO movies (name, info) VALUES (?,?)', movies)

# handle alphabetical results
genres = []
f = codecs.open('results_00001-05000-alpha.txt', 'r', encoding='utf-8')
for line in f:
    (genre, genre_id) = line.strip().split(' (')
    genre_id = int(genre_id[:-1])

    if 'Subgenres' in genre:
        genre = genre[:genre.index('Subgenres')]
        print "Genre %s (%s) has subgenres" % (genre_id, genre)

    genre_url = "http://movies.netflix.com/WiAltGenre?agid=%s" % genre_id
    
    # enough to write
    genres.append((genre_id, genre, genre_url, 'null', 'null', False))

f.close()

c.executemany('INSERT INTO genres VALUES (?,?,?,?,?,?)', genres)
conn.commit()
conn.close()

