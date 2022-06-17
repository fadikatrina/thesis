import json


def get_mod_location_data(filename):
	f = open(f'./input/locations/{filename}.json')
	return json.load(f)
