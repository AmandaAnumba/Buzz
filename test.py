# -*- coding: UTF-8 -*-

from locations import *
import sys
import time
from datetime import datetime
import pytz
import json
import tweepy, os, sys
#import tweepy.streaming
from pymongo import Connection
#import nltk
import re
import string
import cPickle as pickle
import urllib, pprint, urllib2
from pygeocoder import Geocoder


def main(text):
	username = "Rodrigo Salxixa Leal"
	keys = text.split()
	url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)
	song = ""
	artist = ""
	genre = "unknown"

	# Float On by Modest Mouse is #nowplaying in Cricketers, Brighton. 
	if "by" and "is" and "#nowplaying" in text:
		try:
			x = keys.index('by')
			y = keys.index('is')
			song = " ".join(keys[0:x])
			artist = " ".join(keys[x+1:y])
			# return song, artist, genre
		except Exception:
			pass

	# Bertine Zetlitz - Beautiful So Far #nowplaying
	if "-" and "#nowplaying" in text and "@" and "http:" not in text:
		try:
			x = keys.index('#nowplaying')
			y = keys.index('-')
			song = " ".join(keys[0:y])
			artist = " ".join(keys[y+1:x])
			# return song, artist, genre
		except Exception:
			pass
	
	#nowplaying "The Heavy - Short Change Hero" on http://t.co/lyVXgaY742
	if "on" and "#nowplaying" in keys and "by" not in keys:
		try:
			x = keys.index('-')
			y = keys.index('#nowplaying')
			z = keys.index('on')
			artist = " ".join(keys[y+1:x])
			song = " ".join(keys[x+1:z])
			
			if '"' == list(artist)[0]:
				artist = ''.join(list(artist))[1:]
			if '"' == list(song)[len(song)-1]:
				song = ''.join(list(song))[0:len(song)-1]
			# return song, artist, genre
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
			# return song, artist, genre
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
			# return song, artist, genre
		except:
			pass

	#nowPlaying fell on black days - soundgarden
	if "-" in keys and "#nowplaying" or "#nowPlaying" in text:
		if keys[0].lower() == "#nowplaying":
			try:
				x = keys.index('-')
				song = " ".join(keys[1:x])
				artist = " ".join(keys[x+1:])
				# return song, artist, genre
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
			# return song, artist, genre
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
				# return song, artist, genre
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
				# return song, artist, genre
			except:
				pass
		else:
			try:
				x = keys.index('#NowPlaying')
				y = keys.index('by')
				song = " ".join(keys[x+1:y])
				artist = " ".join(keys[y+1:])
				# return song, artist, genre
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
				# return song, artist, genre
			except:
				pass

		if "de" and "en" in text:
			try:
				x = keys.index('#NowPlaying')
				y = keys.index('de')
				z = keys.index('en')
				song = " ".join(keys[x+1:y])
				artist = " ".join(keys[y+1:z])
				# return song, artist, genre
			except:
				pass

	# Drivin Around Song (feat. Jason Aldean)  by  Colt Ford on #Spotify
	if "#Spotify" and "by" and "on" in text and "#NowPlaying" not in text:
		try:
			x = keys.index('on')
			y = keys.index('by')
			song = " ".join(keys[0:y])
			artist = " ".join(keys[y+1:x])
			# return song, artist, genre
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
			# return song, artist, genre
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
				# return song, artist, genre
			except:
				pass
		else:
			try:
				x = keys.index('PLACEBO')
				y = keys.index('#NowPlaying')
				artist = " ".join(keys[0:x])
				song = " ".join(keys[x+1:y])
				# return song, artist, genre
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
			# return song, artist, genre	
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
			# return song, artist, genre
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
			# return song, artist, genre
		except:
			pass
	return song, artist, genre
	


if __name__ == "__main__":
    text = '#NowPlaying Message In A Bottle (Acoustic cover) by #30SecondstoMars via http://t.co/Tyd0NlXQjj",'
    song, artist, genre = main(text)
    print "Song: ", song, "    Artist: ", artist
	