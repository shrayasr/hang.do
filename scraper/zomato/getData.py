import requests
import json
import sys
from BeautifulSoup import BeautifulSoup

def getRestaurants(pageNo):

    # Define a zomato base URL
    ZBASE_URL = 'http://www.zomato.com/'

    # Define a base URL for restaurants
    BASE_URL = ZBASE_URL + 'bangalore/restaurants?sort=pa&page='

    # Pick up the page text
    page = requests.get(BASE_URL + pageNo)

    # Declare a beautifulsoup object on the page's text
    soup = BeautifulSoup(page.text)

    # Pick up all the <article>'s from the page
    articles = soup.findAll('article')

    # Pick up the count of articles on the page
    countArticles = len(articles)

    # Declare a count to loop through articles on page
    count = 1

    print "Getting data for page: "+pageNo

    for article in articles:
        print "Processing article "+str(count)+" of "+str(countArticles)

        # required stuff on the backend
        itemType = "restaurant"
        itemLocationCoarse = ""
        itemLocationSpecific = ""
        itemName = ""
        itemRating = ""
        itemCost = ""
        itemPhone = ""
        itemLink = ""

        # Get the article link
        itemLink = ZBASE_URL + article.findAll('h3')[0].a['href'][1:].strip() + "/info#tabtop"

        # Get the name of the restaurant
        itemName = article.findAll('h3')[0].a.contents[0].strip()


        # Go inside the article page
        articlePage = requests.get(itemLink)  

        # Get a BS to that page
        articleDetailPage = BeautifulSoup(articlePage.text)

        # Location is quite complex, BS handles it stupidly
        # Take the location area composite and pick up the contents
        locationArrayComposite = articleDetailPage.findAll('h4',{'class':'res-main-address-text left'}); 
        locationArray = locationArrayComposite[0].contents

        # for all the parts in the location
        for locationParts in locationArray:
            # Get the full address
            if hasattr(locationParts,'contents'):
                itemLocationCoarse += locationParts.contents[0].strip()
            else:
                itemLocationCoarse += locationParts.strip()

        # Pick up a specific location
        itemLocationSpecific = articleDetailPage.findAll('strong',{'itemprop':'addressLocality'})[0].contents[0].strip()

        # Pick up a rating string
        itemRatingString = articleDetailPage.findAll('b',{'class':'rating-text-div rrw-rating-text'})[0].contents[0].strip()

        # Set the ratings
        ratings = {
                "legendary":5,
                "excellent":4.5,
                "very good":4,
                "good":3.5,
                "average":2.5,
                "poor":2
        }

        # Pick up the rating depending on the settings
        itemRating = ratings[itemRatingString.lower()]

        # Pick up the cost
        itemCost = articleDetailPage.findAll('span',{'class':'cft-big'})[0].contents[0].strip()

        # There can be more than 1 telephone,
        # get the first one
        telItem = articleDetailPage.findAll('span',{'class':'tel'})
        if len(telItem) > 1:
            if "Not Available" in telItem[1].contents[0]:
                itemPhone = ""
            else:
                itemPhone = telItem[1].contents[0].strip()
        else:
            itemPhone = telItem[0].contents[0].strip()

        # Generate a payload
        payload = {
                "name": itemName,
                "name_extra": "",
                "type": itemType,
                "location_coarse": itemLocationCoarse.lower(),
                "location_specific": itemLocationSpecific.lower(),
                "rating": itemRating,
                "cost": itemCost,
                "phone": itemPhone,
                "link": itemLink
                }

        headers = {
                "Content-Type":"application/json"
        }

        print "pushing to DB"
        requests.post("http://localhost:3000/places",data=json.dumps(payload),headers=headers)

        count += 1

if __name__ == "__main__":

    if len(sys.argv) == 1:
        print "min 1 parameter required (page to start from)"
        sys.exit(1)

    startPage = int(sys.argv[1])
    
    print "Scraping from page number: " + str(startPage)
    for i in xrange(startPage,192):
        getRestaurants(str(i))
