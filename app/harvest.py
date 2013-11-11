'''
Command to harvest keywords on the fly
Jason Cohn 10/21/2013
''' 

from django.core.management.base import NoArgsCommand, BaseCommand, CommandError
#from django.contrib.gis.geos import Point
#from django.db.models import F
#from tweets.models import *
#import sys
#import time
#from datetime import datetime
#import pytz
import json
import re
#import tweepy
#import tweepy.streaming
#import linear as classifier
import urllib2
import cPickle as pickle
from nltk.corpus import wordnet


def scrapWiki(wikiurls,english_words,skip):
	'''Harvests keywords from the given wikipedia url'''
	keywords = set()
	for url in wikiurls:
		response = urllib2.urlopen(url)
		data = response.read()
		response.close()
		data = data.split('{"ns":0,"*":"')
		for d in data[:-1][::-1]:
			if "exists" not in d: continue
			k = re.search('.*["][,]',d).group()
			#get rid of '",'
			k = k[:-2]
			#get rid of (EP) (band) etc
			if "(" in k:
				idx = k.index("(")
				k = k[:idx]
			k = k.strip()
			#short keywords are ambiguous ...
			#if len(k) < 7: continue
			if k.lower() in skip: continue
			if len(k.split()) > 1 and k.split()[0].lower() == "the": continue
			if "love" in k: continue
			if wordnet.synsets(k): continue
			if k.lower() in english_words: continue
			keywords.add(unicode(k.lower(),"utf-8"))
	print len(keywords)
	#outfile = open("keywords.txt",'w')
	#outfile.write(str(list(keywords)))
	#outfile.close()
	actors = open("actors.pickled",'r')
	actorslist = pickle.load(actors)
	actors.close()
	actors = actorslist + list(keywords)
	actors = list(set(actors))
	actors.sort()
	pickle.dump( actors, open( "actors.pickled", "wb" ) )
	print len(keywords)
	return keywords


class Command(NoArgsCommand):
	help = 'Connect to the twitter stream'
	can_import_settings = True

	def handle_noargs(self, **options):
		#harvest(self.stdout)
		pass
		
if __name__ == "__main__":
	skip = ["emo","emi","andy","lmfao","up!","rca","ska","nme","in love","chocolat","x2"
		,"inna","luv","no id","give up","oh no", "i'm so excited","in time", "2.0","mgm",
		"the hospital","samantha","walmart","3.0","about time","the family","eddie","the greatest"
		,"good news","carrie","better late than never","anti-","the front","so big", "the group",
		"good music", "making it", "so fine", "some girls","love affair","good news","3.0","junior year"
		,"walmart", "every sunday","deal with it","baby daddy","in luv","enough said","give up","girl code"
		,"making it", "yours truly","the test","angie","soap opera"]



	word_file = open("wordsEn.txt",'r')
	english_words = set(word.strip().lower() for word in word_file)
	word_file.close()
	#urls = ["http://en.wikipedia.org/w/api.php?format=json&action=parse&page=List_of_2013_albums",
	#		"http://en.wikipedia.org/w/api.php?format=json&action=parse&page=2013_in_film",
	#		"http://en.wikipedia.org/w/api.php?format=json&action=parse&page=2013_in_American_television",
	#		"http://en.wikipedia.org/w/api.php?format=json&action=parse&page=List_of_stars_on_the_Hollywood_Walk_of_Fame"]
	urls = ["http://en.wikipedia.org/w/api.php?format=json&action=parse&page=List_of_stars_on_the_Hollywood_Walk_of_Fame"]

	scrapWiki(urls,english_words,skip)
	
	
	
	
	