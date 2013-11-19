import cPickle as pickle
import urllib2
import sys
import re

actors = []
f = open("actors.txt",'r')
lines = [l.strip() for l in f.readlines()]
f.close()
for l in lines:
	a = l.split('\t')[1]
	actors.append(unicode(a.lower(),"utf-8"))
actors = list(set(actors))
actors.sort()
f = open("actors.pickled",'w')
pickle.dump(actors,f)
f.close()
