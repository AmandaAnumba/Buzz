
from pymongo import *
from sys import argv

def getTweets(conn,keyword,city):
	ids = conn.keywords.find({"text" : keyword, "city" : city},{"tweet_ids" : 1})
	if ids.count() == 0:
		return []
	ids = [str(id) for id in  list(ids)[0]["tweet_ids"]]
	tweets = conn.tweets.find({"id_str" : {"$in" : ids }},{"text" : 1})
	for t in tweets:
		print t["text"]
		print
	return tweets

keyword = argv[1]
city = argv[2]
conn = Connection().buzz
getTweets(conn,keyword,city)