import json

# open the file with json
json1_file = open('sample.txt')
json1_str = json1_file.read()
music = json.loads(json1_str)


# print the data for each city/country
cities = music.keys()

for city in cities:
	print city
	genres = music[city].keys()

	for genre in genres:
		print genre
		artists = music[city][genre].keys()
		count = len(artists)
		print count

		for artist in artists:
			print artist
			songs = music[city][genre][artist]
			print songs
			print '\n'
	