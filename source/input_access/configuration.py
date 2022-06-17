import json

config_data = None
car_config_data = None


def load_config_data(general_filename, car_charge_filename):
	global config_data
	f = open(f'./input/general_config/{general_filename}.json')
	config_data = json.load(f)

	f = open(f'./input/car_charge_config/{car_charge_filename}.json')
	global car_config_data
	car_config_data = json.load(f)


def get_config_value(key):
	return config_data[key]


def get_car_charge_config_value(car_id):
	try:
		charge_value = int(car_config_data[str(car_id)])
	except KeyError:
		return None
	return charge_value
