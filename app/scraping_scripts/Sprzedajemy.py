#! python3
# Sprzedajemy.py - defines functions to scrape Sprzedajemy.pl in order
# to download requested information from flat offers

import bs4, requests, re, json, pprint

baseURL = 'https://sprzedajemy.pl/szukaj?inp_category_id=3&inp_category_id=36&catCode=1b8e55&inp_location_id=14&inp_location_id=28024&'
URL_opt1 = 'sort=inp_srt_date_d&items_per_page=30'
offerBaseURL = 'https://www.sprzedajemy.pl'
Links = []
flatOfferArray = []

# Location codes and others for URL creation specific for this site
locationCodes = {
    "bemowo": '1101',
    "wola": '1181',
    "bielany": '1111',
    "ochota": '1121'
}
marketCode = {'pierwotny': '',
          'wtorny': ''
          }

## Function to create URL for search of given parameters
def SearchUrl(queryCriteria):
    url = (baseURL
           + 'inp_precinct_id=' + locationCodes[queryCriteria['location']] + '&'
           + 'inp_price%5Bfrom%5D=' + queryCriteria['priceMin'] + '&'
           + 'inp_price%5Bto%5D=' + queryCriteria['priceMax'] + '&'
           + 'inp_attribute_143%5Bfrom%5D=' + queryCriteria['flatSizeMin'] + '&'
           + 'inp_attribute_143%5Bto%5D=' + queryCriteria['flatSizeMax'] + '&'
           + 'inp_attribute_252%5Bfrom%5D=' + queryCriteria['pricePerM2min'] + '&'
           + 'inp_attribute_252%5Bto%5D=' + queryCriteria['pricePerM2max'] + '&'
           + 'inp_attribute_145%5Bfrom%5D=' + queryCriteria['roomsNoSearch'] +'&'
           + 'inp_attribute_145%5Bto%5D=' + queryCriteria['roomsNoSearch'] +'&'
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
    tempList = list(soup.find_all('h2', class_='title'))
    for textLine in tempList:
        Links.append(offerBaseURL + textLine.a.get('href'))
    return Links

# Function to get required data from a single offer
def getOfferDetailsSprzedajemy(url):
    offerSoup = downloadPage(url)
    
    # 1. Find offer title
    offerTitle = offerSoup.h1.getText().strip()
    
    detailsListRaw = list(offerSoup.find_all('ul', class_='attribute-list'))
    detailsList = list(detailsListRaw[0].find_all('li', class_='item'))
    for textLine in detailsList:

        # 2. Find flat size
        if textLine.span.getText() == 'Powierzchnia':
            flatSizeRaw = textLine.strong.getText()
            flatSize = ''.join(flatSizeRaw.split()[0:-1])
            
        #3. Find number of rooms
        elif textLine.span.getText() == 'Liczba pokoi':
            roomsNo = textLine.strong.getText()

        #4. Find offer source
        elif textLine.span.getText() == 'Oferta od':
            offerSourceTemp = textLine.strong.getText().strip()
            if offerSourceTemp == 'firmy':
                offerSource = 'Agencja'
            elif offerSourceTemp == 'osoby prywatnej':
                offerSource = 'Właściciel'
            else:
                offerSource = ''

    #5. Find price of flat
    priceRaw = offerSoup.find_all('div', class_='priceWrp')[0].span.getText().strip()
    price = ''.join(priceRaw.split()[0:-1])

    return offerTitle, flatSize, roomsNo, price, offerSource
