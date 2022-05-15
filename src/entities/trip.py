class Trip:

	def __init__(self, request_time, start_time, start_station_id, end_station_id,
	             car_id=-1, end_time=None, charge_cost=None):
		self.request_time = request_time
		self.start_time = start_time
		self.start_station_id = start_station_id
		self.end_station_id = end_station_id
		self.car_id = car_id
		if not charge_cost:
			charge_cost = self.calculate_charge_cost()
		self.charge_cost = charge_cost
		if not end_time:
			end_time = self.calculate_end_time()
		self.end_time = end_time

	def has_a_car(self):
		if self.car_id == -1:
			return False
		else:
			return True

	# todo
	def calculate_end_time(self):
		return 1

	# todo
	def calculate_charge_cost(self):
		return 1

	def __str__(self):
		return f"Trip REQUEST_TIME {self.request_time} START_TIME {self.start_time} START_STATION " \
		       f"{self.start_station_id} END_STATION {self.end_station_id} CAR_ID {self.car_id}"
