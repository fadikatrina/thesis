# this is the same distance calculation used in the original paper
# except the traffic level thing

from src.entities.simulation import Simulation
import json
import math


def rad2deg(rad):
	return rad * 180.0 / math.pi


def deg2rad(deg):
	return deg * math.pi / 180.0


def calculate_duration(s1, s2):
	lon1 = s1.longitude
	lat1 = s1.latitude
	lon2 = s2.longitude
	lat2 = s2.latitude

	theta = lon1 - lon2

	distance = math.sin(deg2rad(lat1)) * math.sin(deg2rad(lat2)) + math.cos(deg2rad(lat1)) * math.cos(
		deg2rad(lat2)) * math.cos(deg2rad(theta))
	distance = math.acos(distance);
	distance = rad2deg(distance);
	distance = distance * 60 * 1.1515;
	distance = distance * 1.609344;

	trip_duration = (distance / 85) * 60;

	return trip_duration, distance


sim = Simulation()
stations = sim.stations

calc_list = []
i = 0

for station1 in stations:
	calc_list.append({
		"start_id": station1.id_,
		"dest":[]
	})
	for station2 in stations:
		if station1.id_ == station2.id_:
			print("Same station, skip")
		else:
			duration, distance = calculate_duration(station1, station2)
			charge = duration * 0.50
			calc_list[i]["dest"].append({
				"finish_id": station2.id_,
				"duration": duration,
				"distance": distance,
				"charge_cost": charge
			})
	i+=1

with open('../../data/stations_metrics_based_on_original_paper.json', 'w') as fp:
	json.dump(calc_list, fp)
