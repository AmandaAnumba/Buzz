#from locations import *
#import sys
#import time
#from datetime import datetime
#import pytz
#import json
#import tweepy
#import tweepy.streaming
from pymongo import Connection
from collections import Counter
#import nltk
#import re
#import string
#import cPickle as pickle

skip = ["emo","emi","andy","lmfao","up!","rca","ska","nme","in love","chocolat","x2"
	,"inna","luv","no id","give up","oh no", "i'm so excited","in time", "2.0","mgm",
	"the hospital","samantha","walmart","3.0","about time","the family","eddie","the greatest"
	,"good news","carrie","better late than never","anti-","the front","so big", "the group",
	"good music", "making it", "so fine", "some girls"]

keywords = Connection().buzz.keywords
#header = "Cities Chi
entries = keywords.find({"type":'c'})
kwdict = Counter()
kwdict["Chicago"] = Counter()
kwdict["San Francisco"] = Counter()
kwdict["New York City"] = Counter()

for e in entries:
	if e["text"] in skip:
		continue
	kwdict[e["city"]][e["text"]] += e["count"]

chart = [kwdict[k] for k in kwdict.keys()]

comp = open("comp.tab",'w')
comp.write("name	New York	San Francisco	Chicago\n")
toChart = chart[2].most_common(25)
c = float(sum(chart[0].values()))
s = float(sum(chart[1].values()))
n = float(sum(chart[2].values()))
trunc = 5
for i in xrange(20):
	ct = chart[0][toChart[i][0]] / c
	st = chart[1][toChart[i][0]] / s
	nt = chart[2][toChart[i][0]] / n
	comp.write(toChart[i][0] + '\t' + str(nt*100)[:trunc] + '\t' + str(st*100)[:trunc] + '\t' + str(ct*100)[:trunc] + '\n')
comp.close()
