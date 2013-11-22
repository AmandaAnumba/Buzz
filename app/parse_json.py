import json
from settings import cities
from pymongo import *

def pull_tweets():
	conn = Connection()
	tweetRet = conn.buzz.tweets.find({},{"id_str" : 1 , "user_id_str" : 1})
	tdict = {}
	for t in tweetRet:
		#tdict[t["id_str"]] = '<iframe border=0 frameborder=0 height=150 width=350 align = right src="https://twitframe.com/show?url=https://twitter.com/%s/status/%s"></iframe>' % (t["user_id_str"],t["id_str"])
		tdict[t["id_str"]] = t["user_id_str"]
	tfile = open("static/json/tids.json",'w')
	json.dump(tdict,tfile)
	tfile.close()
	return tdict

def outputDict(dictlist,sortfield="score",lim=None,fp=None):
	values = []
	outdict = {"key" : "", "values" : values}
	for t in dictlist:
		values.append({"label" : t["text"],"value" : t[sortfield]})
	outdict["values"] = sorted(outdict["values"], key=lambda k: k["value"])[::-1]
	if lim:
		outdict["values"] = outdict["values"][lim[0]:lim[1]]
	if fp:
		fp = open(fp,'w')
		json.dump(outdict,fp)
		fp.close()
	return outdict

def outputall(city,top_keywords,color,tweets_dict,uid_dict,tweets,overall_keywords):
	'''For comparison chart'''
	values = []
	tweets[city] = {}
	for t in top_keywords[city]:
		tid = tweets_dict[city][t["text"]][0]
		tidlist = tweets_dict[city][t["text"]]

		uid = uid_dict[tid]
		#tweets.append({"id_str" : tid , "user_id_str" : uid})
		tweets[city][t["text"]] = tidlist

		#values.append({"label" : t["text"],"value" : t["score"],"id_str" : tid, "user_id_str" : uid})
		values.append({"label" : t["text"],"value" : t["score"],"tweets" : tidlist, "id_str" : tid, "user_id_str" : uid,"score" : t["combined_score"]})
	values = sorted(values, key=lambda k: k['score'])[::-1]
	tweetIds = []
	values = {"key" : city , "color" : color, "values" : values[:60]}
	topfile = open("static/json/%s_values.json" % city,'w')
	json.dump(values,topfile)
	topfile.close()
	return tweets

def outputtop(city,top_keywords,color,tweets_dict,uid_dict,tweets,overall_keywords):
	values = []
	tweets[city] = {}
	citykeywords = [t["text"] for t in top_keywords[city]]
	cityvalues = {}
	for t in top_keywords[city]:
		if t["text"] in [k[1] for k in overall_keywords]:
			cityvalues[t["text"]] = (t["score"],t["contrib_score"])
	for score,keyword in overall_keywords:
		if keyword not in citykeywords:
			continue
		tidlist = tweets_dict[city][keyword]
		tweets[city][keyword] = tidlist
		values.append({"label" : keyword,"value" : cityvalues[keyword][0],"tweets" : tidlist, "score" : score})
	values = sorted(values, key=lambda k: k['score'])[::-1]
	values = {"key" : city , "color" : color, "values" : values}
	topfile = open("static/json/%s_values.json" % city,'w')
	json.dump(values,topfile)
	topfile.close()
	return tweets

def outputpie(city,top_keywords,fp,lim1,lim2):
	'''for city view donut chart'''
	values = []
	for t in top_keywords[city]:
		values.append({"key" : t["text"],"y" : t["score"]})
	values = sorted(values, key=lambda k: k['y'])[::-1][lim1:lim2]
	piefile = open("static/json/%s_%s_values.json" % (city,fp),'w')
	json.dump(values,piefile)
	piefile.close()

