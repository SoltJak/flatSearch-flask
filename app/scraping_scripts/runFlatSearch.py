#! python3
# runFlatSearch.py - main run file for flat offer search

from app import app, db
from app.scraping_scripts import NieruchomosciOnline, OLX, Gratka, Gumtree, Sprzedajemy, DomiPorta
from app.models import User, Flat, Flatcurrent
import bs4, requests, json, logging, pprint, re
import logging, threading
# import random, string

# def get_random_string(length):
# # get random string pf length 20 with letters, digits, and symbols
#     characters = string.ascii_letters + string.digits + string.punctuation
#     searchString = ''.join(random.choice(characters) for i in range(length))
#     return searchString

def runFlatSearch(search_params):

    Flatcurrent.query.delete()
    delete = db.session.query(Flatcurrent).delete()
    db.session.commit()
    # searchString = get_random_string(10)
    # currentSearchResults = []

    # # 1. Nieruchomosci-Online.pl
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
    if 'olx' in search_params['source']:
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
                pass
   
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

    # 3. Gratka.pl
    if 'gratka' in search_params['source']:
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
            
            # currentSearchResults.append({'title': offerCurrent.title, 'district': offerCurrent.district, 'roomsNo': offerCurrent.roomsNo, 'size': offerCurrent.size, 'price': offerCurrent.price, 'pricePerM2': offerCurrent.pricePerM2, 'link': offerCurrent.link, 'pictureLink': offerCurrent.pictureLink})

            db.session.add(offer)
            db.session.add(offerCurrent)



    # # 4. Gumtree.pl
    if 'gumtree' in search_params['source']:
        Links = Gumtree.getOfferLinks(search_params)
        for link in Links:
            offerTitle, flatSize, roomsNo, price, offerSource, pictureLink = Gumtree.getOfferDetailsGumtree(link)
            pricePerM2 = str(round(float(price) / float(flatSize), 0))
            # print('Current flat price Gumtree: ' + price + ', current size: ' + flatSize)
            offer = Flat(title=offerTitle, district=search_params['location'], roomsNo=roomsNo, size=flatSize, price=price, pricePerM2=pricePerM2, link=link, pictureLink=pictureLink, searchCode=search_params['searchCode'])
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

    # # 5. Sprzedajemy.pl
    # if 'sprzedajemy' in search_params['source']:
    #     Links = Sprzedajemy.getOfferLinks(search_params)
    #     for link in Links:
    #         offerTitle, flatSize, roomsNo, price, offerSource, pictureLink = Sprzedajemy.getOfferDetailsSprzedajemy(link)
    #         pricePerM2 = str(round(float(price) / float(flatSize), 0))
    #         offer = Flat(title=offerTitle, district=search_params['location'], roomsNo=roomsNo, size=flatSize, price=price, pricePerM2=pricePerM2, link=link, pictureLink=pictureLink)
    #         offerCurrent = Flatcurrent(title=offerTitle, district=search_params['location'], roomsNo=roomsNo, size=flatSize, price=price, pricePerM2=pricePerM2, link=link, pictureLink=pictureLink)       
    #         db.session.add(offer)
    #         db.session.add(offerCurrent)

    # # 6. Domiporta.pl
    # if 'domiporta' in search_params['source']:
    #     Links = DomiPorta.getOfferLinks(search_params)
    #     for link in Links:
    #         # print('Current domiporta link: ' + link)
    #         offerTitle, flatSize, roomsNo, price, offerSource, pictureLink = DomiPorta.getOfferDetailsDomiPorta(link)
    #         pricePerM2 = str(round(float(price) / float(flatSize), 0))
    #         offer = Flat(title=offerTitle, district=search_params['location'], roomsNo=roomsNo, size=flatSize, price=price, pricePerM2=pricePerM2, link=link, pictureLink=pictureLink)
    #         offerCurrent = Flatcurrent(title=offerTitle, district=search_params['location'], roomsNo=roomsNo, size=flatSize, price=price, pricePerM2=pricePerM2, link=link, pictureLink=pictureLink)       
    #         db.session.add(offer)
    #         db.session.add(offerCurrent)

    # for item in currentSearchResults:
    #     offerCurrent = Flatcurrent(title=item('title'), district=search_params['location'], roomsNo=item('roomsNo'), size=item('size'), price=item('price'), pricePerM2=item('pricePerM2'), link=item('link'), pictureLink=item('pictureLink'))       
    #     db.session.add(offerCurrent)
    db.session.commit()
    # return searchString

####



# # TODO4: Run searches throuh different portals
# offerNum = 1
# # 1. Nieruchomosci-Online.pl
# Links = NieruchomosciOnline.getOfferLinks(search1.unifiedQuery())
# for link in Links:
#     offerTitle, flatSize, roomsNo, price, offerSource = NieruchomosciOnline.getOfferDetails(link)
#     Offer_offerNum = flatOffer(offerTitle, price, roomsNo, flatSize, offerSource, link)
#     # Check if criterias are met for portals that cannot specify all conditions from query
# ##    pricePerM2 = str(round(float(price) / float(flatSize), 0))
# ##    if (float(price) / float(flatSize)) > float(search1.pricePerM2max):
# ##        continue
#     if float(Offer_offerNum.pricePerM2) > float(search1.pricePerM2max):
#         continue
#     else:
#         Offer_offerNum.flatOfferExport()
#         offerNum += 1
    
# ### 2. OLX.pl
# ##Links = OLX.getOfferLinks(search1.unifiedQuery())
# ##for link in Links:
# ##    if 'www.otodom.pl' in link:
# ##        offerTitle, flatSize, roomsNo, price, offerSource = OLX.getOfferDetailsOTODOM(link)
# ##    else:
# ##        offerTitle, flatSize, roomsNo, price, offerSource = OLX.getOfferDetailsOLX(link)
# ##    pricePerM2 = str(round(float(price) / float(flatSize), 0))
# ##    writeOffer()
# ##

# ##



