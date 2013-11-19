
from pymongo import *
from sys import argv
from collections import Counter

def keywordFreq(conn):
	outfile = open("out.csv",'w')
	cities = [c['city'] for c in conn.buzz.locations.find()]
	kwdata = {}
	counts = {}
	keywords = {}
	for c in cities:
		ret = conn.buzz.keywords.find({"type" : "c", "city" : c}).sort("count",-1)
		ret = [(r['count'],r['text']) for r in ret]
		count = sum([r[0] for r in ret])
		counts[c] = count
		ret = [((r[0] * 1000 / float(count)),r[1]) for r in ret]
		ret.sort()
		for r in ret:
			if r[1] in keywords.keys():
				keywords[r[1]] = keywords[r[1]] + r[0]
			else:
				keywords[r[1]] = r[0]
	ret = []
	for k in keywords.keys():
		ret.append((keywords[k],k))
	ret.sort()
	for r in ret:
		print r
	#print counts
	#print kwdata
	outfile.close()

def getTweets(conn,keyword):
	ids = conn.keywords.find({"text" : keyword},{"tweet_ids" : 1})
	if ids.count() == 0:
		return []
	ids = [str(id) for id in  list(ids)[0]["tweet_ids"]]
	tweets = conn.tweets.find({"id_str" : {"$in" : ids }},{"text" : 1})
	for t in tweets:
		print t["text"]
		print
	return tweets

keyword = argv[1]
conn = Connection().buzz
getTweets(conn,keyword)
#keywordFreq(conn)