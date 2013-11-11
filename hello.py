from models import *
from flask import render_template
from flask import request
from flask import Flask

app = Flask(name)




conn = Connection()



@hello.route('/')
@hello.route('/index')
def index():
	cities = [c['city'] for c in conn.buzz.locations.find()]
	kwdata = {}
	for c in cities:
		kwdata[c] = [k['text'] for k in conn.buzz.keywords.find({"type" : "c", "city" : c}).sort("count",-1)]
	return render_template('tweets/index.html',
		title="buzz",
		cities = cities,
		keywords = kwdata)
		
@buzz.route('/pie')
def pie():
	cities = [c['city'] for c in conn.buzz.locations.find()]
	kwdata = {}
	for c in cities:
		kwdata[c] = [k['text'] for k in conn.buzz.keywords.find({"type" : "c", "city" : c}).sort("count",-1)][:5]	
	return render_template("pie.html",
		cities = cities)