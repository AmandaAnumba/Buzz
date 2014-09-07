import json
from pymongo import *
import urllib, urllib2
import cPickle as pickle
import pprint
import operator

a = [line.strip() for line in open('country.txt')]
b = [line.strip() for line in open('electronic.txt')]
c = [line.strip() for line in open('hiphop.txt')]
d = [line.strip() for line in open('indie.txt')]
e = [line.strip() for line in open('jazz.txt')]
f = [line.strip() for line in open('metal.txt')]
g = [line.strip() for line in open('pop.txt')]
h = [line.strip() for line in open('reggae.txt')]
i = [line.strip() for line in open('rnb.txt')]
j = [line.strip() for line in open('rock.txt')]


def parseAll():
	"""for taking all tweets that have been parsed and
	placing them in allTweets to be parsed for relevant
	info"""

	conn = Connection()
	tweets = conn.buzz.tweets
	tweets2 = conn.buzz.tweets2
	allTweets = conn.buzz.allTweets
	collected = []
	allT = []

	for t in allTweets.find(timeout=False):
		allT.append(t['id'])

	with open('app/static/json/music/all_tweets.json', 'w') as f:
		for tweet in tweets2.find(timeout=False):
			location = tweet['city']
			tid = tweet['id_str']

			if location is None:
				print 'location is none', '\n'
				tweets.insert(tweet)
				tweets2.remove({'id_str' : tid})

			else:
				loc = location.split(', ')
				if len(loc) == 3:
					city = loc[0]
					state = loc[1]
					country = loc[2]

				if len(loc) == 2:
					city = ""
					state = loc[0]
					country = loc[1]
								
				song = tweet['song']
				genre = tweet['genre']
				artist = tweet['artist']
				latlong = [tweet['lat'],tweet['long']]
				text = tweet['text']

				if tid not in collected and tid not in allT:
					if genre:
						collected.append(tid)

						data = {
							'id' : tid,
							'genre' : genre,
							'artist' : artist,
							'song' : song,
							'city' : city,
							'state' : state,
							'country' : country,
							'coordinates' : latlong,
							'text' : text
						}

						allTweets.insert(data)
						print 'inserted ', '\n'
					
					else:
						if not genre:
							tweets.insert(tweet)
							tweets2.remove({'id_str' : tid})
				
				else:
					if tid in collected:
						print 'deleting ', '\n'
						tweets2.remove({'id_str' : tid})
					if tid in allT:
						print 'deleting ', '\n'
						tweets2.remove({'id_str' : tid})

		print "finished parsing"
		f.write('[')

		for x in allTweets.find(timeout=False):
			data2 = {
				'id' : x['id'],
				'genre' : x['genre'],
				'artist' : x['artist'],
				'song' : x['song'],
				'city' : x['city'],
				'state' : x['state'],
				'country' : x['country'],
				'coordinates' : x['coordinates'],
				'text' : x['text']
			}
			json.dump(data2, f)
			f.write(',\n')

		print "finished json"
		f.close()


def getGenre(artist):
	if artist in a:
		return "country"
	if artist in b:
		return "electronic"
	if artist in c:
		return "hiphop"
	if artist in d:
		return "indie"
	if artist in e:
		return "jazz"
	if artist in f:
		return "metal" 
	if artist in g:
		return "pop"
	if artist in h:
		return "reggae"
	if artist in i:
		return "R&B"
	if artist in j:
		return "rock"
	else:
		return "unknown"


def getImage(artist):
	try:
		key = 'CoG4VJ1i4Pm/jp2P8+CwQUlB9bsB1dXWtuuuOpHWqb0'
		query = urllib.quote(artist) 
		user_agent = 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; FDM; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 1.1.4322)'
		credentials = (':%s' % key).encode('base64')[:-1]
		auth = 'Basic %s' % credentials
		url = 'https://api.datamarket.azure.com/Data.ashx/Bing/Search/Image?Query=%27'+query+'%27&$top=5&$format=json'
		request = urllib2.Request(url)
		request.add_header('Authorization', auth)
		request.add_header('User-Agent', user_agent)
		request_opener = urllib2.build_opener()
		response = request_opener.open(request) 
		response_data = response.read()
		json_result = json.loads(response_data)
		result_list = json_result['d']['results']

		image = result_list[0]['MediaUrl']
		return image
	except:
		return ""


