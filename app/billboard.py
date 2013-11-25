import cPickle as pickle
import urllib2
import sys
import re
from nltk.corpus import wordnet

word_file = open("wordsEn.txt",'r')
english_words = set(word.strip().lower() for word in word_file)
word_file.close()

#false positive keywords are removed
skipfile = open("skip.txt",'r')
skip = []
for line in skipfile:
	toskip = re.search('["].*["]',line)
	if toskip:
		skip.append(toskip.group()[1:-1])
skipfile.close()


artists = []
letter = 97
while True:
	print chr(letter)
	if letter == 123:
		break
	url = "http://www.billboard.com/artists/%s" % chr(letter)
	response = urllib2.urlopen(url)
	data = response.read()
	#data = data.split('<article class="masonry-brick">')
	data = data.split('<span class="field-content"><a href="/artist/')
	#print data[-1]
	#data = data
	for d in data:
		a = re.search('["][>].*[<][/][a][>][<][/]span[>]',d,re.UNICODE)
		if a:
			a = a.group()[2:-11]
			if len(a) < 4: continue
			if "love" in a.lower(): continue
			if wordnet.synsets(a.lower()): continue
			if a.lower() in english_words: continue	
			if a.lower() in skip: continue
			#if a.lower() in ["fucked up", "stan", "shou", "der","no one","the time","the family","real estate","the system","the ones","the field","the reason","take that","the word","fucked up","for real","the jets", "the weekend", "this picture", "red carpet", "the party"]: continue	
			artists.append(unicode(a.lower(),"utf-8"))
	#for a in artists:
	#	print a
	response.close()
	letter += 1
artists = list(set(artists))
artists.sort()
f = open("artists.pickled",'w')
pickle.dump(artists,f)
f.close()
