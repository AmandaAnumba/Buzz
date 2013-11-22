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
	#westlimit=-122.475734; southlimit=47.417553; eastlimit=-122.091581; northlimit=47.824583
	locs.add("Seattle",[-122.475734,47.417553,-122.091581,47.824583])
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
		
	