def makePieValues(city):
	vfile = open("static/json/%s_pie_combined.json" % city,'w')
	vfile.write("{\n")
	chartTypes = ["trending","upcoming","verge"]
	for i in range(3):
		cfile = open("static/json/%s_%s_values.json" % (city,chartTypes[i]),'r')
		if i < 2:
			vfile.write('"%s"' % chartTypes[i] + ": " + cfile.read() + ',\n')
		else:
			vfile.write('"%s"' % chartTypes[i] + ": " + cfile.read() + '\n}')
		cfile.close()
	vfile.close()

def makeChartValues(cities):
	vfile = open("static/json/compare_values.json",'w')
	vfile.write("[\n")
	i = 0
	for c in cities:
		i += 1
		cfile = open("static/json/%s_values.json" % c,'r')
		if i != len(cities):
			vfile.write('\t' + cfile.read() + ',\n')
		else:
			vfile.write('\t' + cfile.read() + '\n]')
		cfile.close()
	vfile.close()

def parseTable():
	keywordfile = open("static/json/keywordtable.json",'r')
	outfile = open("static/json/keywordtableout.json",'w')
	outfile.write('[')
	lines = keywordfile.readlines()
	nlines = len(lines)
	i = 0
	for line in lines:
		i += 1
		if i != nlines:
			outfile.write(line + ',\n')
		else:
			outfile.write(line)
	outfile.write(']')
	keywordfile.close()
	outfile.close()


def main():
	pull_tweets()
	keywords_by_city = {}
	for c in cities:
		keywords_by_city[c] = []
	#parseTable()
	keywordfile = open("static/json/keywordtableout.json",'r')
	json_list = json.load(keywordfile,encoding="utf-8")
	keywordfile.close()
	for k in json_list:
		if k["city"] in cities:
			keywords_by_city[k["city"]].append(k)
	city_sums = {}
	tweets_dict = {}
	combined_keywords = {}
	combined_sum = 0.
	for k in keywords_by_city.keys():
		tweets_dict[k] = {}
		city_sums[k] = 0.
		for c in keywords_by_city[k]:
			city_sums[k] += c['count']
			combined_sum += c['count']
			tweets_dict[k][c['text']] = c['tweet_ids']
			if c['text'] in combined_keywords.keys():
				combined_keywords[c['text']] += c['count']
			else:
				combined_keywords[c['text']] = 0.
	top_keywords = {}
	overall_keywords = []
	comb_text = []
	for k in keywords_by_city.keys():
		top = []
		city_sum = city_sums[k]
		for c in keywords_by_city[k]:
			#percentage of tweets
			score = 100 * (c["count"] / city_sum)
			combined_score = 100 * (combined_keywords[c['text']] / combined_sum)
			contrib_score = (c["count"] / (combined_sum / 500.))
			c["score"] = round(score,2)
			c["combined_score"] = round(combined_score,2)
			c["contrib_score"] = contrib_score
			top.append(c)
			if c['text'] in comb_text:
				continue
			else:
				comb_text.append(c["text"])
				overall_keywords.append((c["combined_score"],c["text"]))
		#sort by highest score
		top = sorted(top, key=lambda k: k['combined_score'])[::-1]
		top_keywords[k] = top
	overall_keywords = sorted(overall_keywords)[::-1][:75]

	chart = {}
	colors = ["#FF0000","blue","gold","green","#BF00FF","#04B4AE"][::-1]
	tfile = open("static/json/tids.json",'r')
	uid_dict = json.load(tfile)
	tweets = {}
	for c in cities:
		color = colors.pop()
		tweets = outputtop(c,top_keywords,color,tweets_dict,uid_dict,tweets,overall_keywords)
	makeChartValues(cities)
	#comp_tweets = open("static/json/compare_tweets2.json",'w')
	#json.dump(tweets,comp_tweets)
	#comp_tweets.close()
	tfile.close()

	for city in cities:	
		#trending
		outputpie(city,top_keywords,"trending",0,10)
		#Upcoming
		outputpie(city,top_keywords,"upcoming",10,20)
		#On the Verge
		outputpie(city,top_keywords,"verge",40,50)
		makePieValues(city)

if __name__ == "__main__":
	main()



