from flask import Flask, Blueprint, render_template, request, flash, Markup
from requests import Request, Session
from datetime import datetime
from queryCMC import getCMCquotesRESTapi, getSGDUSDrate
import json
import pprint
import pytz

app = Flask(__name__)
#app.secret_key = "showmethemoney168"

views = Blueprint(__name__, "views")
viewq = Blueprint(__name__, "viewq")

@views.route("/")
def home():
	msg1 = Markup('###  Version 1.5 HOME Page - Default displays latest prices of my favourite Crypto Tokens <br>')
	msg2 = Markup('###  Option to enter the tokens you want to display. (Note:No error checking yet)<br>')
	msg3 = Markup('###  Will display "Internal Server Error" if symbols you entered is not valid or not supported by CMC<br>')
	flash(msg1 + msg2 + msg3)
	return render_template("index.html", favcoins="CRO,CAKE,LTC,MATIC,DFI,BNB", curr="SGD")
#	return "home getq page"

@views.route("/viewq", methods=["POST"])
def altcoins():
#
#	Get Exchange Rates
#
	exUSDSGD = getSGDUSDrate()
	if str(exUSDSGD) == 'err10':
		msg0 = Markup('Cannot get exchange rates from http://freecurrenyapi.net<br><br>')
		msg1 = Markup('Either environment variable key not configured or  <br>')
		msg2 = Markup('<span class="tab"></span>connection to source timeout or hourly retrieval quota exceeded<br><br><br>')
		msg3 = Markup('Environement variable (KEY/VALUE) : <br>')
		msg4 = Markup('<em><span class="tab"></span>KEY: freecurrapi <br><span class="tab"></span>VALUE : abcdefuuuddddkkkkgggadkfhakdj</em> <br>')
		flash(msg0 + msg1 + msg2 + msg3 + msg4)
		return render_template("noAPIKEY.html")


	exSGDUSD = round(1/exUSDSGD, 4)
#
#	Get Current Date/time
#
	tz = pytz.timezone('Asia/Manila')
	now = datetime.now(tz)

	dt_string = now.strftime("%d/%m/%Y Timezone GMT+8 : %H:%M:%S")
	fc = request.form['coin_input'] 
	cmcquotes = getCMCquotesRESTapi(exUSDSGD,fc)
	if cmcquotes == 'err11':
		msg0 = Markup('Cannot retrieves quotes from CMC. <br> Either environment vars key not configured or  <br>')
		msg1 = Markup('<span class="tab"></span>connection to source(CMC)timeout or hourly retrieval quota exceeded<br><br><br>')
		msg2 = Markup('<br>')
		msg3 = Markup(('Environement variable (KEY/VALUE) : <br>'))
		msg4 = Markup('<em><span class="tab"></span> cmcAPI_KEY=abcdefuuuddddkkkkgggadkfhakdj  </em> <br><br>')
		msg5 = Markup('Get Free API Key from https://pro.coinmarketcap.com/signup/  <br>')
		flash(msg0 + msg1 + msg2 + msg3 + msg4 + msg5)
		return render_template("noAPIKEY.html")
	else:
#		msg1 = Markup('Quotes from CMC as follows    <span class="tab"></span>   <span class="tab"></span>       Changes last 1h / 24h / 30d ')
#		flash(msg1 + cmcquotes)
		flash(cmcquotes)
		return render_template("dispQuotestable.html", exrate1=str(exUSDSGD), exrate2=str(exSGDUSD), currDT=dt_string, userinput=str(fc))
