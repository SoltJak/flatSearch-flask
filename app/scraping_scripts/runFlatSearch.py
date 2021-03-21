#! python3
# runFlatSearch.py - main run file for flat offer search

from app import app, db
from app.scraping_scripts import NieruchomosciOnline, OLX, Gratka, Gumtree, Sprzedajemy, DomiPorta
from app.models import User, Flat, Flatcurrent
import bs4, requests, json, logging, pprint, re
import logging, threading

logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s -  %(levelname)s -  %(message)s')

# # 1. Nieruchomosci-Online.pl
# def runNierOnlinesearch(search_params):
    # Links = NieruchomosciOnline.getOfferLinks(search_params)
    # for link in Links:
    #     offerTitle, flatSize, roomsNo, price, offerSource = NieruchomosciOnline.getOfferDetails(link)
    #     offer = Flat(title=offerTitle, district=search_params['district'], roomsNo=roomsNo, size=flatSize, price=price, link=link)
    #     # Check if criterias are met for portals that cannot specify all conditions from query
    # ##    pricePerM2 = str(round(float(price) / float(flatSize), 0))
    # ##    if (float(price) / float(flatSize)) > float(search1.pricePerM2max):
    # ##        continue
    #     if float(offer.pricePerM2) > float(search_params['pricePerM2max']):
    #         continue
    #     else:
    #         db.session.add(offer)
    #         # offerNum += 1

# 2. OLX.pl
def runOLXsearch(search_params):
    logging.debug('Starting OLX & Otodom search.')
    Links = OLX.getOfferLinks(search_params)
    linkPattern = re.compile('(\S+?)(.html)')
    # Collect offers from links
    for link in Links:
        if 'www.otodom.pl' in link:
            offerTitle, flatSize, roomsNo, price, offerSource, pictureLink = OLX.getOfferDetailsOTODOM(link)
            pricePerM2 = str(round(float(price) / float(flatSize), 0))
            offer = Flat(title=offerTitle, district=search_params['location'], roomsNo=roomsNo, size=flatSize, price=price, pricePerM2=pricePerM2, link=link)
            offerCurrent = Flatcurrent(title=offerTitle, district=search_params['location'], roomsNo=roomsNo, size=flatSize, price=price, pricePerM2=pricePerM2, link=link, pictureLink=pictureLink)
            db.session.add(offer)
            db.session.add(offerCurrent) 
        else:
            pass    # Olx currently not supported - see below
    # # Collect offers from OLX search page (OLX offers alone not working) - not working now since OLX blocks scraping
    # OLXlist = OLX.getOfferDetailsOLXliteList(search_params)
    # for textLine in OLXlist:
    #     link = textLine.h3.a.get('href')
    #     if 'olx.pl' in link:
    #         offerTitle, flatSize, price, offerSource, pictureLink = OLX.getOfferDetailsOLXlite(textLine)
    #         offer = Flat(title=offerTitle, district=search_params['location'], roomsNo=search_params['roomsNoSearch'], size=flatSize, price=price, pricePerM2='BD', link=link)
    #         offerCurrent = Flatcurrent(title=offerTitle, district=search_params['location'], roomsNo=search_params['roomsNoSearch'], size=flatSize, price=price, pricePerM2='BD', link=link, pictureLink=pictureLink)
    #         db.session.add(offer)
    #         db.session.add(offerCurrent) 
    logging.debug('End of OLX & Otodom search.')

# 3. Gratka.pl
def runGratkaSearch(search_params):
    logging.debug('Starting Gratka search.')
    Links = Gratka.getOfferLinks(search_params)
    for link in Links:
        offerTitle, flatSize, roomsNo, price, offerSource, pictureLink = Gratka.getOfferDetailsGratka(link)
        pricePerM2 = str(round(float(price) / float(flatSize), 0))
        # Check if criterias are met for portals that cannot specify all conditions from query
        if float(pricePerM2) > float(search_params['pricePerM2max']) or float(pricePerM2) < float(search_params['pricePerM2min']):
            # print('pricePerM2: ' + pricePerM2 + ', maxlimit: ' + search_params['pricePerM2max'] + ' - Continuing')
            continue
        offer = Flat(title=offerTitle, district=search_params['location'], roomsNo=roomsNo, size=flatSize, price=price, pricePerM2=pricePerM2, link=link, pictureLink=pictureLink)
        offerCurrent = Flatcurrent(title=offerTitle, district=search_params['location'], roomsNo=roomsNo, size=flatSize, price=price, pricePerM2=pricePerM2, link=link, pictureLink=pictureLink)       
        db.session.add(offer)
        db.session.add(offerCurrent)
    logging.debug('End of Gratka search.')

