from src.data_access.locations import get_mod_location_data
from src.entities.station import Station


class Simulation:

	stations = []
	# seconds
	simulation_clock = 0

	def __init__(self):
		self.seed_cars_stations()
		self.trips = []

	def seed_cars_stations(self):
		id_ = 0
		for ml in get_mod_location_data():
			self.stations.append(Station(id_, ml["site_name"], ml["longitude"], ml["latitude"]))
			id_ += 1

	def __str__(self):
		return f"Simulation STATIONS# {len(self.stations)}"
