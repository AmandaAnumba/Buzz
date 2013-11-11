from locations import *

class App:
	def __init__(self):
		self.location_conn = Location_Conn()
		self.cities = self.location_conn.cities

class City:
	def __init__(self,city,conn):
		self.city = city
		self.keywords = conn.buzz.keywords.find({"type" : "c", "city" : self.city}).sort("count" , -1)		
		
	def keywordTweets(self,keyword):
		t_idlist = keyword['tweet_ids']
		tweets = self.conn.buzz.tweets.find({"id_str" : {"$in" : t_idlist }}).sort("created_at",-1)
		return tweets
		
	