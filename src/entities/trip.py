from src.input_access.station_metrics import get_stations_metrics
import copy

class Trip:

	def __init__(self, id_, request_time, start_time, start_station_id, end_station_id, car_id=-1):
		self.id_ = id_
		self.request_time = request_time
		self.start_time = start_time
		self.start_station_id = start_station_id
		self.end_station_id = end_station_id
		self.car_id = car_id
		self.duration, self.distance, self.charge_cost = get_stations_metrics(start_station_id, end_station_id)
		self.end_time = start_time + self.duration
		assert start_time < self.end_time
		assert request_time < start_time

	def has_a_car(self):
		if self.car_id == -1:
			return False
		else:
			return True

	def __eq__(self, other):
		self_dict = copy.deepcopy(self.__dict__)
		other_dict = copy.deepcopy(other.__dict__)
		del self_dict['car_id']
		del other_dict['car_id']
		return self_dict == other_dict

	def __str__(self):
		return f"Trip ID {self.id_} REQUEST_TIME {self.request_time} START_TIME {self.start_time} END_TIME {self.end_time} START_STATION " \
		       f"{self.start_station_id} END_STATION {self.end_station_id} CAR_ID {self.car_id} CHARGE_COST {self.charge_cost}"
