import json
from pathlib import Path
import time
from collections import OrderedDict
import logging


def restructure_realtime():
	filenames = ''
	with open(f'./scrape_dump/realtime/timestamps.txt') as file:
		for line in file:
			filenames = line.rstrip()

	filenames = filenames.split(",")
	filenames = filenames[:-1]
	for i in range(15):
		res_best_guess = []
		res_pessimistic = []
		for filename in filenames:
			try:
				f = open(f"./scrape_dump/realtime/{i}_{filename}.json")
				f = json.load(f)

				res_best_guess.append({
					"rows": f["rows"],
					"departure_time": filename,
					"destinations": f["destinations"],
					"time_sent_to_google": f["time_sent_to_google"]
				})
			except FileNotFoundError:
				pass

			f = open(f"./scrape_dump/realtime/{i}_{filename}_pessimistic.json")
			f = json.load(f)

			res_pessimistic.append({
				"rows": f["rows"],
				"departure_time": filename,
				"destinations": f["destinations"]
			})

		with open(f'./scrape_dump/realtime_grouped/{i}_best_guess.json', 'w') as fp:
			json.dump(res_best_guess, fp)

		with open(f'./scrape_dump/realtime_grouped/{i}_pessimistic.json', 'w') as fp:
			json.dump(res_pessimistic, fp)


def convert_timestamp(unix_timestamp):
	hh_mm = time.strftime('%H:%M', time.localtime(int(unix_timestamp)))
	hh_mm = [int(x) for x in hh_mm.split(":")]
	return (3600*hh_mm[0]) + (60*hh_mm[1])


def calculate_charge_cost(trip):
	usual_duration = trip["duration"]["value"]
	traffic_duration = trip["duration_in_traffic"]["value"]
	stop_time = min(0, traffic_duration-usual_duration)
	distance = trip["distance"]["value"]
	COST_PER_METER = 0.000435
	COST_PER_SECOND_WAITING = 0.0001
	return (COST_PER_METER * distance) + (COST_PER_SECOND_WAITING * stop_time)


def restructure_key_by_time_specific():

	modes = ["best_guess", "pessimistic"]

	for mode in modes:
		for i in range(15):

			f = open(f'./scrape_dump/realtime_grouped/{i}_{mode}.json')
			f = json.load(f)
			res = {}
			timestamps = []

			for observation in f:
				try:
					timestamp = convert_timestamp(observation["departure_time"])
					timestamps.append(timestamp)
					res[timestamp] = []
					for trip in observation["rows"][0]["elements"]:
						trip["charge_cost"] = calculate_charge_cost(trip)
						res[timestamp].append(trip)
				except (IndexError, KeyError) as e:
					logging.info(f"{mode} {i} {observation} {e}")

			orders = sorted(res.keys(), key=lambda v: v, reverse=False)
			ordered = OrderedDict()
			for order in orders:
				ordered[order] = res[order]

			with open(f'../../input/locations/bristol_google_time_specific/{i}_{mode}.json', 'w') as fp:
				json.dump(ordered, fp)


def restructure_average_time():

	modes = ["best_guess", "pessimistic"]

	for mode in modes:
		res = []
		for start_id in range(15):
			f = open(f'./scrape_dump/realtime_grouped/{start_id}_{mode}.json')
			f = json.load(f)
			station_json = {
				"start_id": start_id,
				"dest": []
			}
			correction = 0
			for finish_id in range(14):
				if start_id == finish_id:
					correction = 1
				current = f[0]["rows"][0]["elements"][finish_id]
				station_json["dest"].append({
					"finish_id": finish_id + correction,
					"duration": current["duration"]["value"],
					"distance": current["distance"]["value"],
					"charge_cost": 0.000435 * current["distance"]["value"]
				})
			res.append(station_json)

		with open(f'../../input/locations/google_average_{mode}.json', 'w') as fp:
			json.dump(res, fp)


if __name__ == "__main__":
	Path("./scrape_dump/realtime_grouped/").mkdir(parents=True, exist_ok=True)
	Path("../../input/locations/bristol_google_time_specific/").mkdir(parents=True, exist_ok=True)
	logging.basicConfig(filename="./logs/restructure.log", level=logging.DEBUG)
	restructure_realtime()
	restructure_key_by_time_specific()
	# restructure_average_time()
