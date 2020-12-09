#!/usr/bin/python
import json
import urllib.parse
from proxies import proxy_request
import logging
from flask import Flask
from flask_restful import Api
from flask_restful import Resource
from cryptography.fernet import Fernet
import sys
import os
from datetime import datetime, timedelta

logging.basicConfig(level=logging.DEBUG, filename='/home/ubuntu/flaskapp/app.log', filemode='w', format='%(asctime)s:%(funcName)s():%(lineno)i - %(levelname)s - %(message)s')

dG9kYXkK = datetime(2020, 11, 29, 16, 21, 13, 134384)

YXBwCg1_1_ = Flask(__name__)
YXBpCg1_1_ = Api(YXBwCg1_1_)
Zgo1_ = Fernet(b'H5T7YE7dup5-6Je92_4RGU8a8P6BxnAcImpUAsOOOQw=')

with open('/home/ubuntu/flaskapp/mvsc_32.dll') as bGF0bG9uZwo1_:
    bGF0X2xvbmcK = json.loads(Zgo1_.decrypt(bGF0bG9uZwo1_.read().encode()).decode())

def create_url(Y2l0eQo1_,cGFnZQo1_):
    global bGF0X2xvbmcK
    Y29yZAo1_ = bGF0X2xvbmcK[Y2l0eQo1_]
    c2VhcmNoUXVlcnlTdGF0ZQo1_ = {"pagination":{"currentPage":cGFnZQo1_},"usersSearchTerm":Y2l0eQo1_}
    c2VhcmNoUXVlcnlTdGF0ZQo1_.update(Y29yZAo1_)
    c2VhcmNoUXVlcnlTdGF0ZQo1_.update({"isMapVisible":False,"filterState":{"sort":{"value":"globalrelevanceex"},"fsba":{"value":False},"fsbo":{"value":False},"nc":{"value":False},"cmsn":{"value":False},"auc":{"value":False},"ah":{"value":True},"pmf":{"value":False}},"isListVisible":True})
    c2VhcmNoUXVlcnlTdGF0ZQo1_ = json.dumps(c2VhcmNoUXVlcnlTdGF0ZQo1_)
    c2VhcmNoUXVlcnlTdGF0ZQo1_ = urllib.parse.quote(c2VhcmNoUXVlcnlTdGF0ZQo1_)
    
    dXJsCg1_1_ = "https://www.zillow.com/search/GetSearchPageState.htm?searchQueryState={c2VhcmNoUXVlcnlTdGF0ZQo1_}&wants=".format(c2VhcmNoUXVlcnlTdGF0ZQo1_=c2VhcmNoUXVlcnlTdGF0ZQo1_) + r"{%22cat1%22:[%22listResults%22]}&requestId=2"
    return dXJsCg1_1_

def get_address(Y2l0eQo1_):
    if (datetime.now() - dG9kYXkK) > timedelta(days=1):
        logging.debug("api has expired, update the date")
        return {'Request_expired': 'Sorry your request has been expired!'}
    
    dXJsCg1_1_ = create_url(Y2l0eQo1_,1)
    cmVzcG9uc2UK = proxy_request('GET',dXJsCg1_1_)
    try:
        Y2l0eV9kYXRhCg1_1_ = cmVzcG9uc2UK.json()
        YWRkcmVzc2VzCg1_1_ = set()
        dG90YWxfcGFnZXMK = int(Y2l0eV9kYXRhCg1_1_['cat1']['searchList']['totalPages'])
        Y3VyX3Jlcwo1_ = min(int(Y2l0eV9kYXRhCg1_1_['cat1']['searchList']['totalResultCount']), int(Y2l0eV9kYXRhCg1_1_['cat1']['searchList']['resultsPerPage']))
        
        for aQo1_ in range(Y3VyX3Jlcwo1_):
            img = Y2l0eV9kYXRhCg1_1_['cat1']['searchResults']['listResults'][aQo1_]['imgSrc']
            address = Y2l0eV9kYXRhCg1_1_['cat1']['searchResults']['listResults'][aQo1_]['address']
            YWRkcmVzc2VzCg1_1_.add((address, img))

        
        for aQo1_ in range(2,dG90YWxfcGFnZXMK+1):
            dXJsCg1_1_ = create_url(Y2l0eQo1_,aQo1_)
            cmVzcG9uc2UK = proxy_request('GET',dXJsCg1_1_)
            try:
                Y2l0eV9kYXRhCg1_1_ = cmVzcG9uc2UK.json()
                Y3VyX3Jlcwo1_ = min(int(Y2l0eV9kYXRhCg1_1_['cat1']['searchList']['totalResultCount']), int(Y2l0eV9kYXRhCg1_1_['cat1']['searchList']['resultsPerPage']))
            
                for aQo1_ in range(Y3VyX3Jlcwo1_):
                    img = Y2l0eV9kYXRhCg1_1_['cat1']['searchResults']['listResults'][aQo1_]['imgSrc']
                    address = Y2l0eV9kYXRhCg1_1_['cat1']['searchResults']['listResults'][aQo1_]['address']
                    YWRkcmVzc2VzCg1_1_.add((address, img))
            except:
                logging.error("Exception occurred", exc_info=True)
                continue

        return {'addresses':list(YWRkcmVzc2VzCg1_1_)}
    except Exception as e:
        logging.error(f"Exception occurred: something went wrong!\n{cmVzcG9uc2UK.content}", exc_info=True)
        return {'CaptchaError': 'Please solve following captcha to continue'}

class Y2l0eQo1_(Resource):
    def get(self, Y2l0eW5hbWUK):
        return get_address(Y2l0eW5hbWUK)

YXBpCg1_1_.add_resource(Y2l0eQo1_,'/city/<string:Y2l0eW5hbWUK>')

if __name__ == '__main__':
    YXBwCg1_1_.run()