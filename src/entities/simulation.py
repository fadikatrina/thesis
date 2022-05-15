from src.data_access.locations import get_mod_location_data
from src.entities.station import Station
from src.entities.triplist import TripList
from src.entities.trip import Trip


class Simulation:

	stations = []
	trips = TripList()

	# seconds
	simulation_clock = 0

	def __init__(self):
		for ml in get_mod_location_data():
			self.stations.append(Station(ml["id"], ml["site_name"], ml["longitude"], ml["latitude"]))

	def __str__(self):
		return f"Simulation STATIONS# {len(self.stations)}"
