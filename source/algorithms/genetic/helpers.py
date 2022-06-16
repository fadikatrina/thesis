import copy
from source.helpers.car_finder import CarIDError
from source.helpers.logger import algo_genetic as l
from source.helpers.logger import sim_copy_logger


simulation_cache = {}


def reset_simulation_cache():
	global simulation_cache
	simulation_cache = {}


def filter_using_map(trip_list):
	global simulation_cache
	for trip in trip_list:
		if trip.car_id in simulation_cache.setdefault(trip.id_, []):
			trip_list.remove(trip)
			trip.car_id = -1
			trip_list.append(trip)
	return trip_list


def filter_using_simulation(trip_list, sim):
	global simulation_cache
	sim2 = copy.deepcopy(sim)
	sim2.set_logger(sim_copy_logger)
	trip_list2 = copy.deepcopy(trip_list)
	sim2.set_new_triplist(trip_list2)
	try:
		while not sim2.simulation_END:
			sim2.advance_simulation()
	except CarIDError as e:
		l.debug(f"Removing car trip assignment, CarIDError {e.trip}")
		trip_list.remove(e.trip)
		simulation_cache.setdefault(e.trip.id_, []).append(e.trip.car_id)
		e.trip.car_id = -1
		trip_list.append(e.trip)
		return filter_using_simulation(trip_list, sim)
	return trip_list, simulation_cache


def filter_illegal_assignments(trip_list, sim):
	trip_list = filter_using_map(trip_list)
	trip_list, updated_map = filter_using_simulation(trip_list, sim)
	return trip_list


def assign_genotype_to_triplist(sim, genotype):
	for i in range(len(sim.announced_trip_list)):
		sim.announced_trip_list[i].car_id = genotype[i]
	return sim.announced_trip_list
