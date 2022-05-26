import json
from src.entities.trip import Trip
from src.entities.requesttriplist import RequestTripList


def parse_trips_into_requesttriplist(json_trips):
	request_trip_list = RequestTripList()
	for j_trip in json_trips:
		try:
			request_trip_list.append(Trip(j_trip["request_time"], j_trip["start_time"], j_trip["start_station_id"],
			                              j_trip["end_station_id"], j_trip["car_id"]))
		except KeyError:
			request_trip_list.append(Trip(j_trip["request_time"], j_trip["start_time"], j_trip["start_station_id"],
			                              j_trip["end_station_id"]))
	return request_trip_list


def get_trip_requests(file_name):
	f = open(f'../../data/trips_requests/{file_name}.json')
	return parse_trips_into_requesttriplist(json.load(f)["trips"])
