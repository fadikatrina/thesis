from src.helpers.station_metrics import get_stations_metrics


class Trip:

	def __init__(self, request_time, start_time, start_station_id, end_station_id, car_id=-1):
		self.request_time = request_time
		self.start_time = start_time
		self.start_station_id = start_station_id
		self.end_station_id = end_station_id
		self.car_id = car_id
		duration, self.distance, self.charge_cost = get_stations_metrics(start_station_id, end_station_id)
		self.end_time = start_time + duration

	def has_a_car(self):
		if self.car_id == -1:
			return False
		else:
			return True

	def __str__(self):
		return f"Trip REQUEST_TIME {self.request_time} START_TIME {self.start_time} START_STATION " \
		       f"{self.start_station_id} END_STATION {self.end_station_id} CAR_ID {self.car_id}"
