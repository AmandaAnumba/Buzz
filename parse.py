from locations import *
import sys
import time
from datetime import datetime
import pytz
import json
#import tweepy
#import tweepy.streaming
from pymongo import Connection
#import nltk
import re
import string
import cPickle as pickle

class Parser:
	"""Parse tweets from the cache"""
	def __init__(self, *args, **kwargs):
		#self.keywords = list(pickle.load(open("keywords.pickled")))
		self.eng_dict = self.summonDictionary()
		self.conn = Connection()
		self.cache = self.conn.buzz.cache
		self.tweets = self.conn.buzz.tweets
		self.keywords = self.conn.buzz.keywords
		self.loc_conn = Location_Conn()
		artists = open("artists.pickled",'r')
		actors = open("actors.pickled",'r')
		self.popculture = pickle.load(artists) + pickle.load(actors)
		#self.popculture = pickle.load(keywordsfile)
		artists.close()
		actors.close()
		self.conductor()
		#for t in self.tweets.find():
		#	self.parseTweet(t)
	
	def conductor(self):
		while True:
			if self.cache.count() == 0:
				time.sleep(60)
			else:
				#tweets = self.cache.find()
				for tweet in self.cache.find(timeout=False):
					self.parseTweet(tweet)
				#except:
				#	continue
				
	
			
	
	def geolocate(self,longlat):
		return self.loc_conn.hood(longlat)
	
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
			
	def parseTweet(self,tweet):
		text = tweet['text']
		#print text
		popcultlist = self.popCulture(tweet)
		#text = self.removeLeadingPronouns(text)
		##hashtags,text = self.pullHashtags(text)
		#print hashtags
		##usernames,text = self.pullUsernames(text)
		#print usernames
		#text = self.removePunctuation(text)
		##phrases = self.cappedPhrases(text)
		#print phrases
		#text = self.removeDictionaryWords(text)
		#return text.strip()
		city = self.geolocate([tweet['long'],tweet['lat']])
		tweet['city'] = city
		tid = tweet['id_str']
		#update cache
		self.cache.remove({'id_str' : tid})
		if city:
			hashtags = [[1,1]]
			usernames = [[1,1]]
			phrases = [[1,1]]
			if len(popcultlist) > 0:
				self.tweets.insert(tweet)
				self.updateKeywords(popcultlist,hashtags,usernames,phrases,tweet['id_str'],tweet['created_at'],city)
	
	def popCulture(self,tweet):
		popcultlist = []
		text = tweet["text"]
		for k in self.popculture:
			if k in text:
				#print text
				#print k
				#print r"\b" + k + "\b"
				head = re.search(r"\b%s\b" % k,text.lower(),re.UNICODE)
				if head:
					popcultlist.append(k)
					#print "KEYWORD: " + k
					#print				
				#if k in tweet['text'].lower():
				#	popcultlist.append(k)
		
		#print
		return popcultlist
	
	def updateKeywords(self,popcultlist,hashtags,usernames,phrases,t_id,t_created,city,hood=None):
		keylist = [[c,'c'] for c in popcultlist ] #+ [[h,'h'] for h in hashtags] + [[u, 'u'] for u in usernames] + [[p, 'p'] for p in phrases]
		
		for k in keylist:
			existing = self.keywords.find({'city' : city, 'text': k[0], 'type' : k[1]})
			
			#keyword has not yet been encountered, make a new one and insert it
			if existing.count() == 0:
				keyword = {
					'city' : city,
					'type' : k[1],
					'text' : k[0],
					'created_at' : t_created,
					'updated_at' : json.dumps(datetime.now().isoformat()),
					'count' : 1,
					'tweet_ids' : [t_id,]
				}
				self.keywords.insert(keyword)
				
			#keyword already exists, update its entry
			elif existing.count() == 1:
				keyword = existing.next()
				keyword['count'] += 1
				keyword['updated_at'] = json.dumps(datetime.now().isoformat())
				keyword['tweet_ids'].append(t_id)
				self.keywords.save(keyword)
				
			else:
				print "Duplicate keyword entries"
				sys.exit(0)
				
	
	def pullHashtags(self,text):
		htset = set(part for part in text.split() if part.startswith('#'))
		text = filter(lambda w: w not in htset,text.split())
		text = ' '.join(text)
		return list(htset),text.strip()
		
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
		
Parser()		