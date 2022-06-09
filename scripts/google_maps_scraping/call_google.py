import requests
import json
import logging
from pathlib import Path


LOCATIONS_FILENAME = 'bristol_min'
INTERVAL_IN_HOURS = 1
NUMBER_OF_DAYS = 1
SEPTEMBER_5TH_2022_MIDNIGHT_EPOCH = 1662332400
MARCH_6TH_2023_MIDNIGHT_EPOCH = 1678060800
TRAFFIC_MODEL = 'best_guess'
GOOGLE_CLOUD_API_KEY = None


def scrape_google_maps():
	return

	f = open(f'../../input/locations/{LOCATIONS_FILENAME}.json')
	locations = json.load(f)

	for location1 in locations:
		origin = f"{location1['latitude']},{location1['longitude']}"
		destinations = ""
		results = []
		for location2 in locations:
			if location1["id"] == location2["id"]:
				continue
			destinations = f"{destinations}{location2['latitude']},{location2['longitude']}|"

		destinations = destinations[:-1]
		request_url = f"https://maps.googleapis.com/maps/api/distancematrix/json?origins={requests.utils.quote(origin)}&destinations={requests.utils.quote(destinations)}"

		logging.debug(f"ORIGIN {origin} DESTINATIONS {destinations}")
		for day in range(NUMBER_OF_DAYS):
			logging.debug(f"DAY {day}")
			for hour_block in range(int(24/INTERVAL_IN_HOURS)):
				logging.debug(f"HOUR BLOCK {hour_block}")
				current_departure_time = MARCH_6TH_2023_MIDNIGHT_EPOCH + (hour_block*INTERVAL_IN_HOURS*3600) + (day*86400)
				logging.debug(f"DEPARTURE TIME {current_departure_time}")
				request_url = f"{request_url}&departure_time={current_departure_time}"
				request_url = f"{request_url}&traffic_model={TRAFFIC_MODEL}"
				request_url = f"{request_url}&key={GOOGLE_CLOUD_API_KEY}"
				logging.debug(f"REQUEST URL {request_url}")

				response = requests.request("GET", request_url)
				logging.debug(f"{response.status_code}")
				res_json = response.json()
				res_json["destinations"] = destinations
				res_json["departure_time"] = current_departure_time
				logging.debug(f"{res_json}")

				results.append(res_json)

		with open(f'./scrape_dump/{location1["id"]}_{TRAFFIC_MODEL}.json', 'w') as fp:
			json.dump(results, fp)


if __name__ == "__main__":
	Path("./logs").mkdir(parents=True, exist_ok=True)
	Path("./scrape_dump").mkdir(parents=True, exist_ok=True)
	logging.basicConfig(filename="./logs/call_google.log", level=logging.DEBUG)
	scrape_google_maps()
