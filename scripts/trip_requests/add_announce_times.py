from os import walk
import json
import random
from pathlib import Path

PATH = "../../input/trips_requests/exp"
ANNOUNCE_UP_TO_SECONDS_BEFORE = 3600


def add_request_time():
	filenames = next(walk(PATH), (None, None, []))[2]

	for filename in filenames:

		if filename == ".DS_Store":
			continue

		f = open(f'{PATH}/{filename}')
		trips = json.load(f)
		trips = trips["trips"]

		for trip in trips:
			trip["request_time"] = max(trip["start_time"] - random.randint(1, ANNOUNCE_UP_TO_SECONDS_BEFORE), 0)

		with open(f'{PATH}/dynamic_request_time/{filename}', 'w') as fp:
			json.dump(trips, fp)


if __name__ == "__main__":
	Path(f'{PATH}/dynamic_request_time/').mkdir(parents=True, exist_ok=True)
	add_request_time()
