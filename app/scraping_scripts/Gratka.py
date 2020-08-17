#! python3
# Gratka.py - defines functions to scrape Gratka.pl in order
# to download requested information from flat offers

import bs4, requests, re, json, pprint

baseURL = 'https://gratka.pl/nieruchomosci/mieszkania/warszawa/'
URL_opt1 = '/sprzedaz?'
URL_opt2 = '&sort=newest'
Links = []
flatOfferArray = []

# Location codes and others for URL creation specific for this site
locationCodes = {
    "bemowo": 'bemowo',
    "wola": 'wola',
    "bielany": 'bielany',
    "ochota": 'ochota'
}
marketCode = {'pierwotny': 'pierwotny',
          'wtorny': 'wtorny'
          }

## Function to create URL for search of given parameters
def SearchUrl(queryCriteria):
    url = (baseURL
           + locationCodes[queryCriteria['location']]
           + URL_opt1
           + 'cena-calkowita:min=' + queryCriteria['priceMin'] + '&'
           + 'cena-calkowita:max=' + queryCriteria['priceMax'] + '&'
           + 'cena-za-m2:min=' + queryCriteria['pricePerM2min'] + '&'
           + 'cena-za-m2:max=' + queryCriteria['pricePerM2max'] + '&'
           + 'powierzchnia-w-m2:min=' + queryCriteria['flatSizeMin'] + '&'
           + 'powierzchnia-w-m2:max=' + queryCriteria['flatSizeMax'] + '&'
           + 'liczba-pokoi:min=' + queryCriteria['roomsNoSearch'] + '&'
           + 'liczba-pokoi:max=' + queryCriteria['roomsNoSearch'] + '&'
           + 'rynek' + marketCode[queryCriteria['market']]
           + URL_opt2)
    return url

# Function to download the page and allow for its scrape
def downloadPage(url):
    res = requests.get(url)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    return soup

# TODO: Function to create list of sites from a given search condition

# Function to create a list of offers from a search page
def getOfferLinks(queryCriteria):
    url = SearchUrl(queryCriteria)
    soup = downloadPage(url)
    tempList = list(soup.find_all('a', class_='teaser__anchor'))
    for textLine in tempList:
        Links.append(textLine.get('href'))
    return Links

# Function to get required data from a single offer
def getOfferDetailsGratka(url):
    offerSoup = downloadPage(url)
    
    # 1. Find offer title
    offerTitle = offerSoup.h1.getText().strip()

    detailsListTemp = list(offerSoup.find_all('ul', class_='parameters__rolled'))
    detailsList = detailsListTemp[0].find_all('li')
    for textLine in detailsList:

        if textLine.span == None:
            continue
        
        else:
            # 2. Find flat size
            if textLine.span.getText() == 'Powierzchnia w m2':
                flatSizeRaw = textLine.b.getText().strip()
                flatSize = ''.join(flatSizeRaw.split()[0:-1])
                pattern = re.compile('(\d+?)(,)(\d*\d$)')
                if pattern.search(flatSize) != None:
                    flatSize = pattern.search(flatSize)[1] + '.' + pattern.search(flatSize)[3]
            
            #3. Find number of rooms
            elif textLine.span.getText() == 'Liczba pokoi':
                    roomsNo = textLine.b.getText()

            #4. Find offer source
            offerSource = 'BD'

    #5. Find price of flat
    priceRawTemp = offerSoup.select('span' '.priceInfo__value')[0].getText().strip().replace('\n','')
    priceRawPattern = re.compile('(\d+?)(\s)(\d+?)(\s+?)(zł)')
    priceRaw = ''
    for i in range(1,6):
        priceRaw = priceRaw + priceRawPattern.search(priceRawTemp)[i]
    price = ''.join(priceRaw.split()[0:-1])

    return offerTitle, flatSize, roomsNo, price, offerSource