def edit():
	""" for editing each of the parsed tweets to make sure the artist
	song and genres are there"""
	
	f = open('app/static/json/music/all_tweets.json', 'r')
	clean = open('app/static/json/music/allTweets.json', 'r')
	json_list = json.load(f,encoding="utf-8")
	clean_list = json.load(clean,encoding="utf-8")
	f.close()
	clean.close()
	
	ids = []
	for i in clean_list:
		ids.append(i['id'])
	print "done appending", '\n'

	with open('app/static/json/music/allTweets2.json', 'w') as f2:
		f2.write('[')

		for line in json_list:
			l_id = line['id']

			if l_id not in ids:
				if line['genre'] == 'unknown':
					genre = line['genre']
					artist = line['artist']
					song = line['song']
					text = line['text']

					print text
					print artist
					new_artist = raw_input ( 'Enter artist: ' )

					if new_artist != "":
						line['artist'] = new_artist

					print song
					new_song = raw_input ( 'Enter song: ' )

					if new_song != "":
						line['song'] = new_song

					# print genre
					new = getGenre(new_artist)
					print new

					new_genre = raw_input ( 'Enter genre: ' )

					if new_genre == "":
						line['genre'] = new

					if new_genre != "":
						line['genre'] = new_genre

					pprint.pprint(line)
					json.dump(line, f2)
					f2.write(',\n')
					print '\n\n'

				else:	
					pass
			else:
				pass

		print "finished"
		f2.close()


def allUSdata():
	f = open('app/static/json/music/allTweets.json', 'r')
	json_list = json.load(f,encoding="utf-8")
	f.close()

	with open('app/static/json/music/all_us_data.json', 'w') as f2:
		f2.write('[')

		for line in json_list:
			if line['country'] == 'United States':
				json.dump(line, f2)
				f2.write(',\n')
			else:
				pass
		print "finished"
		f2.write(']')
		f2.close()


