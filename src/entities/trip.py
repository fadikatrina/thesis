class Trip:

	def __init__(self, request_time, start_time, start_station_id, end_station_id, charge_cost, end_time=None, car_id=None):
		self.request_time = request_time
		self.start_time = start_time
		self.start_station_id = start_station_id
		self.end_station_id = end_station_id
		self.end_time = end_time
		self.car_id = car_id
		self.charge_cost = charge_cost

	def __str__(self):
		return f"Car ID {self.id_} CHARGE {self.current_charge_level}"
