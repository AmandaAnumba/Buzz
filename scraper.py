from bs4 import BeautifulSoup
import requests

web = [
"http://www.ranker.com/list/techstep-bands-and-artists/reference",
"http://www.ranker.com/list/dub-bands-and-musicians/reference",
"http://www.ranker.com/list/dub-bands-and-musicians/reference?page=2",
"http://www.ranker.com/list/dub-bands-and-musicians/reference?page=3",
"http://www.ranker.com/list/dub-bands-and-musicians/reference?page=4",
"http://www.ranker.com/list/trance-music-bands-and-musicians/reference",
"http://www.ranker.com/list/trance-music-bands-and-musicians/reference?page=2",
"http://www.ranker.com/list/trance-music-bands-and-musicians/reference?page=3",
"http://www.ranker.com/list/trance-music-bands-and-musicians/reference?page=4",
"http://www.ranker.com/list/tech-trance-bands-and-artists/reference",
"http://www.ranker.com/list/uk-garage-bands-and-musicians/reference",
"http://www.ranker.com/list/uk-garage-bands-and-musicians/reference?page=2",
"http://www.ranker.com/list/uplifting-trance-bands-and-artists/reference",
"http://www.ranker.com/list/dance-music-bands-and-musicians/reference",
"http://www.ranker.com/list/dance-music-bands-and-musicians/reference?page=2",
"http://www.ranker.com/list/dance-music-bands-and-musicians/reference?page=3",
"http://www.ranker.com/list/dance-music-bands-and-musicians/reference?page=4",
"http://www.ranker.com/list/dance-music-bands-and-musicians/reference?page=5",
"http://www.ranker.com/list/dark-electro-bands-and-artists/reference",
"http://www.ranker.com/list/best-dubstep-bands-and-musicians/reference",
"http://www.ranker.com/list/best-dubstep-bands-and-musicians/reference?page=2",
"http://www.ranker.com/list/techno-bands-and-musicians/reference",
"http://www.ranker.com/list/techno-bands-and-musicians/reference?page=2",
"http://www.ranker.com/list/techno-bands-and-musicians/reference?page=3",
"http://www.ranker.com/list/techno-bands-and-musicians/reference?page=4"
]

artists = []

for i in web:
	r = requests.get(i)
	data = r.text
	soup = BeautifulSoup(data)
	# result = soup.find('ol', 'mainList').find_all("li")
	result = soup.find_all("div", "float relative name")
	for i in range(0, len(result)):
		try:
			name = result[i].find('span', 'oNode').text
			artists.append(name)
			# print name
		except:
			pass

f = open('techno.txt','w')

for i in artists:
	f.write("%s\n" % i.encode('utf8'))

f.close()