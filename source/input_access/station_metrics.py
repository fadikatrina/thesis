import json

station_datas = None
MODE = None


def load_station_metrics(filename):
	global station_datas
	global MODE
	default_behaviour_filenames = ["bristol_metrics_ogpaper", "google_average_best_guess", "google_average_pessimistic"]
	if filename in default_behaviour_filenames:
		MODE = 1
		f = open(f'./input/locations/{filename}.json')
		station_datas = json.load(f)
	else:
		station_datas = []
		for i in range(15):
			f = open(f'./input/locations/bristol_google_time_specific/{i}_{filename}.json')
			station_datas.append(json.load(f))


def get_stations_metrics(start_station_id, end_station_id, start_time):
	if MODE:
		for station_data in station_datas:
			if start_station_id == station_data["start_id"]:
				for dest_data in station_data["dest"]:
					if end_station_id == dest_data["finish_id"]:
						return dest_data["duration"], dest_data["distance"], dest_data["charge_cost"]
		raise ValueError(f"Can not find metrics for start {start_station_id} and end {end_station_id}")
	else:
		station_data = station_datas[start_station_id]
		correction = 0
		if start_station_id < end_station_id:
			correction = -1
		index = 0
		try:
			index = max(k for k in station_data if int(k) <= start_time)
		except ValueError:
			pass
		station_data = station_data[list(station_data.keys())[index]][end_station_id+correction]
		return station_data["duration_in_traffic"]["value"], station_data["distance"]["value"], station_data["charge_cost"]


if __name__ == "__main__":
	load_station_metrics("best_guess")
	get_stations_metrics(0, 2, 6653)
