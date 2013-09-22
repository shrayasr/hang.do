#!/usr/bin/python
import requests
import re
import unicodedata
import json
import time as _time
from BeautifulSoup import BeautifulSoup

headers = {"Content-Type":"application/json"}

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
    #find all the theaters in the page

    theaters = soup.findAll('div',{'class':'theater'})
    for theater in theaters:

        #find all the movies in this theater
        movies = theater.findAll('div',{'class':'movie'})
        movs_in_theatre = []
        
        for movie in movies:
            movinth = dict()

            #get movie name
            mname = movie.find('div',{'class':'name'}).a.contents[0] 
            movinth['name'] = mname

            #get movie info . The last word in info is the movie language
            info = movie.find('span',{'class':'info'}).contents[0].lower()
            info = unicodedata.normalize('NFKD', info).encode('ascii','ignore')
            info = ' '.join(re.findall('[a-z]+',info))

            t = info.split()
            movinth['lang'] = t[-1]

            #get show times for the movie
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

            # get the imdb link for the movie
            movinth['link'] = 'http://www.google.com/search?hl=en&q='+('+').join(mname.split())+'+imdb&btnI=I'
            
            #try getting the rating of the movie from the movie'S IMDB page
            try:
                imdbpage = movinth['link']
                imdbdata = requests.get(imdbpage).content
                imdbsoup = BeautifulSoup(imdbdata)
                rate = imdbsoup.find('div',{'class':'star-box-details'}).strong.span.contents[0]
            except:
                rate = -1
            movinth['rating'] = rate
            
            mtl = list()
            names = [movinth['name']+'::==>'+time for time in movinth['times'] if time]
            
            for name in names:
                tmp = dict()
                tmp['name'] = name.split('::==>')[0]
                tmp['time'] = name.split('::==>')[1]
                tmp['lang'] = movinth['lang']
                tmp['info'] = movinth['info']
                tmp['rating'] = movinth['rating']
                tmp['link'] = movinth['link']
                mtl.append(tmp)

            movs_in_theatre += mtl
        # theater name 
        name = theater.findAll('h2',{'class':'name'})[0].a.contents[0]
        print '-'*80
        print name

        tmp = dict()
        
        #get the theater's address using google maps
        mapurl = 'https://maps.google.co.in/maps?q='+'+'.join(name.split())
        mapdata = requests.get(mapurl).content
        mapsoup = BeautifulSoup(mapdata)
        address = None

        div = mapsoup.find('div',{'class':'text vcard indent block'})
        try:
            address = div.findAll('span',{'class':'pp-headline-item pp-headline-address'})[0].span.contents[0]
        except:
            pass

        if address is not None:
            try:
                caddr = address.split(',')[-3].strip(' ')
            except:
                caddr = None
        else:
            caddr = None

        for mov in movs_in_theatre:

            tmp['name_extra'] = name
            tmp['location_coarse'] = address
            tmp['location_specific'] = caddr
            tmp['mapurl'] = mapurl
            tmp['type'] = "movie"
            tmp['name'] = mov['name']
            mov['time'] = mov['time'].lower()

            a = mov['time'].find('pm')
            if a != -1:
                mov['time'] = mov['time'][:a]
                hrs = int(mov['time'].split(':')[0]) + 12
                mins = int(mov['time'].split(':')[1])
                secs = hrs * 3600 + mins * 60
                tmp['time'] = _time.time() + secs

            a = mov['time'].find('am')
            if a != -1:
                mov['time'] = mov['time'][:a]
                hrs = int(mov['time'].split(':')[0])
                mins = int(mov['time'].split(':')[1])
                secs = hrs * 3600 + mins * 60
                tmp['time'] = _time.time() + secs

            if mov['time'].find('am') == -1 and mov['time'].find('pm') == -1:
                hrs = int(mov['time'].split(':')[0]) + 12
                mins = int(mov['time'].split(':')[1])
                secs = hrs * 3600 + mins * 60
                tmp['time'] = _time.time() + secs
            
            tmp['cost'] = str(0.0)
            try:
                tmp['rating'] = str(float(unicodedata.normalize('NFKD', mov['rating']).encode('ascii','ignore'))/2)
            except TypeError:
                tmp['rating'] = str(mov['rating'])
            tmp['info'] = mov['info']
            tmp['link'] = mov['link']
            tmp['lang'] = mov['lang']

            print tmp
            print '-'*80
            theaters_data.append(tmp)

            requests.post('http://localhost:3000/places',data=json.dumps(tmp), headers=headers)

#print theaters_data

#dump the data in json format
#jsond = json.dumps(theaters_data)
#f = open('mov_data.json','w')
#f.write(jsond)
#f.close()

