#!/usr/bin/python
import requests
import re
import unicodedata
import json
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
            movs_in_theatre.append(movinth)


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

        print movs_in_theatre
        print address
        if address is not None:
            caddr = address.split(',')[-3]
        else:
            caddr = None

        '''
        if address is not None:
            try :
                int(address.split(',')[-1])
                caddr = address.split(',')[-4]
            except:
                caddr = address.split()[-3].strip(',')
        else :
            caddr = None
        '''
        tmp['name'] = name
        tmp['coarse-address'] = address
        tmp['fine-address'] = caddr
        tmp['mapurl'] = mapurl
        tmp['movies'] = movs_in_theatre
        theaters_data.append(tmp)
        requests.post('http://localhost:3000/places',data=json.dumps(tmp), headers=headers)
        print '-'*80

print theaters_data

#dump the data in json format
jsond = json.dumps(theaters_data)
f = open('mov_data.json','w')
f.write(jsond)
f.close()

