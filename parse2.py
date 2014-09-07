# -*- coding: UTF-8 -*-

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
import urllib, pprint, urllib2
#import cPickle as pickle
import os
import sys
from pygeocoder import Geocoder

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



class Parser:
	"""Parse tweets from the cache"""
	def __init__(self, *args, **kwargs):
		#self.keywords = list(pickle.load(open("keywords.pickled")))
		self.conn = Connection()
		# self.cache = self.conn.buzz.cache
		self.tweets = self.conn.buzz.tweets
		self.allTweets = self.conn.buzz.allTweets
		self.conductor()

	
	def conductor(self):
		tids = []
		for tweet in self.tweetsDB.find(timeout=False):
			id = tweet['id_str']
			tids.append(id)
		# print tids, '\n'

		# tDB = []
		# for tweet in self.tweetsDB.find(timeout=False):
		# 	latlong = [tweet['lat'],tweet['long']]
		# 	location = tweet['city']
		# 	data = [latlong, location]
		# 	tDB.append(data)
		# pprint.pprint(tDB)

		# d = []
		# find = []
		# for tweet in self.tweets.find(timeout=False):
		# 	latlong = str([tweet['lat'],tweet['long']])
		# 	tid = tweet['id_str']
		# 	info = {
		# 		latlong : [tid,]
		# 	}

		# # pprint.pprint(d)

		# 	if len(d) == 0:
		# 		d.append(info)
		# 		find.append(latlong)

		# 	else:
		# 		if latlong in find:
		# 			for i in range(0,len(d)):
		# 				if latlong in d[i].keys():
		# 					d[i][latlong].append(tid)
		# 					break
		# 				else:
		# 					continue

		# 		else:
		# 			d.append(info)
		# 			find.append(latlong)

		# pprint.pprint(d)

		while True:
			if self.tweets.count() < 10:
				time.sleep(60)
			else:	
				for tweet in self.tweets.find(timeout=False):
					self.parseTweet(tweet)
					# self.compare(tweet, tDB)

		
		
	def compare(self, tweet, dataB):
		latlong = [tweet['lat'],tweet['long']]
		tid = tweet['id_str']

		# print latlong

		if 'city' not in tweet.keys():
			if  tweet['genre']:
				for data in dataB:
					if latlong == data[0]:
						tweet['city'] = data[1]
						pprint.pprint(tweet)
						print '\n'

						self.tweetsDB.insert(tweet)
						self.tweets.remove({'id_str' : tid})
						break

					else:
						pass
		else:
			if 'city' in tweet.keys():
				if tweet['city'] is not None:
					print "skipping this tweet", '\n'
					self.tweetsDB.insert(tweet)
					self.tweets.remove({'id_str' : tid})




	def parseTweet(self,tweet,kw=False):
		tid = tweet['id_str']
		
		if 'city' in tweet.keys() and tweet['city'] is not None:
			self.tweetsDB.insert(tweet)
			self.tweets.remove({'id_str' : tid})
			# pass


		else:
			if tweet['genre']:
				# city = self.geolocate(tweet['lat'], tweet['long'])
				city = self.geolocate(tweet['lat'], tweet['long'])
				
				if city is None:
					print "no city found"
					pass
				else:
					tweet['city'] = city
					# self.tweets.remove({'id_str' : tid})
					# self.tweetsDB.insert(tweet)
					pprint.pprint(tweet)
					print '\n'
					# self.tweets.save(tweet)
					self.tweetsDB.insert(tweet)
					self.tweets.remove({'id_str' : tid})
			else: 
				pass
			


	# def parseTweet(self,tweet,kw=False):
	# 	city = self.geolocate(tweet['lat'], tweet['long'])
	# 	song, artist, genre = self.getArtistSong(tweet)
		
	# 	if (city == None) or (city == "Unknown"):
	# 		print "no city found"
	# 		pass
	# 	else:
	# 		tweet['city'] = city

	# 	tweet['artist'] = artist
	# 	tweet['genre'] = genre
	# 	tweet['song'] = song

	# 	pprint.pprint(tweet)
	# 	print '\n'
	# 	tid = tweet['id_str']
		
	# 	# update cache
	# 	self.cache.remove({'id_str' : tid})

	# 	# insert tweet into db
	# 	self.tweets.insert(tweet)



	def geolocate(self, lat, long):
		# try:
		# 	results = Geocoder.reverse_geocode(lat, long)
		# 	city = results[0].city
		# 	country = results[0].country
		# 	location = ""

		# 	if city is None:
		# 		location = "Unknown"
		# 	else: 
		# 		state = results[0].state
		# 		location = city + ", " + state + ", " + country
			
		# 	return location
		# except:
		# 	time.sleep(11)
		# 
		try:
			url = 'http://maps.googleapis.com/maps/api/geocode/json?' + \
		            'latlng={},{}&sensor=false'.format(lat, long)
			jsondata = json.load(urllib.urlopen(url))
			# print jsondata['results'][0]
			# print data
			city = ""
			state = ""
			country = ""
			
			for i in range(0,len(jsondata['results'][0]['address_components'])):
				if jsondata['results'][0]['address_components'][i]['types'] == [ "locality", "political" ]:
					city = jsondata['results'][0]['address_components'][i]['long_name']
					# print city

				elif jsondata['results'][0]['address_components'][i]['types'] == [ "administrative_area_level_1", "political" ]:
					state = jsondata['results'][0]['address_components'][i]['long_name']
					# print state

				elif jsondata['results'][0]['address_components'][i]['types'] == [ "country", "political" ]:
					country = jsondata['results'][0]['address_components'][i]['long_name']
					# print country

			location = city + ", " + state + ", " + country
			# print location
			return location
		except:
			time.sleep(11)
	

	def getGenre(self, artist):
		if artist in a:
			return "country"
		if artist in b:
			return "electronic"
		if artist in c:
			return "hiphop"
		if artist in d:
			return "indie"
		if artist in e:
			return "jazz"
		if artist in f:
			return "metal" 
		if artist in g:
			return "pop"
		if artist in h:
			return "reggae"
		if artist in i:
			return "R&B"
		if artist in j:
			return "rock"
		else:
			return "unknown"


	def getArtistSong(self, tweet):
		text = tweet['text']
		username = tweet['user_name']
		keys = text.split()
		url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)
		song = ""
		artist = ""
		genre = ""

		# Float On by Modest Mouse is #nowplaying in Cricketers, Brighton. 
		if "by" and "is" and "#nowplaying" in text:
			try:
				x = keys.index('by')
				y = keys.index('is')
				song = " ".join(keys[0:x])
				artist = " ".join(keys[x+1:y])
				genre = self.getGenre(artist)
			except:
				pass

		# Bertine Zetlitz - Beautiful So Far #nowplaying
		if "-" and "#nowplaying" in text and "@" and "http:" not in text:
			try:
				x = keys.index('#nowplaying')
				y = keys.index('-')
				song = " ".join(keys[0:y])
				artist = " ".join(keys[y+1:x])
				genre = self.getGenre(artist)
			except:
				pass
		
		#nowplaying "The Heavy - Short Change Hero" on http://t.co/lyVXgaY742
		if "on" and "#nowplaying" in keys and "by" not in keys:
			try:
				x = keys.index('-')
				y = keys.index('#nowplaying')
				z = keys.index('on')
				artist = " ".join(keys[y+1:x])
				song = " ".join(keys[x+1:z])
				genre = self.getGenre(artist)
				
				if '"' == list(artist)[0]:
					artist = ''.join(list(artist))[1:]
				if '"' == list(song)[len(song)-1]:
					song = ''.join(list(song))[0:len(song)-1]
			except:
				pass	
				
		#nowplaying Rap God by Eminem http://t.co/FG3kaTECm2
		if "by" and "http:" and "#nowplaying" in text:
			try:
				x = keys.index('by')
				y = keys.index('#nowplaying')
				z = keys.index(url[0])
				song = " ".join(keys[y+1:x])
				artist = " ".join(keys[x+1:z])
				genre = self.getGenre(artist)
			except:
				pass

		#nowplaying Emma Kate's Accident by Bloc Party
		#nowplaying Strawberry Bubblegum by Justin Timberlake
		if "by" and "#nowplaying" in text and "http:" not in text:
			try:
				x = keys.index('by')
				y = keys.index('#nowplaying')
				song = " ".join(keys[y+1:x])
				artist = " ".join(keys[x+1:])
				genre = self.getGenre(artist)
			except:
				pass

		#nowPlaying fell on black days - soundgarden
		if "-" in keys and "#nowplaying" or "#nowPlaying" in text:
			if keys[0].lower() == "#nowplaying":
				try:
					x = keys.index('-')
					song = " ".join(keys[1:x])
					artist = " ".join(keys[x+1:])
					genre = self.getGenre(artist)
				except:
					pass

		# I'm Listening to "Red Red Wine" by Tony Tribe (on Baked in the Sun) http://t.co/AgcwU6B65H via @Songza Android app
		if "@Songza" and "(on Baked in the Sun)" in text:
			try:
				x = keys.index('to')
				y = keys.index('by')
				z = keys.index('(on')
				song = " ".join(keys[x+1:y])
				
				if '"' == list(song)[0] and '"' == list(song)[len(song)-1]:
					song = ''.join(list(song))[1:len(song)-1]

				artist = " ".join(keys[y+1:z])
				genre = self.getGenre(artist)
			except:
				pass

		#nowplaying #peterfox ~ Peter Fox | Haus am See ||| BB RADIO - #bbradio
		#nowplaying #petermaffay ~ Peter Maffay | Halleluja ||| Radio TEDDY - In #Kassel #GER auf 91.7
		#nowplaying #adele ~ Adele | Set Fire To The Rain ||| #bbradio
		if "BB RADIO" or "Radio TEDDY" or "#bbradio" in text:
			if "~" and "|" and "|||" in keys:
				try:
					x = keys.index('~')
					y = keys.index('|')
					z = keys.index('|||')
					artist = " ".join(keys[x+1:y])
					song = " ".join(keys[y+1:z])
					genre = self.getGenre(artist)
				except:
					pass

		# goes well with the trippy fog #NowPlaying The Golden Age  by  Beck
		if "#NowPlaying" and "by" in text:
			if "on" in text:
				try:
					x = keys.index('#NowPlaying')
					y = keys.index('by')
					z = keys.index('on')
					song = " ".join(keys[x+1:y])
					artist = " ".join(keys[y+1:z])
					genre = self.getGenre(artist)
				except:
					pass
			else:
				try:
					x = keys.index('#NowPlaying')
					y = keys.index('by')
					song = " ".join(keys[x+1:y])
					artist = " ".join(keys[y+1:])
					genre = self.getGenre(artist)
				except:
					pass
		
		#NowPlaying Life's Been Good by Joe Walsh on #Spotify  http://t.co/G8JNuQPfMm
		#NowPlaying Sweet Nothing de Calvin Harris en #Spotify  http://t.co/gcxalUXEBy"
		if "#NowPlaying" and "#Spotify" in text:
			if "by" and "on" in text:
				try:
					x = keys.index('#NowPlaying')
					y = keys.index('by')
					z = keys.index('on')
					song = " ".join(keys[x+1:y])
					artist = " ".join(keys[y+1:z])
					genre = self.getGenre(artist)
				except:
					pass

			if "de" and "en" in text:
				try:
					x = keys.index('#NowPlaying')
					y = keys.index('de')
					z = keys.index('en')
					song = " ".join(keys[x+1:y])
					artist = " ".join(keys[y+1:z])
					genre = self.getGenre(artist)
				except:
					pass

		# Drivin Around Song (feat. Jason Aldean)  by  Colt Ford on #Spotify
		if "#Spotify" and "by" and "on" in text and "#NowPlaying" not in text:
			try:
				x = keys.index('on')
				y = keys.index('by')
				song = " ".join(keys[0:y])
				artist = " ".join(keys[y+1:x])
				genre = self.getGenre(artist)
			except:
				pass

		#NowPlaying Fortune Days - Glitch Mob
		#NowPlaying california dreams - The Mamas and Papas
		if "#NowPlaying" and "-" in keys and "#Spotify" and "http:" not in text:
			try:
				x = keys.index('-')
				y = keys.index("#NowPlaying")
				song = " ".join(keys[y+1:x])
				artist = " ".join(keys[x+1:])
				genre = self.getGenre(artist)
			except:
				pass	

		# "PLACEBO 'Special Needs' #NowPlaying #Puebla http://t.co/8leyKvJNFo",
		# "The Chemical Brothers - Hey Boy Hey Girl #NowPlaying #Puebla http://t.co/VmpKJ4fjxi"
		# "Bryan Adams - Don't Give Up - Live at Slane Castle, Ireland #NowPlaying #Puebla http://t.co/p4oMiB0h38"
		if "#NowPlaying" and "#Puebla" in text:
			if "-" in keys:
				try:
					x = keys.index('-')
					y = keys.index('#NowPlaying')
					artist = " ".join(keys[0:x])
					song = " ".join(keys[x+1:y])
					genre = self.getGenre(artist)
				except:
					pass
			else:
				try:
					x = keys.index('PLACEBO')
					y = keys.index('#NowPlaying')
					artist = " ".join(keys[0:x])
					song = " ".join(keys[x+1:y])
					genre = self.getGenre(artist)
				except:
					pass
		
		#VirtualTwitter @HollywoodDub 6-10 @HOT1039SC #NowPlaying @IamRicoLove #TheyDontKnow #TTLO http://t.co/0Os81b7VKr
		#VirtualTwitter @HollywoodDub 6-10 @HOT1039SC #NowPlaying @TreySongz #OooNaNa prod by @DJmustard http://t.co/e6kGsdHGXs"
		#VirtualTwitter @HollywoodDub 6-10 @HOT1039SC #NowPlaying @ScHoolBoyQ #ManOfTheYear prod by @NEZandRIO http://t.co/e6kGsdHGXs
		if "@HollywoodDub" and "#VirtualTwitter" and "#NowPlaying" in text:
			try:
				mentions = tweet['entities']['user_mentions']
				x = keys.index('#NowPlaying')
				artist_tag = "".join(list(" ".join(keys[x+1:x+2]))[1:])
				
				for i in range(0,len(mentions)):
					if mentions[i]['screen_name'] == artist_tag:
						artist = mentions[i]['name']

				song = "".join(list(" ".join(keys[x+2:x+3]))[1:])		
				genre = self.getGenre(artist)
			except:
				pass

		#NowPlaying @Pantera #5MinutesAlone on @HardDrivinRadio @soundtracking... ♫ \"5 Minutes Alone\" by @OfficialPantera http://t.co/m6GmUOtB9P
		#NowPlaying @slipknot #Psychosocial on @HardDrivinRadio soundtracking #METAL #MetalHead #MetalRules @… http://t.co/cfN92QwmA
		#NowPlaying @Korn #Blind on @HardDrivinRadio @soundtracking #AreYouReady #Metal #MetalHead... ♫ \"Blind\" by @Korn http://t.co/ng85unj1qM
		#NowPlaying @slipknot #Psychosocial on @HardDrivinRadio soundtracking #METAL #MetalHead #MetalRules @… http://t.co/cfN92QwmAa",
		#NowPlaying pantera dimebagdarrellofficial #5MinutesAlone on @HardDrivinRadio #Metal #OldSchoolMetal… http://t.co/g9QqpwMY5G",
		#NowPlaying korn #Blind on @HardDrivinRadio soundtracking #AreYouReady #Metal #MetalHead #MetalRules @… http://t.co/aHKVDrHeiw
		#NowPlaying @METALLICA #SuicideAndRedemption on @HardDrivinRadio ... ♫ \"Suicide &amp; Redemption\" by @Metallica http://t.co/ndAdVhrLcB
		if "#NowPlaying" and "@HardDrivinRadio" in text and username == "Jessie James":
			try:
				mentions = tweet['entities']['user_mentions']
				x = keys.index('#NowPlaying')
				artist_tag = " ".join(keys[x+1:x+2])

				if list(artist_tag)[0] == "@":
					a_tag = "".join(list(artist_tag)[1:])
				
				for i in range(0,len(mentions)):
					if mentions[i]['screen_name'] == a_tag:
						artist = mentions[i]['name']

				song_tag = " ".join(keys[x+2:x+3])
				if list(song_tag)[0] != "#":
					song = "".join(list(" ".join(keys[x+3:x+4]))[1:])
				else:
					song = "".join(list(song_tag)[1:])

				genre = self.getGenre(artist)
			except:
				pass

		#NowPlaying Message In A Bottle (Acoustic cover) by #30SecondstoMars via http://t.co/Tyd0NlXQjj",
		#NowPlaying Here In My Room by #Incubus via http://t.co/Tyd0NlXQjj
		#NowPlaying Porfirio Diaz by #AtTheDriveIn via http://t.co/Tyd0NlXQjj"
		#NowPlaying Eviction Article by #BoySetsFire via http://t.co/Tyd0NlXQjj",
		if "#NowPlaying" and "by" and "via" and "http:" in text and username == "Rodrigo Salxixa Leal":
			try:
				x = keys.index('#NowPlaying')
				y = keys.index('by')
				z = keys.index('via')
				song = " ".join(keys[x+1:y])
				artist_tag = " ".join(keys[y+1:z])
				
				if list(artist_tag)[0] == "#":
					artist_tag = "".join(list(artist_tag)[1:])
					if artist_tag == "30SecondstoMars":
						artist = "30 Seconds to Mars"
					else:
						artist = " ".join(re.findall('[A-Z][^A-Z]*', artist_tag))

				genre = self.getGenre(artist)
			except:
				pass

		return song, artist, genre


Parser()		