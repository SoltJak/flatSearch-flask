#! python3
# Gumtree.py - defines functions to scrape Gumtree.pl in order
# to download requested information from flat offers

import bs4, requests, re, json, pprint

baseURL = 'https://www.gumtree.pl/s-mieszkania-i-domy-sprzedam-i-kupie/'
URL_opt1 = 'priceType=FIXED'
offerBaseURL = 'https://www.gumtree.pl'
Links = []
flatOfferArray = []

# Location codes and others for URL creation specific for this site
locationCodes = {
    "bemowo": 'bemowo/v1c9073l3200009p1',
    "wola": 'wola/v1c9073l3200025p1',
    "bielany": 'bielany/v1c9073l3200011p1',
    "ochota": 'ochota/v1c9073l3200013p1'
}
marketCode = {'pierwotny': '',
          'wtorny': ''
          }

## Function to create URL for search of given parameters
def SearchUrl(queryCriteria):
    url = (baseURL
           + locationCodes[queryCriteria['location']]
           + '?'
           + 'pr=' + queryCriteria['priceMin'] + ',' + queryCriteria['priceMax'] + '&'
           + 'nr=' + queryCriteria['roomsNoSearch'] + '&'
           + URL_opt1)
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
    tempList = list(soup.find_all('a', class_='href-link tile-title-text'))
    for textLine in tempList:
        Links.append(offerBaseURL + textLine.get('href'))
    return Links

# Function to get required data from a single offer
def getOfferDetailsGumtree(url):
    offerSoup = downloadPage(url)
    
    # 1. Find offer title
    offerTitle = offerSoup.find('span', class_='myAdTitle').getText()

    detailsList = list(offerSoup.find_all('div', class_='attribute'))
    for textLine in detailsList:

        # 2. Find flat size
        if textLine.find('span', class_='name').getText() == 'Wielkość (m2)':
            flatSize = textLine.find('span', class_='value').getText()
        #3. Find number of rooms
        elif textLine.find('span', class_='name').getText() == 'Liczba pokoi':
            roomsNo = textLine.find('span', class_='value').getText()

        #4. Find offer source
        elif textLine.find('span', class_='name').getText() == 'Na sprzedaż przez':
            offerSource = textLine.find('span', class_='value').getText()

    #5. Find price of flat
    priceRaw = offerSoup.find('span', class_='amount').getText()
    price = ''.join(priceRaw.split()[0:-1])

    #6. Find picture link
    if offerSoup.find('div', class_='main').find('img').get('src'):
        pictureLink = offerSoup.find('div', class_='main').find('img').get('src')

    return offerTitle, flatSize, roomsNo, price, offerSource, pictureLink
