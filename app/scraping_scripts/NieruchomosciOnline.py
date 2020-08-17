#! python3
# NieruchomosciOnline.py - defines functions to scrape NieruchomosciOnline in order
# to download requested information from flat offers

import bs4, requests, re, json, pprint

baseURL = 'https://www.nieruchomosci-online.pl/szukaj.html?3,mieszkanie,sprzedaz,,'
Links = []
flatOfferArray = []

# Location codes for URL creation specific for this site
locationCodes = {
    "bemowo": 'Warszawa:20571,Bemowo:77',
    "wola": 'Warszawa:20571,Wola:93',
    "bielany": 'Warszawa:20571,Bielany:79'
}

# Function to create URL for search of given parameters
def SearchUrl(queryCriteria):
    url = (baseURL
           + locationCodes[queryCriteria['location']] + ',,,'
           + queryCriteria['priceMin'] + '-' + queryCriteria['priceMax'] + ','
           + queryCriteria['flatSizeMin'] + '-' + queryCriteria['flatSizeMax'] + ',,,,,,'
           + queryCriteria['roomsNoSearch'] + '-' +  queryCriteria['roomsNoSearch'])
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
    tempList = list(soup.find_all('h2', class_='name'))
    for textLine in tempList:
        Links.append(textLine.a.get('href'))
    return Links

# Function to get required data from a single offer
def getOfferDetails(url):
    offerSoup = downloadPage(url)
    
    # 1. Find offer title
    offerTitleRaw = offerSoup.h1.getText().strip()
    offerTitle = ' '.join(offerTitleRaw.split())

    # 2. Find flat size
    flatSizeRaw = offerSoup.find('span', class_='info-area desktop-tablet-only').getText()
    flatSize = ''.join(flatSizeRaw.split()[0:-1])
    pattern = re.compile('(\d+?)(,)(\d*\d$)')
    if pattern.search(flatSize) != None:
        flatSize = pattern.search(flatSize)[1] + '.' + pattern.search(flatSize)[3]    
    
    #3. Find number of rooms
    textForSize = offerSoup.select('#attributesTable')[0].find_all('td')
    for textLine in textForSize:
        if textLine.find('span', class_='fheader').getText() == 'Liczba pokoi:':
            roomsNo = textLine.find('span', class_='fsize-a').getText()

    #4. Find price of flat
    priceRaw = offerSoup.find('span', class_='info-primary-price').getText()
    price = ''.join(priceRaw.split()[0:-1])

    #5. Find offer source
    offerSource = 'BD'

    return offerTitle, flatSize, roomsNo, price, offerSource