# # 4. Gumtree.pl
def runGumtreeSearch(search_params):
    logging.debug('Starting Gumtree search.')
    Links = Gumtree.getOfferLinks(search_params)
    for link in Links:
        offerTitle, flatSize, roomsNo, price, offerSource, pictureLink = Gumtree.getOfferDetailsGumtree(link)
        pricePerM2 = str(round(float(price) / float(flatSize), 0))
        # print('Current flat price Gumtree: ' + price + ', current size: ' + flatSize)
        offer = Flat(title=offerTitle, district=search_params['location'], roomsNo=roomsNo, size=flatSize, price=price, pricePerM2=pricePerM2, link=link, pictureLink=pictureLink)
        offerCurrent = Flatcurrent(title=offerTitle, district=search_params['location'], roomsNo=roomsNo, size=flatSize, price=price, pricePerM2=pricePerM2, link=link, pictureLink=pictureLink)        

        # Check if criterias are met for portals that cannot specify all conditions from query
        if float(pricePerM2) > float(search_params['pricePerM2max']):
            # print('pricePerM2: ' + pricePerM2 + ', maxlimit: ' + search_params['pricePerM2max'] + ' - Continuing')
            continue
        if (float(flatSize) < float(search_params['flatSizeMin']) or float(flatSize) > float(search_params['flatSizeMax'])):
            # print('pricePerM2: ' + pricePerM2 + ', minlimit: ' + search_params['pricePerM2min'] + ' - Continuing') 
            continue
        db.session.add(offer)
        db.session.add(offerCurrent)
    logging.debug('End of Gumtree search.')

# 5. Sprzedajemy.pl
def runSprzedajemySearch(search_params):
    logging.debug('Starting Sprzedajemy search.')
    Links = Sprzedajemy.getOfferLinks(search_params)
    for link in Links:
        offerTitle, flatSize, roomsNo, price, offerSource, pictureLink = Sprzedajemy.getOfferDetailsSprzedajemy(link)
        pricePerM2 = str(round(float(price) / float(flatSize), 0))
        offer = Flat(title=offerTitle, district=search_params['location'], roomsNo=roomsNo, size=flatSize, price=price, pricePerM2=pricePerM2, link=link, pictureLink=pictureLink)
        offerCurrent = Flatcurrent(title=offerTitle, district=search_params['location'], roomsNo=roomsNo, size=flatSize, price=price, pricePerM2=pricePerM2, link=link, pictureLink=pictureLink)       
        db.session.add(offer)
        db.session.add(offerCurrent)
    logging.debug('End of Domiporta search.')

# 6. Domiporta.pl
def runDomiportaSearch(search_params):
    logging.debug('Starting Domiporta search.')
    Links = DomiPorta.getOfferLinks(search_params)
    for link in Links:
        # print('Current domiporta link: ' + link)
        offerTitle, flatSize, roomsNo, price, offerSource, pictureLink = DomiPorta.getOfferDetailsDomiPorta(link)
        pricePerM2 = str(round(float(price) / float(flatSize), 0))
        offer = Flat(title=offerTitle, district=search_params['location'], roomsNo=roomsNo, size=flatSize, price=price, pricePerM2=pricePerM2, link=link, pictureLink=pictureLink)
        offerCurrent = Flatcurrent(title=offerTitle, district=search_params['location'], roomsNo=roomsNo, size=flatSize, price=price, pricePerM2=pricePerM2, link=link, pictureLink=pictureLink)       
        db.session.add(offer)
        db.session.add(offerCurrent)
    logging.debug('End of Domiporta search.')

def runFlatSearch(search_params):

    Flatcurrent.query.delete()
    db.session.commit()

    #  ====== Run search in threads =========
    scrapeThreads = []

    # Nieruchomości Online:
    # if 'nierOnline' in search_params['source']:
    #     scrapeThread = threading.Thread(target=runNierOnlinesearch, args=(search_params,))
    #     scrapeThreads.append(scrapeThread)
    #     scrapeThread.start()
    if 'olx' in search_params['source']:
        scrapeThread = threading.Thread(target=runOLXsearch, args=(search_params,))
        scrapeThreads.append(scrapeThread)
        scrapeThread.start()
    if 'gratka' in search_params['source']:
        scrapeThread = threading.Thread(target=runGratkaSearch, args=(search_params,))
        scrapeThreads.append(scrapeThread)
        scrapeThread.start()
    if 'gumtree' in search_params['source']:
        scrapeThread = threading.Thread(target=runGumtreeSearch, args=(search_params,))
        scrapeThreads.append(scrapeThread)
        scrapeThread.start()
    if 'sprzedajemy' in search_params['source']:
        scrapeThread = threading.Thread(target=runSprzedajemySearch, args=(search_params,))
        scrapeThreads.append(scrapeThread)
        scrapeThread.start()
    if 'domiporta' in search_params['source']:
        scrapeThread = threading.Thread(target=runDomiportaSearch, args=(search_params,))
        scrapeThreads.append(scrapeThread)
        scrapeThread.start()

    # Wait for all threads to end.
    for scrapeThread in scrapeThreads:
        scrapeThread.join()
    logging.debug('Done.')

    # Commit dowloaded offers to database
    # runGumtreeSearch(search_params)       # Test only
    db.session.commit()

####