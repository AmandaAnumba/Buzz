from bs4 import BeautifulSoup
import requests

web = ["http://www.ranker.com/list/best-punk-rock-bands-and-artists/reference",
"http://www.ranker.com/list/best-punk-rock-bands-and-artists/reference?page=2"]

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

# f = open('rock.txt','w')

for i in artists:
	f.write("%s\n" % i.encode('utf8'))

f.close()