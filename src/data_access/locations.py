import json


def get_mod_location_data():
	f = open('../../data/bristol_mod_locations.json')
	return json.load(f)
