from src.helpers.configuration import get_config_value
from src.entities.car import Car


def initialise_cars(station_id, max_station_capacity):
	cars = []
	for i in range(max_station_capacity):
		car_id = (station_id * max_station_capacity) + i
		cars.append(Car(car_id))
	return cars


class Station:

	def __init__(self, id_, name, latitude, longitude, cars=None, max_capacity=None):
		self.id_ = id_
		self.name = name
		self.longitude = longitude
		self.latitude = latitude

		if max_capacity is None:
			max_capacity = get_config_value("station_max_capacity")
		self.max_capacity = max_capacity

		if not cars:
			cars = initialise_cars(self.id_, self.max_capacity)
		self.cars = cars

		if len(self.cars) > max_capacity:
			raise ValueError("A station can not have more cars than max_capacity")

	def __str__(self):
		return f"Station ID {self.id_} NAME {self.name} CARS# {len(self.cars)}"
