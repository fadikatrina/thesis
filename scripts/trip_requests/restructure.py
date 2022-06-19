from os import walk
import json
from pathlib import Path

FOLDER_NAME = "input"


def restructure_txt_from_route_generation_tool():
	filenames = next(walk(f"./{FOLDER_NAME}"), (None, None, []))[2]  # [] if no file

	for filename in filenames:

		if filename == ".DS_Store":
			continue

		res = {"trips" : []}
		with open(f'./{FOLDER_NAME}/{filename}') as f:
			lines = f.readlines()

		for line in lines:
			line = line.rstrip('\n').split(',')
			start_time = line[2].split(":")
			start_time = (int(start_time[0])*3600) + (int(start_time[1])*60)
			if start_time == 0:
				continue
			start_id = int(line[0])
			end_id = int(line[1])
			if start_id == end_id:
				continue
			res["trips"].append({
				"request_time": 0,
				"start_time": start_time,
				"start_station_id": start_id,
				"end_station_id": end_id
			})

		filename = filename.split("-")[1:3]
		filename = '_'.join(filename)

		with open(f'../../input/trips_requests/exp/{filename}.json', 'w') as fp:
			json.dump(res, fp)


if __name__ == "__main__":
	Path("./scrape_dump/realtime_grouped/").mkdir(parents=True, exist_ok=True)
	restructure_txt_from_route_generation_tool()
