import json

f = open('../../data/stations_metrics_based_on_original_paper.json')
station_datas = json.load(f)


def get_stations_metrics(start_station_id, end_station_id):
	for station_data in station_datas:
		if start_station_id == station_data["start_id"]:
			for dest_data in station_data["dest"]:
				if end_station_id == dest_data["finish_id"]:
					return dest_data["duration"], dest_data["distance"], dest_data["charge_cost"]
	raise ValueError(f"Can not find metrics for start {start_station_id} and end {end_station_id}")
