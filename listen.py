#from django.core.management.base import NoArgsCommand, BaseCommand, CommandError
#from django.contrib.gis.geos import Point
#from django.db.models import F
from locations import *
import sys
import time
from datetime import datetime
import pytz
import json
import tweepy
import tweepy.streaming
#import linear as classifier
from pymongo import Connection
import cPickle as pickle
from Oauth import main as GetAPI
import nltk
import re
import string





class Listener(tweepy.streaming.StreamListener): 
	"""Listen to the twitter stream"""
	def __init__(self, *args, **kwargs):
		super(Listener, self).__init__(*args, **kwargs)
		#self.keywords = list(pickle.load(open("keywords.pickled")))
		#self.eng_dict = self.summonDictionary()
		self.conn = Connection()
		self.cache = self.conn.buzz.cache
		#self.tweets = conn.buzz.tweets
	
	def summonDictionary(self):
		eng_dict_file = open("eng_dict",'r')
		eng_dict = [w.replace('\n','').strip() for w in eng_dict_file.readlines()]
		eng_dict.append('i')
		eng_dict_file.close()
		return eng_dict
	
	def parseTweet1(self,text):
		hashtags,text = self.pullHashtags(text)
		usernames,text = self.pullUsernames(text)
		text = self.removePunctuation(text)
		print text		
		tree = nltk.ne_chunk( nltk.pos_tag( nltk.word_tokenize(text)))
		entities = [i for i in tree if isinstance(i,nltk.tree.Tree)]
		for e in entities:
			print e
			
	def parseTweet(self,text):
		text = self.removeLeadingPronouns(text)
		hashtags,text = self.pullHashtags(text)
		usernames,text = self.pullUsernames(text)
		stext = self.removePunctuation(text)
		#print self.cappedPhrases(text)
		text = self.removeDictionaryWords(text)
		return text.strip()
	
	def pullHashtags(self,text):
		htset = set(part for part in text.split() if part.startswith('#'))
		text = filter(lambda w: w not in htset,text.split())
		text = ' '.join(text)
		return htset,text.strip()
		
	def pullUsernames(self,text):
		return re.findall("@(?i)[a-z0-9_]+",text),re.sub("@(?i)[a-z0-9_]+","",text).strip()
		
	def cappedPhrases(self,text):
		capped = []
		#return re.findall('([A-Z0-9"]+(?=\s[A-Z"])(?:\s[A-Z0-9"]+)+)',text)
		#phrases = re.findall("([A-Z][']*[\w-]*(?:\s+[A-Z][']*[\w-]*)+)",text)
		#endings like 'er in we're
		phrases = re.findall("([a-z]{0,1}[A-Z][']*[s]*[\w-]*(?:\s+[a-z]{0,1}[A-Z][']*[s]*[\w-]*)+)",text,re.UNICODE)
		#for p in phrases:
		#	startidx = text.index(p)
		return phrases

	def removePunctuation(self,text):
		return re.sub("[.!,;:?]", '', text).strip()

	def removeLeadingPronouns(self,text):
		return re.sub("(I'm)|(I[ ])|^(I[ ]am)|^(Can[']t)|(You)|^(He)|^(She)|^(They)|^(Hi)|^(Hey)|^(Sup)|^(Hello)|^(Omg)|^(Lol)|^(Omfg)","",text,re.UNICODE).strip()

	def removeDictionaryWords(self,text):
		noDictWords = []
		for t in text.split():
			if t.strip() in self.eng_dict:
				continue
			noDictWords.append(t)
		return ' '.join(noDictWords).strip()

	def extractMusicTerm(self,text):
		pass
		
	def on_status(self, status):
		"""Categorize and save tweets with coords in a state and community."""
		if hasattr(status, 'lang') and status.lang != 'en':
			return
		if not status.coordinates:
			return
		tweet = {
			'id_str' : status.id_str,
			'created_at' : status.created_at,
			'lang' : status.lang,
			'text' : status.text,
			'entities' : json.dumps(status.entities),
			'long' :  status.coordinates['coordinates'][0],
			'lat' :  status.coordinates['coordinates'][1],
			'user_id_str' : status.user.id_str,
			'user_name' : status.user.name,
			'user_screen_name' : status.user.screen_name,
			'user_profile_image_url' : status.user.profile_image_url
		}
		self.cache.insert(tweet)

	def on_error(self, code):
		'''Called when a non-200 status code is returned.'''
		raise Exception('Error (%s)' % self.convertStatusCode(code))
	
	def on_timeout(self):
		'''Called when the stream comection times out.'''
		return True

	def convertStatusCode(self, code):
		'''Convert an HTTP status code to message.'''
		if code == 200:
			return 'OK'
		if code == 304:
			return 'Not Modified'
		if code == 400:
			return 'Bad Request'
		if code == 401:
			return 'Unauthorized: Authentication credentials are missing or incorrect.'
		if code == 403:
			return 'Forbidden: The request was understood but refused.'
		if code == 404:
			return 'Not Found: The URI requested is invalid or the resource requested does not exist.'
		if code == 406:
			return 'Not Acceptable: An invalid format was specified in the request.'
		if code == 420:
			return 'You are being rate limited.'
		if code == 500:
			return 'Internal Server Error: Something is broken on Twitter.'
		if code == 502:
			return 'Bad Gateway: Twitter is down or being upgraded.'
		if code == 503:
			return 'Service Unavailable: The Twitter servers are up, but overloaded with requests. Try again later.'
	
		return 'Unknown HTTP status code.'