def parseGenres():
	clean = open('app/static/json/music/allTweets.json', 'r')
	clean_list = json.load(clean,encoding="utf-8")
	clean.close()
	total = len(clean_list)


	with open('app/static/json/music/genres2.json', 'w') as f2:
		g_country = {
			'genre' : 'country',
			'ids' : [],
			'trending' : {},
			'total' : 0
		}

		electronic = {
			'genre' : 'electronic',
			'ids' : [],
			'trending' : {},
			'total' : 0
		}

		hiphop = {
			'genre' : 'hiphop',
			'ids' : [],
			'trending' : {},
			'total' : 0
		}

		indie = {
			'genre' : 'indie',
			'ids' : [],
			'trending' : {},
			'total' : 0
		}

		jazz = {
			'genre' : 'jazz',
			'ids' : [],
			'trending' : {},
			'total' : 0
		}

		metal = {
			'genre' : 'metal',
			'ids' : [],
			'trending' : {},
			'total' : 0
		}

		pop = {
			'genre' : 'pop',
			'ids' : [],
			'trending' : {},
			'total' : 0
		}

		reggae = {
			'genre' : 'reggae',
			'ids' : [],
			'trending' : {},
			'total' : 0
		}

		rnb = {
			'genre' : 'rnb',
			'ids' : [],
			'trending' : {},
			'total' : 0
		}

		rock = {
			'genre' : 'rock',
			'ids' : [],
			'trending' : {},
			'total' : 0
		}

		unknown = {
			'genre' : 'unknown',
			'ids' : [],
			'trending' : {},
			'total' : 0
		}

		for line in clean_list:
			genre = line['genre']
			id = line['id']
			artist = line['artist']
			song = line['song']
			latlong = line['coordinates']
			city = line['city']
			state = line['state']
			country = line['country']

			if city and state and country:
				loc = city + ', ' + state + ', ' + country

			if not city:
				if state and country:
					loc = state + ', ' + country

			if not state:
				if city and country:
					loc = city + ', ' + country

			if not country:
				if city and state:
					loc = city + ', ' + state

			location = [loc, latlong]
			
			data = {
				'artist': artist, 
				'genre' : genre,
				'count': 1,
				'song': [song, ],
				'places': [location, ]
			}

			if genre == 'country':
				g_country['ids'].append(id)
				g_country['total'] += 1

				if artist not in g_country['trending'].keys():
					g_country['trending'][artist] = data
				else:
					g_country['trending'][artist]['count'] += 1

					if song not in g_country['trending'][artist]['song']:
						g_country['trending'][artist]['song'].append(song)

					g_country['trending'][artist]['places'].append(location)
				

			if genre == 'electronic':
				electronic['ids'].append(id)
				electronic['total'] += 1

				if artist not in electronic['trending'].keys():
					electronic['trending'][artist] = data
				else:
					electronic['trending'][artist]['count'] += 1

					if song not in electronic['trending'][artist]['song']:
						electronic['trending'][artist]['song'].append(song)

					electronic['trending'][artist]['places'].append(location)

			if genre == 'hiphop':
				hiphop['ids'].append(id)
				hiphop['total'] += 1

				if artist not in hiphop['trending'].keys():
					hiphop['trending'][artist] = data
				else:
					hiphop['trending'][artist]['count'] += 1

					if song not in hiphop['trending'][artist]['song']:
						hiphop['trending'][artist]['song'].append(song)

					hiphop['trending'][artist]['places'].append(location)

			if genre == 'indie':
				indie['ids'].append(id)
				indie['total'] += 1

				if artist not in indie['trending'].keys():
					indie['trending'][artist] = data
				else:
					indie['trending'][artist]['count'] += 1

					if song not in indie['trending'][artist]['song']:
						indie['trending'][artist]['song'].append(song)

					indie['trending'][artist]['places'].append(location)

			if genre == 'jazz':
				jazz['ids'].append(id)
				jazz['total'] += 1

				if artist not in jazz['trending'].keys():
					jazz['trending'][artist] = data
				else:
					jazz['trending'][artist]['count'] += 1

					if song not in jazz['trending'][artist]['song']:
						jazz['trending'][artist]['song'].append(song)

					jazz['trending'][artist]['places'].append(location)

			if genre == 'metal':
				metal['ids'].append(id)	
				metal['total'] += 1

				if artist not in metal['trending'].keys():
					metal['trending'][artist] = data
				else:
					metal['trending'][artist]['count'] += 1

					if song not in metal['trending'][artist]['song']:
						metal['trending'][artist]['song'].append(song)

					metal['trending'][artist]['places'].append(location)

			if genre == 'pop':
				pop['ids'].append(id)
				pop['total'] += 1

				if artist not in pop['trending'].keys():
					pop['trending'][artist] = data
				else:
					pop['trending'][artist]['count'] += 1

					if song not in pop['trending'][artist]['song']:
						pop['trending'][artist]['song'].append(song)

					pop['trending'][artist]['places'].append(location)

			if genre == 'reggae':
				reggae['ids'].append(id)		
				reggae['total'] += 1

				if artist not in reggae['trending'].keys():
					reggae['trending'][artist] = data
				else:
					reggae['trending'][artist]['count'] += 1

					if song not in reggae['trending'][artist]['song']:
						reggae['trending'][artist]['song'].append(song)

					reggae['trending'][artist]['places'].append(location)

			if genre == 'rnb':
				rnb['ids'].append(id)
				rnb['total'] += 1

				if artist not in rnb['trending'].keys():
					rnb['trending'][artist] = data
				else:
					rnb['trending'][artist]['count'] += 1

					if song not in rnb['trending'][artist]['song']:
						rnb['trending'][artist]['song'].append(song)
					
					rnb['trending'][artist]['places'].append(location)

			if genre == 'rock':
				rock['ids'].append(id)
				rock['total'] += 1

				if artist not in rock['trending'].keys():
					rock['trending'][artist] = data
				else:
					rock['trending'][artist]['count'] += 1

					if song not in rock['trending'][artist]['song']:
						rock['trending'][artist]['song'].append(song)
					
					rock['trending'][artist]['places'].append(location)

			if genre == 'unknown':
				unknown['ids'].append(id)
				unknown['total'] += 1

				if artist not in unknown['trending'].keys():
					unknown['trending'][artist] = data
				else:
					unknown['trending'][artist]['count'] += 1

					if song not in unknown['trending'][artist]['song']:
						unknown['trending'][artist]['song'].append(song)
					
					unknown['trending'][artist]['places'].append(location)

		print "finished"

		# print rock['trending'].keys()
		f2.write('[\n \t')
		json.dump(g_country, f2)
		f2.write(',\n \t')
		json.dump(electronic, f2)
		f2.write(',\n \t')
		json.dump(hiphop, f2)
		f2.write(',\n \t')
		json.dump(indie, f2)
		f2.write(',\n \t')
		json.dump(jazz, f2)
		f2.write(',\n \t')
		json.dump(metal, f2)
		f2.write(',\n \t')
		json.dump(pop, f2)
		f2.write(',\n \t')
		json.dump(rock, f2)
		f2.write(',\n \t')
		json.dump(reggae, f2)
		f2.write(',\n \t')
		json.dump(rnb, f2)
		f2.write(',\n \t')
		json.dump(unknown, f2)
		f2.write('\n]')
		f2.close()
		parseArtists()
		parseUnknown()


