#! python3
# DomiPorta.py - defines functions to scrape DomiPorta.pl in order
# to download requested information from flat offers

import bs4, requests, re, json, pprint

baseURL = 'https://www.domiporta.pl/mieszkanie/sprzedam/mazowieckie/warszawa/'
URL_opt1 = ''
offerBaseURL = 'https://www.domiporta.pl'
Links = []
flatOfferArray = []

# Location codes and others for URL creation specific for this site
locationCodes = {
    "bemowo": 'bemowo',
    "wola": 'wola',
    "bielany": 'bielany',
    "ochota": 'ochota'
}
marketCode = {'pierwotny': 'Pierwotny',
          'wtorny': 'Wtorny'
          }


## Function to create URL for search of given parameters
def SearchUrl(queryCriteria):
    url = (baseURL
           + locationCodes[queryCriteria['location']] + '?'
           + 'Surface.From=' + queryCriteria['flatSizeMin'] + '&'
           + 'Surface.To=' + queryCriteria['flatSizeMax'] + '&'
           + 'Price.From=' + queryCriteria['priceMin'] + '&'
           + 'Price.To=' + queryCriteria['priceMax'] + '&'
           + 'PricePerMeter.From=' + queryCriteria['pricePerM2min'] + '&'
           + 'PricePerMeter.To=' + queryCriteria['pricePerM2max'] + '&'
           + 'Rooms.From=' + queryCriteria['roomsNoSearch'] + '&'
           + 'Rooms.To=' + queryCriteria['roomsNoSearch'] + '&'
           + 'Rynek=' + marketCode[queryCriteria['market']]
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
    tempList = list(soup.find_all('a', class_='sneakpeak__title sneakpeak__title_normal sneakpeak__link'))
    for textLine in tempList:
        Links.append(offerBaseURL + textLine.get('href'))
    return Links

# Function to get required data from a single offer
def getOfferDetailsDomiPorta(url):
    offerSoup = downloadPage(url)
    
    # 1. Find offer title
    offerTitleRaw = offerSoup.h1.getText().strip()
    offerTitle = ' '.join(offerTitleRaw.split())
    
    detailsContainer = offerSoup.find('ul', class_='features__list-2')
    detailsListNames = list(detailsContainer.find_all('span', class_='features__item_name'))
    detailsListValues = list(detailsContainer.find_all('span', class_='features__item_value'))
    for i in range(0, len(detailsListNames)):
        textLine = detailsListNames[i].getText()
        textValue = detailsListValues[i].getText()
        
        # 2. Find flat size
        if textLine == 'Powierzchnia całkowita':
            flatSizeRaw = textValue.strip()
            flatSize = ''.join(flatSizeRaw.split()[0:-1])
            pattern = re.compile('(\d+?)(,)(\d*\d$)')
            if pattern.search(flatSize) != None:
                flatSize = pattern.search(flatSize)[1] + '.' + pattern.search(flatSize)[3]   

        #3. Find number of rooms
        elif textLine == 'Liczba pokoi ':
            roomsNo = textValue

        #4. Find price of flat
        elif textLine == 'Cena':
            priceRawTemp = textValue.strip()
            priceRawPattern = re.compile('(\d+?)(\s)?(\d+?)(\s+?)(zł)')
            priceRaw = ''
            for i in range(1,len(priceRawPattern.search(priceRawTemp).groups())-1):
                if priceRawPattern.search(priceRawTemp).group(i) != None:
                    priceRaw = priceRaw + priceRawPattern.search(priceRawTemp).group(i)
            priceRaw = priceRaw + ' zł'
            price = ''.join(priceRaw.split()[0:-1])

    #5. Find offer source
    offerSource = 'BD'

    #6. Find picture link
    if len(list(offerSoup.find_all('img', class_='js-gallery__item--open'))) > 0:
        pictureLink = list(offerSoup.find_all('img', class_='js-gallery__item--open'))[0].get('src')
    else:
        pictureLink = ''
            
    return offerTitle, flatSize, roomsNo, price, offerSource, pictureLink
