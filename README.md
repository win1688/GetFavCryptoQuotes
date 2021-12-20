# GetFavCryptoQuotes

Title : Get favourite COINS/TOKEN quotes from CMC. Rel: 1.0 [21Q4]


This script creates a webserver to display my/your favourites 
crypto coins/tokens from CoinMarketCAP.

You will need to get your own API-KEY from https://pro.coinmarketcap.com/signup/ and 
create a cmcAPI_KEY environemnt variable that will be used to access latest quotes 
from CMC. cmcAPI_KEY=api-key-fromCMC-xxxbbbcccddd or enter via Heroku dashboard 


Clone this repo to your own repo and modifiy 'querycoins' variable in queryCMC.py
to display your favourite coins/tokens:

function :- getCMCquotesRESTapi()

	querycoins = { 
    	           'symbol':'LTC,CAKE,BNB,CRO,DFI,BTC,MATIC' }

Roadmap: Release 2.0 to get user input for favourite coins

