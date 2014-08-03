from locations import *
import time
from datetime import datetime
import pytz
import json
import tweepy
#import tweepy.streaming
from pymongo import Connection
#import nltk
import re
import string
import urllib, pprint
#import cPickle as pickle
import os
import sys
from pygeocoder import Geocoder

# cities = ['Chicago', 'Miami', 'Los Angeles', 'New York', 'San Francisco', 'Washington DC']
# genres = ['country', 'electronic', 'hiphop', 'indie', 'jazz', 'metal', 'pop', 'reggae', 'rnb', 'rock']
music = {}
# genre = {}

a = [line.strip() for line in open('country.txt')]
b = [line.strip() for line in open('electronic.txt')]
c = [line.strip() for line in open('hiphop.txt')]
d = [line.strip() for line in open('indie.txt')]
e = [line.strip() for line in open('jazz.txt')]
f = [line.strip() for line in open('metal.txt')]
g = [line.strip() for line in open('pop.txt')]
h = [line.strip() for line in open('reggae.txt')]
i = [line.strip() for line in open('rnb.txt')]
j = [line.strip() for line in open('rock.txt')]
# print a
# print '\n'
# print '\n'
# print b
# print '\n'
# print '\n'
# print c
# print '\n'
# print '\n'
# print d
# print '\n'
# print '\n'
# print e
# print '\n'
# print '\n'
# print f
# print '\n'
# print '\n'
# print g
# print '\n'
# print '\n'
# print h
# print '\n'
# print '\n'
# print i
# print '\n'
# print '\n'
# print j
# print '\n'
# print '\n'

class Parser:
	"""Parse tweets from the cache"""
	def __init__(self, *args, **kwargs):
		#self.keywords = list(pickle.load(open("keywords.pickled")))
		self.conn = Connection()
		self.cache = self.conn.buzz.cache
		self.tweets = self.conn.buzz.tweets
		self.keywords = self.conn.buzz.keywords
		self.loc_conn = Location_Conn()
		self.conductor()

	
	def conductor(self):
		while True:
			if self.cache.count() < 10:
				time.sleep(60)
			else:
				for tweet in self.cache.find(timeout=False).limit(1000):
					self.parseTweet(tweet)				
		

	def geolocate(self,longlat):
		return self.loc_conn.hood(longlat)


	def tweetLocate(self, lat, long):
		try:
			results = Geocoder.reverse_geocode(lat, long)
			city = results[0].city
			country = results[0].country

			if country != "United States":
				location = country
				return location
			elif city is None:
				location = "Unknown"
				return location
			else: 
				state = results[0].state
				location = city + ", " + state
				return location
		except:
			time.sleep(11)
		# print location
		# consumer_key='qZnzpvBV2uwKiF2e4kR5mg'
		# consumer_secret='E7ts8X242CfRKWBYMdTdXfwa3qyIHcEf2B76NUbQs'
		# access_token='1244598638-biVu1Hk4fiPMUTHO9HvYb09rXq7saMtNaevIt7S'
		# access_token_secret='75F3W2zKO0MsET6makez1sJVJKh9LpcgRefNQXLZWDg8M'

		# auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
		# auth.set_access_token(access_token, access_token_secret)

		# api = tweepy.API(auth)
		
		# try:
		# 	city = api.reverse_geocode(lat=lat, long=long, granularity='city')
		# 	# print dir(city[0])
		# 	name = city[0].full_name
		# 	return name
		# 	# print city[0].name
		# except tweepy.TweepError:
		# 	time.sleep(11)
		# except StopIteration:
		# 	pass
		
		

	def genre(self, artist):
		if artist in a:
			return "country"
		elif artist in b:
			return "electronic"
		elif artist in c:
			return "hiphop"
		elif artist in d:
			return "indie"
		elif artist in e:
			return "jazz"
		elif artist in f:
			return "metal" 
		elif artist in g:
			return "pop"
		elif artist in h:
			return "reggae"
		elif artist in i:
			return "R&B"
		elif artist in j:
			return "rock"
		else:
			return "unknown"


