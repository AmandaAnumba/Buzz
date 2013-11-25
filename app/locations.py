from pymongo import *

#Chicago#SF#NYC
#LOCATIONS = [-87.96,41.644, -87.40,42.04,-122.75,36.8,-121.75,37.8,-74,40,-73,41]	 
class Location_Conn:
	def __init__(self):
		self.conn = Connection()
		self.locations = self.conn.buzz.locations
		self.coordinates = self.list_coordinates()
		self.cities = [loc["city"] for loc in self.locations.find()]
	
	def add(self,city,coords,hood=None):
		#coords = wlim,slim,elim,nlim
		newLoc = {}
		newLoc['coordinates'] = coords
		newLoc['city'] = city	
		if hood:
			newLoc['hood'] = hood
		self.locations.insert(newLoc)
		
	def list_coordinates(self):
		return sum([c['coordinates'] for c in self.locations.find()],[])
		
	def hood(self,longlat):
		#longlat = [-73.91049924,40.89240194]
		long,lat = longlat[0],longlat[1]	
		locs = self.locations.find()
		for l in locs:
			c = l['coordinates']
			west_east = sorted([c[0],[c]])
			south_north = sorted([c[1],c[3]])
			if west_east[0] <= long <= west_east[1] and south_north[0] <= lat <= south_north[1]:
				return l['city']
			

		
if __name__ == "__main__":
	locs = Location_Conn()
	#westlimit=-71.309903; southlimit=42.22788; eastlimit=-70.891615; northlimit=42.471335
	#locs.add("Boston",[-71.309903,42.22788,-70.891615,42.471335])
	#westlimit=-75.376433; southlimit=39.796346; eastlimit=-74.8253; northlimit=40.182072
	#locs.add("Philadelphia",[-75.376433,39.796346,-74.8253,40.182072])
	#westlimit=-97.969969; southlimit=30.097471; eastlimit=-97.488769; northlimit=30.53579
	#locs.add("Austin",[-97.969969,30.097471,-97.488769,30.53579])
	#westlimit=-122.475734; southlimit=47.417553; eastlimit=-122.091581; northlimit=47.824583
	#locs.add("Seattle",[-122.475734,47.417553,-122.091581,47.824583])
	#westlimit=-80.468075; southlimit=25.709042; eastlimit=-80.077856; northlimit=26.050704
	#locs.add("Miami",[-80.468075,25.709042,-80.077856,26.050704])
	#westlimit=-87.997945; southlimit=41.624833; eastlimit=-87.385342; northlimit=42.119975
	#locs.add("Chicago", [-87.997945,41.624833,-87.385342,42.119975])
	#westlimit=-77.241982; southlimit=38.791645; eastlimit=-76.849655; northlimit=39.151737
	#locs.add("Washington DC",[-77.241982,38.791645,-76.849655,39.151737])
	#locs.add("San Francisco", [-122.75,36.8,-121.75,37.8])
	#locs.add("New York City", [-74,40,-73,41])
	#LA
	#locs.add("Los Angeles", [-118.6682,33.7037,-118.1553,34.3373])
		
	