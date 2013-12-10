#!/usr/bin/python
# TODO make range command line arguments

import sys, codecs
sys.stdout = codecs.getwriter('utf-8')(sys.stdout) # if your terminal can't do utf-8, well...

import time
import urllib2

import BeautifulSoup

cookie = """ copy from eg Chrome's developer tools Request tab into here: NetflixId=[string];profilesNewSession=0;profilesNewUser=0 """

def get_genre(i):
    opener = urllib2.build_opener()
    opener.addheaders.append(('Cookie', cookie))

    page = opener.open("http://movies.netflix.com/WiAltGenre?agid=%s" % i)
    soup = BeautifulSoup.BeautifulSoup(page.read())

    name = soup.find('div', {'class': 'crumb'})
    return name.getText().strip()

for i in range(1,100):
    genre = get_genre(i)
    if genre:
        print "%s (%s)" % (genre, i)
    time.sleep(0.1)
