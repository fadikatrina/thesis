from src.input_access.configuration import get_config_value, get_car_charge_config_value


class Car:

	def __init__(self, id_, current_charge_level=None, max_charge_level=None):
		self.id_ = id_
		if current_charge_level is None:
			if get_car_charge_config_value(id_) is None:
				current_charge_level = get_config_value("car_initial_charge_level")
			else:
				current_charge_level = get_car_charge_config_value(id_)
		self.current_charge_level = current_charge_level
		if max_charge_level is None:
			max_charge_level = get_config_value("car_max_charge_level")
		self.max_charge_level = max_charge_level
		self.last_trip_end_time = 0
		self.last_recharge = 0

	def is_charge_full(self):
		return self.max_charge_level == self.current_charge_level

	def add_charge(self, amount):
		self.current_charge_level = min(self.current_charge_level + amount, 100)
		return self.current_charge_level

	def __str__(self):
		return f"Car ID {self.id_} CHARGE {self.current_charge_level}"
