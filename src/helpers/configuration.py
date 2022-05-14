import json

f = open('../config.json')
config_data = json.load(f)


def get_config_value(key):
	return config_data[key]
