#! python3
# runFlatSearch.py - main run file for flat offer search
# import NieruchomosciOnline, OLX, Gratka, Gumtree, Sprzedajemy, DomiPorta
from app import app, db
from app.scraping_scripts import NieruchomosciOnline, OLX, Gratka, Gumtree
from app.models import User, Flat, Flatcurrent
import bs4, requests, json, logging, pprint

def runFlatSearch(search_params):

    Flatcurrent.query.delete()

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

    # # 2. OLX.pl
    # Links = OLX.getOfferLinks(search_params)
    # for link in Links:
    #     if 'www.otodom.pl' in link:
    #         offerTitle, flatSize, roomsNo, price, offerSource = OLX.getOfferDetailsOTODOM(link)
    #     else:
    #         offerTitle, flatSize, roomsNo, price, offerSource = OLX.getOfferDetailsOLX(link)
    #     pricePerM2 = str(round(float(price) / float(flatSize), 0))
    #     offer = Flat(title=offerTitle, district=search_params['location'], roomsNo=roomsNo, size=flatSize, price=price, pricePerM2=pricePerM2, link=link)
    #     db.session.add(offer)

    # 3. Gratka.pl
    Links = Gratka.getOfferLinks(search_params)
    for link in Links:
        offerTitle, flatSize, roomsNo, price, offerSource = Gratka.getOfferDetailsGratka(link)
        pricePerM2 = str(round(float(price) / float(flatSize), 0))
        offer = Flat(title=offerTitle, district=search_params['location'], roomsNo=roomsNo, size=flatSize, price=price, pricePerM2=pricePerM2, link=link)
        offerCurrent = Flatcurrent(title=offerTitle, district=search_params['location'], roomsNo=roomsNo, size=flatSize, price=price, pricePerM2=pricePerM2, link=link)        
        db.session.add(offer)
        db.session.add(offerCurrent)

    # 4. Gumtree.pl
    Links = Gumtree.getOfferLinks(search_params)
    for link in Links:
        offerTitle, flatSize, roomsNo, price, offerSource = Gumtree.getOfferDetailsGumtree(link)
        pricePerM2 = str(round(float(price) / float(flatSize), 0))
        offer = Flat(title=offerTitle, district=search_params['location'], roomsNo=roomsNo, size=flatSize, price=price, pricePerM2=pricePerM2, link=link)
        offerCurrent = Flatcurrent(title=offerTitle, district=search_params['location'], roomsNo=roomsNo, size=flatSize, price=price, pricePerM2=pricePerM2, link=link)        

        # Check if criterias are met for portals that cannot specify all conditions from query
        if (float(price) / float(flatSize)) > float(search_params['pricePerM2max']):
            continue
        if (float(flatSize) < float(search_params['flatSizeMin']) or float(flatSize) > float(search_params['flatSizeMax'])):
            continue
        db.session.add(offer)
        db.session.add(offerCurrent)

    db.session.commit()

####

# import bs4, requests, json, logging, pprint
# import NieruchomosciOnline, OLX, Gratka, Gumtree, Sprzedajemy, DomiPorta

# logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s -  %(levelname)s -  %(message)s')

# flatOfferArray = []
                    
# # # Get user search criteria - hardcoded for the moment
# # location = 'bemowo'
# # priceMin = '1'
# # priceMax = '450000'
# # pricePerM2min = '1'
# # pricePerM2max = '8500'
# # roomsNoSearch = '2'
# # flatSizeMin = '30'
# # flatSizeMax = '55'
# # market = 'wtorny'

# # Define search criteria class
# class searchQuery:

#     def __init__(self, location, priceMin, priceMax, pricePerM2min, pricePerM2max, roomsNoSearch, flatSizeMin, flatSizeMax, market):
#         self.location = location
#         self.priceMin = priceMin
#         self.priceMax = priceMax
#         self.pricePerM2min = pricePerM2min
#         self.pricePerM2max = pricePerM2max
#         self.roomsNoSearch = roomsNoSearch
#         self.flatSizeMin = flatSizeMin
#         self.flatSizeMax = flatSizeMax
#         self.market = market

