from requests import Request, Session
from flask import Markup

import pprint
import json
import os

def retrieveAPI_KEY():
	if 'cmcAPI_KEY' in os.environ:
		API_KEY = os.environ['cmcAPI_KEY'].strip()
		return(API_KEY)
	else:
		return(None)

def retrievedotenvkey(envkey):
	if envkey in os.environ:
		API_KEY = os.environ[envkey].strip()
		return(API_KEY)
	else:
		if envkey == 'freecurrapi':
			return('err10')
		else:
			return('err11')

def getSGDUSDrate():
	## Currency Rate Query API ##<<------------------------------------

	API_KEY = retrievedotenvkey('freecurrapi')
	if API_KEY == 'err10':
		return('err10')

	api_exch_url = 'https://freecurrencyapi.net/api/v2/latest?apikey='+API_KEY+'&base_currency=USD'
	headers = {
    	'Accepts': 'application/json'}

	session = Session()
	session.headers.update(headers)
	exchngrates = session.get(api_exch_url)
	exUSDSGD = json.loads(exchngrates.text)['data']['SGD']
	return(exUSDSGD)


def getCMCquotesRESTapi(usdrate,fcInput):
	## CMC QUERY API ##<<------------------------------------
	apiendpoint_url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'

#	apikey = retrieveAPI_KEY()
	API_KEY = retrievedotenvkey('cmcAPI_KEY')
	if API_KEY == 'err11':
		return('err11')
	qcoins = str(fcInput).strip()
	if not qcoins:
		qcoins = 'LTC,CAKE,BNB,CRO,DFI,BTC,MATIC'

	querycoins = { 
    	           'symbol': qcoins }
	headers = {
    	'Accepts': 'application/json',
    	'X-CMC_PRO_API_KEY': str(API_KEY)
	}
	session = Session()
	session.headers.update(headers)

	## Get CMC quote data with API key ##
	try:
		apidata = session.get(apiendpoint_url, params=querycoins)
	except Session.RequestException as e:
		retrun('err11')
#	apidata = session.get(apiendpoint_url, params=querycoins)

	dataall = json.loads(apidata.text)['data']
	data = dataall

	exUSDSGD = usdrate
	exSGDUSD = round(1/exUSDSGD, 4)

	dispaltcolor = 0
	disptext = Markup(' :<br>')
	for coinsymbol in data:
		nest1 = data[coinsymbol]
		tokensymbol = coinsymbol
		quoteUSDprice = nest1['quote']['USD']['price']
		perchg1h = nest1['quote']['USD']['percent_change_1h']
		perchg24h = nest1['quote']['USD']['percent_change_24h']
		perchg30d = nest1['quote']['USD']['percent_change_30d']
		coinID = nest1['id']
		curr_price = round(quoteUSDprice,2)
		curr_priceSGD = round(quoteUSDprice*exUSDSGD,2)
		perchg1h = round(perchg1h,2)
		perchg24h = round(perchg24h,2)
		perchg30d = round(perchg30d,2)
		if dispaltcolor < 1: 
			disptext = disptext + Markup('<tr><td><font color="#71EFA3"> ' + tokensymbol + '</td><td><font color="#71EFA3">$' + str(curr_price) +
    	                      '</td><td> $' + str(curr_priceSGD) +
        	                  ' </td><td><font color="#71EFA3">' + str(perchg1h) + '% </td><td><font color="#71EFA3"> ' + str(perchg24h) +'% </td><td> ' + 
            	              str(perchg30d) + '% </td> ------</font></tr>') 
			dispaltcolor = 1
		else:
			disptext = disptext + Markup('<tr><td><font color="#FF9966">' + tokensymbol + '</td><td><font color="#FF9966">$' + str(curr_price) +
           		              '</td><td> $' + str(curr_priceSGD) +
               		          ' </td><td><font color="#FF9966">' + str(perchg1h) + '% </td><td><font color="#FF9966"> ' + str(perchg24h) +'% </td><td> ' + 
                   		      str(perchg30d) + '% </td> ------</font></tr>') 
			dispaltcolor = 0
	return(disptext)