def listen(stdout):
	#from django.conf import settings
	#conn = Connection()
	#keywords = pickle.load(open("keywords.pickled"))
	#keywords = list(keywords)
	#encoded_track = [unicode(s).encode('ascii') for s in keywords]
	#r = Country.objects.get(name__iexact='United States')	 
	#locations = r.geom.extent
	#locations = [-87.96,41.644, -87.40,42.04,-122.75,36.8,-121.75,37.8,-74,40,-73,41]	
	#Chicago#SF#NYC
	#LOCATIONS = [-87.96,41.644,-87.40,42.04,-122.75,36.8,-121.75,37.8,-74,40,-73,41]	
	locs = Location_Conn()
	
	
	
	
	
	
	
	 
	#stdout.write('Searching %s with locations %s\n' % (r.name, locations))
	consumer_key = 'qZnzpvBV2uwKiF2e4kR5mg'
	consumer_secret = 'E7ts8X242CfRKWBYMdTdXfwa3qyIHcEf2B76NUbQs'
	access_key = '1244598638-biVu1Hk4fiPMUTHO9HvYb09rXq7saMtNaevIt7S'
	access_secret = '75F3W2zKO0MsET6makez1sJVJKh9LpcgRefNQXLZWDg8M'		
	stream = None	
	try:
		#auth = tweepy.OAuthHmvandler(
		#	consumer_key, consumer_secret)
		#auth.set_access_token(
		#	access_key, access_secret)
		api,auth = GetAPI()
		while True:	   
			stream = tweepy.streaming.Stream(
				auth, Listener(), timeout=None, secure=True)

			# Connect to stream
			stdout.write('Initializing connection...\n')		  
			stream.filter(locations=locs.coordinates, async=True)
			connection_dt = datetime.now()
			
			# Reset connection
			while((datetime.now() - connection_dt).seconds \
				< 900):#settings.TWITTER_RESET_SECS):
				time.sleep(60)
				
			# Disconnect
			stdout.write('Disconnecting...\n')
			stream.disconnect()	 
			stream = None  
	except NameError:
		raise CommandError('Possible missing twitter account configurations.')
	except KeyboardInterrupt:
		stdout.write('Keyboard interrupt!\n')
		pass
	except Exception:
		raise
	finally:
		if stream and stream.running:
			stream.disconnect()
	

'''class Command(NoArgsCommand):
	def __init__(self, *args, **kwargs):
		super(Command, self).__init__(*args, **kwargs)
		help = 'Connect to the twitter stream'
		can_import_settings = True

	def handle_noargs(self, **options):
		stdout.write('command...\n')
		listen(self.stdout)'''
		
listen(sys.stdout)