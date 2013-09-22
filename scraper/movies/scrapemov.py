#!/usr/bin/python
import requests
import re
import unicodedata
import json
from BeautifulSoup import BeautifulSoup

url = 'http://www.google.co.in/movies?near=bangalore,+ka,+ind&start='
pagedata = list()
urls = list()

for i in range(6):
    urls.append(url+str(i*10))

for turl in urls:
    r = requests.get(turl)
    pagedata.append(r.content)

mdata = list()
theaters_data = list()

print len(pagedata)

for page in pagedata:

    soup = BeautifulSoup(page)
    theaters = soup.findAll('div',{'class':'theater'})
    for theater in theaters:
        movies = theater.findAll('div',{'class':'movie'})
        movs_in_theatre = []
        for movie in movies:
            movinth = dict()
            mname = movie.find('div',{'class':'name'}).a.contents[0] 
            movinth['name'] = mname

            info = movie.find('span',{'class':'info'}).contents[0].lower()
            info = unicodedata.normalize('NFKD', info).encode('ascii','ignore')
            info = ' '.join(re.findall('[a-z]+',info))

            t = info.split()
            movinth['lang'] = t[-1]
            movs_in_theatre.append(movinth)

            timesli = list()
            for time in movie.find('div',{'class':'times'}).contents :
                mtimes = time.contents[2].split(';')
                mtime = [unicodedata.normalize('NFKD', mtime).encode('ascii','ignore') for mtime in mtimes]
                tmp = ''    
                for mti in mtime:
                    i = mti.find('&')
                    mti = mti[:i]
                    tmp += mti

                timesli.append(tmp)

            movinth['times'] = timesli
            movinth['info'] = ' '.join(info.split()[:-1])

            movinth['link'] = 'http://www.google.com/search?hl=en&q='+('+').join(mname.split())+'+imdb&btnI=I'
            try:
                imdbpage = movinth['link']
                imdbdata = requests.get(imdbpage).content
                imdbsoup = BeautifulSoup(imdbdata)
                rate = imdbsoup.find('div',{'class':'star-box-details'}).strong.span.contents[0]
            except:
                rate = -1
            movinth['rating'] = rate
            


        name = theater.findAll('h2',{'class':'name'})[0].a.contents[0]
        print '-'*80
        print name
        tmp = dict()
        mapurl = 'https://maps.google.co.in/maps?q='+'+'.join(name.split())
        mapdata = requests.get(mapurl).content
        mapsoup = BeautifulSoup(mapdata)
        address = None
        div = mapsoup.find('div',{'class':'text vcard indent block'})
        try:
            address = div.findAll('span',{'class':'pp-headline-item pp-headline-address'})[0].span.contents[0]
        except:
            pass

        print movs_in_theatre
        print address
        tmp['name'] = name
        tmp['address'] = address
        tmp['mapurl'] = mapurl
        tmp['movies'] = movs_in_theatre
        theaters_data.append(tmp)
        print '-'*80

#print '*'*80
print theaters_data 
jsond = json.dumps(theaters_data)
f = open('mov_data.json','w')
f.write(jsond)
f.close()
#print '*'*80