def parseArtists():
	f = open('app/static/json/music/genres2.json', 'r')
	f_list = json.load(f,encoding="utf-8")
	f.close()

	with open('app/static/json/music/artists2.json', 'w') as f2:
		f2.write('[')

		for line in f_list:

			for key in line['trending']:
				# print key
				# print line['trending'][key]
				image = getImage(key)
				# print image

				if line['trending'][key]['count'] > 1 and line['trending'][key]['genre'] != 'unknown':
					data = { 
						'data' : line['trending'][key],
						'image' : image
					}

					json.dump(data, f2)
					f2.write(',\n')

				else:
					pass
		
		f2.write(']')
		f2.close()


def parseUnknown():
	f = open('app/static/json/music/genres.json', 'r')
	f_list = json.load(f,encoding="utf-8")
	f.close()

	with open('app/static/json/music/artist_unknown.json', 'w') as f2:
		f2.write('[')

		for line in f_list:

			for key in line['trending']:
				# print key
				# print line['trending'][key]
				# image = getImage(key)
				# print image

				if line['trending'][key]['genre'] == 'unknown':
					data = { 
						'data' : line['trending'][key]
					}

					json.dump(data, f2)
					f2.write(',\n')

				else:
					pass
		
		f2.write(']')
		f2.close()


def sortArtists():
	f = open('app/static/json/music/artists.json', 'r')
	f_list = json.load(f,encoding="utf-8")
	f.close()

	mylist = sorted(f_list, key=lambda k: (k['data']['genre'], -k['data']['count']))
	# pprint.pprint(mylist)
	genres = ['country', 'electronic', 'indie', 'hiphop', 'jazz', 'metal', 'pop', 'rock', 'reggae', 'rnb']
	
	for g in genres:
		f2 = open('app/static/json/music/artists_%s.json' % g, 'w')
		f2.write('[')
		for i in range(0, len(mylist)):
			if mylist[i]['data']['genre'] == g:
				json.dump(mylist[i], f2)
				f2.write(',\n')
			else:
				pass

		f2.write(']')
		f2.close()

	


if __name__ == "__main__":
	sortArtists()