# 	def cleanup(self, text):
# 		x = str(text)
# 		# remove hashtags
# 		tweet =  re.sub(r'#.+( )', "", tweet)
# 		tweet =  re.sub(r'\"$', "", tweet)
# 		tweet =  re.sub(r'\".+\"', "", tweet)
# 		tweet =  re.sub(r'-\s+-', "-", tweet)
# 		tweet = tweet.replace("&amp;","and")
# 'Suspicious Minds"'
# 		# tweet =  re.sub(r'.+', "", tweet)
# 		return tweet



	def genDict(self, city, genres, artist, song):
		# if city not in dictionary, add it
		city = str(city)

		if city not in music.keys():
			music[city] = {}

			# if genres not in dictionary, add it
			if genres not in music[city].keys():
				music[city][genres] = {}

				if artist not in music[city][genres].keys():
					music[city][genres][artist] = [song]
				else: 
					music[city][genres][artist].append(song)
			else:
				if artist not in music[city][genres].keys():
					music[city][genres][artist] = [song]
				else: 
					music[city][genres][artist].append(song)
		
		# if city already in dictionary
		else:
			# if genres not in dictionary, add it
			if genres not in music[city].keys():
				music[city][genres] = {}

				if artist not in music[city][genres].keys():
					music[city][genres][artist] = [song]
				else: 
					music[city][genres][artist].append(song)
			else:
				if artist not in music[city][genres].keys():
					music[city][genres][artist] = [song]
				else: 
					music[city][genres][artist].append(song)

		print music
		print '\n'

		f = open('music.txt', 'w')
		json.dump(music, f)


	def parse2db(self, tweet, city, genre, artist, song_name):
		tweet['city'] = city
		tweet['artist'] = artist
		tweet['genre'] = genre
		tweet['song'] = song_name
		tid = tweet['id_str']
		# update cache
		self.cache.remove({'id_str' : tid})

		# insert tweet into db
		self.tweets.insert(tweet)


	def parseTweet(self,tweet,kw=False):
		text = tweet['text']
		# id = tweet['id_str']
		city = self.tweetLocate(tweet['lat'], tweet['long'])
		# tweet['city'] = city
		keys = text.split()
		# print tweet


		if "#nowplaying" in text:
			url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)

			# Float On by Modest Mouse is #nowplaying in Cricketers, Brighton. 
			if "by" in keys and "is" in keys:
				try:
					num = keys.index('by')
					num2 = keys.index('is')
					song_name = " ".join(keys[0:num])
					artist = " ".join(keys[num+1:num2])
					gnr = self.genre(artist)
					cit = tweet['city']
					# print song_name, " by ", artist, " in ", cit, " genre ", gnr
					self.genDict(cit, gnr, artist, song_name)
				except:
					pass

			# Bertine Zetlitz - Beautiful So Far #nowplaying
			elif len(keys) < 7 and "-" in keys:
				try:
					x = keys.index('#nowplaying')
					y = keys.index('-')
					song_name = " ".join(keys[0:y])
					artist = " ".join(keys[y+1:x])
					gnr = self.genre(artist)
					cit = tweet['city']
					# print song_name, " by ", artist, " in ", tweet['city']
					self.genDict(cit, gnr, artist, song_name)
				except:
					pass

			elif "#nowplaying" == keys[0]:
				#nowplaying "The Heavy - Short Change Hero" on http://t.co/lyVXgaY742
				if "on" in keys and "by" not in keys:
					try:
						x = keys.index('-')
						y = keys.index('#nowplaying')
						z = keys.index('on')
						artist = " ".join(keys[y+1:x])
						song_name = " ".join(keys[x+1:z])
						gnr = self.genre(artist)
						cit = tweet['city']
						# print song_name, " by ", artist, " in ", tweet['city']
						if '"' == list(artist)[0]:
							artist = ''.join(list(artist))[1:]
							self.genDict(cit, gnr, artist, song_name)
						if '"' == list(song_name)[len(song_name)-1]:
							song_name = ''.join(list(song_name))[0:len(song_name)-1]
							self.genDict(cit, gnr, artist, song_name)
						else:
							self.genDict(cit, gnr, artist, song_name)
					except:
						pass
				
				#nowplaying Rap God by Eminem http://t.co/FG3kaTECm2
				elif "by" in keys and "on" not in keys:
					try:
						x = keys.index('by')
						y = keys.index('#nowplaying')
						z = keys.index(url[0])
						song_name = " ".join(keys[y+1:x])
						artist = " ".join(keys[x+1:z])
						gnr = self.genre(artist)
						cit = tweet['city']
						# print song_name, " by ", artist, " in ", tweet['city']
						self.genDict(cit, gnr, artist, song_name)
					except:
						pass


		# """ ---------------------------------------------------------- """
		# I'm Listening to "Red Red Wine" by Tony Tribe (on Baked in the Sun) http://t.co/AgcwU6B65H via @Songza Android app
		elif "@Songza" in text:
			if "I'm Listening to" in text:
				try:
					x = keys.index('to')
					y = keys.index('by')
					url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)
					z = keys.index(url[0])
					song_name = " ".join(keys[x+2:y-1])
					artist = " ".join(keys[y+1:z])
					gnr = self.genre(artist)
					cit = tweet['city']
					# print song_name, " by ", artist, " in ", tweet['city']
					self.genDict(cit, gnr, artist, song_name)
				except:
					pass


		# """ ---------------------------------------------------------- """

		#nowplaying #peterfox ~ Peter Fox | Haus am See ||| BB RADIO - #bbradio
		elif "BB RADIO" in text or "Radio TEDDY" in text or "#bbradio" in text:
			if "~" in keys and "|" in keys and "|||" in keys:
				try:
					x = keys.index('~')
					y = keys.index('|')
					z = keys.index('|||')
					song_name = " ".join(keys[x+1:y])
					artist = " ".join(keys[y+1:z])
					gnr = self.genre(artist)
					cit = tweet['city']
					# print song_name, " by ", artist, " in ", tweet['city']
					self.genDict(cit, gnr, artist, song_name)
				except:
					pass

		# """ ---------------------------------------------------------- """
		
		elif "#Spotify" in text:

			# goes well with the trippy fog #NowPlaying The Golden Age  by  Beck
			if "#NowPlaying" in keys and "by" in text:
				try:
					x = keys.index('#NowPlaying')
					y = keys.index('by')
					z = keys.index('on')
					song_name = " ".join(keys[x+1:y])
					artist = " ".join(keys[y+1:z])
					gnr = self.genre(artist)
					cit = tweet['city']
					# print song_name, " by ", artist, " in ", tweet['city']
					self.genDict(cit, gnr, artist, song_name)
				except:
					pass
			
			#  #NowPlaying Life's Been Good by Joe Walsh on #Spotify  http://t.co/G8JNuQPfMm
			elif "#NowPlaying" in keys and "by" in text and "on" in text:
				try:
					x = keys.index('#NowPlaying')
					y = keys.index('by')
					z = keys.index('on')
					song_name = " ".join(keys[x+1:y])
					artist = " ".join(keys[y+1:z])
					gnr = self.genre(artist)
					cit = tweet['city']
					# print song_name, " by ", artist, " in ", tweet['city']
					self.genDict(cit, gnr, artist, song_name)
				except:
					pass

			# Drivin Around Song (feat. Jason Aldean)  by  Colt Ford on #Spotify
			elif "by" in text and "on" in text:
				try:
					x = keys.index('on')
					y = keys.index('by')
					song_name = " ".join(keys[0:y])
					artist = " ".join(keys[y+1:x])
					gnr = self.genre(artist)
					cit = tweet['city']
					# print song_name, " by ", artist, " in ", tweet['city']
					self.genDict(cit, gnr, artist, song_name)
				except:
					pass

		# """ ---------------------------------------------------------- """

		#NowPlaying Fortune Days - Glitch Mob
		elif "#NowPlaying" in keys and "#Spotify" not in text and len(keys) < 7:
			if "-" in keys:
				try:
					x = keys.index('-')
					song_name = " ".join(keys[1:x])
					artist = " ".join(keys[x+1:])
					gnr = self.genre(artist)
					cit = tweet['city']
					# print song_name, " by ", artist, " in ", tweet['city']
					self.genDict(cit, gnr, artist, song_name)
				except:
					pass

		# tweet['artist'] = artist
		# tweet['song'] = song
		#self.tweets.insert(tweet)
		#self.cache.remove({'id_str' : id})

	
Parser()		