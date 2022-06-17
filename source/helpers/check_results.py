from source.entities.simulation import Simulation
from source.helpers.car_finder import pop_from_list
import json


def check_result(sim: Simulation, filename):
	with open(f'./input/result_check/{filename}.json', 'r') as f:
		rules = json.load(f)
		for rule in rules:
			rule_name = rule["rule_name"]
			if rule_name == "car_in_station":
				pop_from_list(sim.stations[rule["station_id"]].cars, rule["car_id"])
			elif rule_name == "trip_assigned_car":
				assert sim.completed_trip_list.get_trip_by_id(rule["trip_id"]).car_id == rule["car_id"]
			else:
				raise ValueError("Invalid check rule name")

