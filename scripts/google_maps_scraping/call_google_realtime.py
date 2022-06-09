import requests
import json
import logging
from pathlib import Path
import time


LOCATIONS_FILENAME = 'bristol_min'
MINUTE_WAIT_TIME = 15
TRAFFIC_MODEL_PESSIMISTIC = 'pessimistic'
GOOGLE_CLOUD_API_KEY = None


def scrape_google_maps():

	f = open(f'../../input/locations/{LOCATIONS_FILENAME}.json')
	locations = json.load(f)

	while True:

		current_time = str(int(time.time()))
		with open("./scrape_dump/realtime/timestamps.txt", "a") as myfile:
			myfile.write(current_time)
			myfile.write(",")

		for location1 in locations:
			origin = f"{location1['latitude']},{location1['longitude']}"
			destinations = ""
			for location2 in locations:
				if location1["id"] == location2["id"]:
					continue
				destinations = f"{destinations}{location2['latitude']},{location2['longitude']}|"

			destinations = destinations[:-1]
			request_url = f"https://maps.googleapis.com/maps/api/distancematrix/json?origins={requests.utils.quote(origin)}&destinations={requests.utils.quote(destinations)}"

			logging.debug(f"ORIGIN {origin} DESTINATIONS {destinations}")
			departure_time = str(int(time.time()) + 10)

			request_url = f"{request_url}&key={GOOGLE_CLOUD_API_KEY}"
			request_url = f"{request_url}&departure_time={departure_time}"
			logging.debug(f"REQUEST URL {request_url}")

			response = requests.request("GET", request_url)
			logging.debug(f"{response.status_code}")
			res_json = response.json()
			res_json["destinations"] = destinations
			res_json["departure_time"] = current_time
			logging.debug(f"BEST GUESS {res_json}")

			with open(f'./scrape_dump/realtime/{location1["id"]}_{current_time}.json', 'w') as fp:
				json.dump(res_json, fp)

			request_url = f"{request_url}&traffic_model={TRAFFIC_MODEL_PESSIMISTIC}"
			response = requests.request("GET", request_url)
			logging.debug(f"{response.status_code}")
			res_json = response.json()
			res_json["destinations"] = destinations
			res_json["departure_time"] = current_time
			logging.debug(f"PESSIMISTIC {res_json}")

			with open(f'./scrape_dump/realtime/{location1["id"]}_{current_time}_pessimistic.json', 'w') as fp:
				json.dump(res_json, fp)

		time.sleep(60 * MINUTE_WAIT_TIME)


if __name__ == "__main__":
	Path("./logs").mkdir(parents=True, exist_ok=True)
	Path("./scrape_dump/realtime").mkdir(parents=True, exist_ok=True)
	logging.basicConfig(filename="./logs/call_google_realtime.log", level=logging.DEBUG)
	scrape_google_maps()
