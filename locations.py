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
	pass
	#locs = Location_Conn()
	#locs.add("Chicago", [-87.96,41.644,-87.40,42.04])
	#locs.add("San Francisco", [-122.75,36.8,-121.75,37.8])
	#locs.add("New York City", [-74,40,-73,41])
	#LA
	#locs.add("Los Angeles", [-118.6682,33.7037,-118.1553,34.3373])
		
	