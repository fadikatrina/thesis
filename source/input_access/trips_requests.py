import json
from source.entities.trip import Trip
from source.entities.triplists.requesttriplist import RequestTripList


def parse_trips_into_requesttriplist(json_trips):
	request_trip_list = RequestTripList()
	count = 0
	for j_trip in json_trips:
		try:
			request_trip_list.append(Trip(count, j_trip["request_time"], j_trip["start_time"], j_trip["start_station_id"],
			                              j_trip["end_station_id"], j_trip["car_id"]))
		except KeyError as e:
			request_trip_list.append(Trip(count, j_trip["request_time"], j_trip["start_time"], j_trip["start_station_id"],
			                              j_trip["end_station_id"]))
		count += 1
	return request_trip_list


def get_trip_requests(file_name):
	f = open(f'./input/trips_requests/{file_name}.json')
	return parse_trips_into_requesttriplist(json.load(f)["trips"])
