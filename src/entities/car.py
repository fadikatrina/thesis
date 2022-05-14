from src.helpers.configuration import get_config_value


class Car:

	def __init__(self, id_, current_charge_level=None, max_charge_level=None):
		self.id_ = id_
		if current_charge_level is None:
			current_charge_level = get_config_value("car_initial_charge_level")
		self.current_charge_level = current_charge_level
		if max_charge_level is None:
			max_charge_level = get_config_value("car_max_charge_level")
		self.max_charge_level = max_charge_level

	def __str__(self):
		return f"Car ID {self.id_} CHARGE {self.current_charge_level}"
