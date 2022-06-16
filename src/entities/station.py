from src.input_access.configuration import get_config_value
from src.entities.car import Car
from src.helpers.car_finder import pop_from_list

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
			cars = initialise_cars(self.id_, get_config_value("station_initial_number_of_cars"))
		self.cars = cars

		if len(self.cars) > max_capacity:
			raise ValueError("A station can not have more cars than max_capacity")

	def remove_car(self, car_id, trip):
		self.cars, found_car = pop_from_list(self.cars, car_id, trip=trip)
		return found_car

	def add_car(self, car):
		if not len(self.cars) < self.max_capacity:
			raise RuntimeError(f"Can not add CAR ({car}) in STATION ({self}) because max capacity reached")
		self.cars.append(car)

	def is_full(self):
		return len(self.cars) == self.max_capacity

	def __str__(self):
		return f"Station ID {self.id_} NAME {self.name} CARS# {len(self.cars)}"