#     # Create unified search query
#     def unifiedQuery(self):
#         self.queryCriteria = {
#             "location": self.location,
#             "priceMin": self.priceMin,
#             "priceMax": self.priceMax,
#             "pricePerM2min": self.pricePerM2min,
#             "pricePerM2max": self.pricePerM2max,
#             "roomsNoSearch": self.roomsNoSearch,
#             "flatSizeMin": self.flatSizeMin,
#             "flatSizeMax": self.flatSizeMax,
#             "market": self.market
#             }
#         return self.queryCriteria

# # Define class for a single flatOffer
# class flatOffer:

#     def __init__(self, offerTitle, price, roomsNo, flatSize, offerSource, url):
#         self.offerTitle = offerTitle.lower()
#         self.flatSize = flatSize        
#         self.roomsNo = roomsNo
#         self.price = price
#         self.pricePerM2 = str(round(float(price) / float(flatSize), 0))
#         self.offerSource = offerSource
#         self.url = url

#     def flatOfferExport(self):
#         flatOffer = {
#             "offerTitle": self.offerTitle,
#             "flatSize": self.flatSize,
#             "roomsNo": self.roomsNo,
#             "price": self.price,
#             "pricePerM2": self.pricePerM2,
#             "offerSource": self.offerSource,
#             "link": self.url
#             }
#         flatOfferArray.append(flatOffer)

# # Define functions for data processing
# def writeOffer():
#     flatOffer = {
#         "offerTitle": offerTitle,
#         "flatSize": flatSize,
#         "roomsNo": roomsNo,
#         "price": price,
#         "pricePerM2": pricePerM2,
#         "source": offerSource,
#         "link": link
#         }
#     flatOfferArray.append(flatOffer)

# # Run search
# search1 = searchQuery(location, priceMin, priceMax, pricePerM2min, pricePerM2max, roomsNoSearch, flatSizeMin, flatSizeMax, market)        
# #queryCriteria = search1.unifiedQuery()
# #pprint.pprint(queryCriteria)

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
# ### 3. Gratka.pl
# ##Links = Gratka.getOfferLinks(search1.unifiedQuery())
# ##for link in Links:
# ##    offerTitle, flatSize, roomsNo, price, offerSource = Gratka.getOfferDetailsGratka(link)
# ##    pricePerM2 = str(round(float(price) / float(flatSize), 0))
# ##    writeOffer()
# ##
# ### 4. Gumtree.pl
# ##Links = Gumtree.getOfferLinks(search1.unifiedQuery())
# ##for link in Links:
# ##    offerTitle, flatSize, roomsNo, price, offerSource = Gumtree.getOfferDetailsGumtree(link)
# ##    pricePerM2 = str(round(float(price) / float(flatSize), 0))
# ##
# ##    # Check if criterias are met for portals that cannot specify all conditions from query
# ##    if (float(price) / float(flatSize)) > float(search1.pricePerM2max):
# ##        continue
# ##    if (float(flatSize) < float(search1.pricePerM2min) or float(flatSize) > float(search1.pricePerM2max)):
# ##        continue
# ##    writeOffer()
# ##
# ### 5. Sprzedajemy.pl
# ##Links = Sprzedajemy.getOfferLinks(search1.unifiedQuery())
# ##for link in Links:
# ##    offerTitle, flatSize, roomsNo, price, offerSource = Sprzedajemy.getOfferDetailsSprzedajemy(link)
# ##    pricePerM2 = str(round(float(price) / float(flatSize), 0))
# ##    writeOffer()
# ##
# ### 6. Domiporta.pl
# ##Links = DomiPorta.getOfferLinks(search1.unifiedQuery())
# ##for link in Links:
# ##    offerTitle, flatSize, roomsNo, price, offerSource = DomiPorta.getOfferDetailsDomiPorta(link)
# ##    pricePerM2 = str(round(float(price) / float(flatSize), 0))
# ##    writeOffer()

# # Dump results to JSON file
# with open('flatData.json', 'w') as outfile:
#     json.dump(flatOfferArray, outfile)
    
# # TODO6: Dump results to DB
# pprint.pprint(flatOfferArray)

