import requests
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
        soupPage = BeautifulSoup(articlePage.text)

        # Location is quite complex, BS handles it stupidly
        # Take the location area composite and pick up the contents
        locationArrayComposite = soupPage.findAll('h4',{'class':'res-main-address-text left'}); 
        locationArray = locationArrayComposite[0].contents

        # for all the parts in the location
        for locationParts in locationArray:
            # Get the full address
            if hasattr(locationParts,'contents'):
                itemLocationCoarse += locationParts.contents[0].strip()
            else:
                itemLocationCoarse += locationParts.strip()

        # Pick up a specific location
        itemLocationSpecific = soupPage.findAll('strong',{'itemprop':'addressLocality'})[0].contents[0].strip()

        # Pick up a rating
        itemRating = soupPage.findAll('b',{'class':'rating-text-div rrw-rating-text'})[0].contents[0].strip()

        # Pick up the cost
        itemCost = soupPage.findAll('span',{'class':'cft-big'})[0].contents[0].strip()

        # There can be more than 1 telephone,
        # get the first one
        telItem = soupPage.findAll('span',{'class':'tel'})
        if len(telItem) > 1:
            itemPhone = telItem[1].contents[0].strip()
        else:
            itemPhone = telItem[0].contents[0].strip()

        '''
        print itemName + " ["+itemLink+"]"
        print itemCost,itemRating
        print itemLocationSpecific
        '''

        count += 1

for i in xrange(1,192):
    getRestaurants(str(i))
