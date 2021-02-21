#! python3
# runFlatSearch.py - main run file for flat offer search

from app import app, db
from app.scraping_scripts import NieruchomosciOnline, OLX, Gratka, Gumtree, Sprzedajemy, DomiPorta
from app.models import User, Flat, Flatcurrent
import bs4, requests, json, logging, pprint

def runFlatSearch(search_params):

    Flatcurrent.query.delete()
    db.session.commit()

    # # flatOfferArray = []
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
    # Links = OLX.getOfferLinks(search_params)
    # for link in Links:
    #     if 'www.otodom.pl' in link:
    #         offerTitle, flatSize, roomsNo, price, offerSource = OLX.getOfferDetailsOTODOM(link)
    #     else:
    #         offerTitle, flatSize, roomsNo, price, offerSource = OLX.getOfferDetailsOLX(link)
    #     pricePerM2 = str(round(float(price) / float(flatSize), 0))
    #     offer = Flat(title=offerTitle, district=search_params['location'], roomsNo=roomsNo, size=flatSize, price=price, pricePerM2=pricePerM2, link=link)
    #     offerCurrent = Flatcurrent(title=offerTitle, district=search_params['location'], roomsNo=roomsNo, size=flatSize, price=price, pricePerM2=pricePerM2, link=link)
    #     db.session.add(offer)
    #     db.session.add(offerCurrent)

    # 3. Gratka.pl
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

    # 4. Gumtree.pl
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

    # # 5. Sprzedajemy.pl
    # Links = Sprzedajemy.getOfferLinks(search_params)
    # for link in Links:
    #     offerTitle, flatSize, roomsNo, price, offerSource = Sprzedajemy.getOfferDetailsSprzedajemy(link)
    #     pricePerM2 = str(round(float(price) / float(flatSize), 0))
    #     offer = Flat(title=offerTitle, district=search_params['location'], roomsNo=roomsNo, size=flatSize, price=price, pricePerM2=pricePerM2, link=link)
    #     offerCurrent = Flatcurrent(title=offerTitle, district=search_params['location'], roomsNo=roomsNo, size=flatSize, price=price, pricePerM2=pricePerM2, link=link)        
    #     db.session.add(offer)
    #     db.session.add(offerCurrent)

    # # 6. Domiporta.pl
    # Links = DomiPorta.getOfferLinks(search_params)
    # for link in Links:
    #     offerTitle, flatSize, roomsNo, price, offerSource = DomiPorta.getOfferDetailsDomiPorta(link)
    #     pricePerM2 = str(round(float(price) / float(flatSize), 0))
    #     offer = Flat(title=offerTitle, district=search_params['location'], roomsNo=roomsNo, size=flatSize, price=price, pricePerM2=pricePerM2, link=link)
    #     offerCurrent = Flatcurrent(title=offerTitle, district=search_params['location'], roomsNo=roomsNo, size=flatSize, price=price, pricePerM2=pricePerM2, link=link)        
    #     db.session.add(offer)
    #     db.session.add(offerCurrent)

    db.session.commit()

    search_done = 1

    return search_done

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



