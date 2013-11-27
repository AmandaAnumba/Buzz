from app import buzz
from models import *
from flask import render_template
from flask import request,url_for,redirect
from flask import Flask,jsonify
import urllib2,json
from datetime import timedelta
from flask import make_response, request,current_app
from functools import update_wrapper
#from parse_json import *
from settings import cities

def crossdomain(origin=None, methods=None, headers=None,
			max_age=21600, attach_to_all=True,
			automatic_options=True):
	if methods is not None:
		methods = ', '.join(sorted(x.upper() for x in methods))
	if headers is not None and not isinstance(headers, basestring):
		headers = ', '.join(x.upper() for x in headers)
	if not isinstance(origin, basestring):
		origin = ', '.join(origin)
	if isinstance(max_age, timedelta):
		max_age = max_age.total_seconds()

	def get_methods():
		if methods is not None:
			return methods

		options_resp = current_app.make_default_options_response()
		return options_resp.headers['allow']

	def decorator(f):
		def wrapped_function(*args, **kwargs):
			if automatic_options and request.method == 'OPTIONS':
				resp = current_app.make_default_options_response()
			else:
				resp = make_response(f(*args, **kwargs))
			if not attach_to_all and request.method != 'OPTIONS':
				return resp

			h = resp.headers

			h['Access-Control-Allow-Origin'] = origin
			h['Access-Control-Allow-Methods'] = get_methods()
			h['Access-Control-Max-Age'] = str(max_age)
			if headers is not None:
				h['Access-Control-Allow-Headers'] = headers
			return resp

		f.provide_automatic_options = False
		return update_wrapper(wrapped_function, f)
	return decorator


app = Flask(__name__)




#conn = Connection('localhost', 27017)



@buzz.route('/')
@buzz.route('/index')
@buzz.route('/index.html')
@buzz.route('/home')
@buzz.route('/home.html')
@crossdomain(origin='*', headers='Content-Type')
def index():
	return render_template("home.html")

@buzz.route('/about')
@buzz.route('/about.html')
@crossdomain(origin='*', headers='Content-Type')
def about():
	return render_template("about.html")

@buzz.route('/discover')
@buzz.route('/discover.html')
@crossdomain(origin='*', headers='Content-Type')
def about():
	return render_template("discover.html")

@buzz.route('/discover_<cityname>')
@buzz.route('/discover_<cityname>.html')
@crossdomain(origin='*', headers='Content-Type')
def discover(cityname):
	return render_template("cityview.html",
		cities = cities,
		city = cityname)


@buzz.route('/explore')
@buzz.route('/explore.html')
@crossdomain(origin='*', headers='Content-Type')
def explore():
	return render_template("explore.html",
		cities = cities)
	
@buzz.route('/city')
@buzz.route('/city.html')
@crossdomain(origin='*', headers='Content-Type')
def city():
	return render_template("city.html")


@buzz.route('/keywords')
@crossdomain(origin='*', headers='Content-Type')
def keywords():
	return redirect(url_for('static/json',filename='keywordtable.json'))	
		
@buzz.route('/test')
@buzz.route('/test.html')
@crossdomain(origin='*', headers='Content-Type')
def test():
	return render_template("test.html")	

	
	
	
