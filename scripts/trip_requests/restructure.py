from os import walk
import json
from pathlib import Path

INPUT_FOLDER_NAME = "input"


def restructure_txt_from_route_generation_tool(out_folder_name):
	filenames = next(walk(f"./{INPUT_FOLDER_NAME}"), (None, None, []))[2]  # [] if no file

	for filename in filenames:

		if filename == ".DS_Store":
			continue

		res = {"trips" : []}
		with open(f'./{INPUT_FOLDER_NAME}/{filename}') as f:
			lines = f.readlines()

		for line in lines:
			line = line.rstrip('\n').split(',')
			start_time = line[2].split(":")
			start_time = (int(start_time[0])*3600) + (int(start_time[1])*60)
			# start_time = (int(start_time[1])*60)
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

		with open(f'../../input/trips_requests/{out_folder_name}/{filename}.json', 'w') as fp:
			json.dump(res, fp)


if __name__ == "__main__":
	Path("../../input/trips_requests/exp/").mkdir(parents=True, exist_ok=True)
	Path("../../input/trips_requests/compact1hr/").mkdir(parents=True, exist_ok=True)
	restructure_txt_from_route_generation_tool("compact1hr")
