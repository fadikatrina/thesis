from source.entities.simulation import Simulation
from source.helpers.logger import sim_copy_logger
from source.helpers.logger import algo_short_mode
import copy
from operator import attrgetter
import random


class ShortMode:

	def __init__(self, config, tracker):
		self.CAR_PICKING_MODE = config["pick_strategy"]
		self.STUPID_VERSION = config["dont_take_into_account_future_cars_and_charge"]
		self.l = algo_short_mode
		self.tracker = tracker
		self.trips_already_attempted = []

	def set_logger(self, new_logger):
		self.l = new_logger

	def remove_cars_with_future_trip(self, cars, trip_list, trip_start_time):
		self.l.debug(f"TRIPLIST ({[str(x) for x in trip_list]}) CARS ({[str(x) for x in cars]})")
		res = [x for x in cars if len(trip_list.get_trips_using_car(x.id_, trip_start_time)) == 0]
		self.l.debug(f"WITHOUT FUTURE ROUTES CARS ({[str(x) for x in res]})")
		return res

	def remove_cars_not_enough_charge(self, cars, min_charge_needed):
		self.l.debug(f"MIN_CAHRGE_NEEDED ({min_charge_needed}) CARS ({[str(x) for x in cars]})")
		res = [x for x in cars if x.current_charge_level >= min_charge_needed]
		self.l.debug(f"ENOUGH CHARGE CARS ({[str(x) for x in res]})")
		return res

	def get_car_with_most_charge(self, cars):
		self.l.debug(f"CARS ({[str(x) for x in cars]})")
		res = max(cars, key=attrgetter('current_charge_level'))
		self.l.debug(f"MAX CHARGE CAR ({res})")
		return res

	def get_car_with_least_charge(self, cars):
		self.l.debug(f"CARS ({[str(x) for x in cars]})")
		res = min(cars, key=attrgetter('current_charge_level'))
		self.l.debug(f"MIN CHARGE CAR ({res})")
		return res

	def get_car_based_on_station_charge_level(self, cars, sim, start_id, end_id):
		start_station_total_charge = sum([x.current_charge_level for x in sim.stations[start_id].cars])
		end_station_total_charge = sum([x.current_charge_level for x in sim.stations[end_id].cars])
		if start_station_total_charge > end_station_total_charge:
			return self.get_car_with_most_charge(cars)
		elif end_station_total_charge > start_station_total_charge:
			return self.get_car_with_least_charge(cars)
		else:
			return self.get_car_randomly(cars)

	def get_car_randomly(self, cars):
		return random.choice(cars)

	def choose_car(self, available_cars, sim, start_station_id, end_station_id):
		if len(available_cars) == 1:
			return available_cars[0]
		else:
			if self.CAR_PICKING_MODE == 0:
				return self.get_car_randomly(available_cars)
			elif self.CAR_PICKING_MODE == 1:
				return self.get_car_with_most_charge(available_cars)
			elif self.CAR_PICKING_MODE == 2:
				return self.get_car_with_least_charge(available_cars)
			elif self.CAR_PICKING_MODE == 3:
				return self.get_car_based_on_station_charge_level(available_cars, sim, start_station_id, end_station_id)
			else:
				raise ValueError(
					f"Invalid value of ({self.should_assign_option}) for CAR_PICKING_MODE in Short Algo")

	def assign_cars(self, sim: Simulation, avoid_car_id=None):
		count_assigned = 0
		for trip in sim.announced_trip_list:
			if not trip.has_a_car() and trip.id_ not in self.trips_already_attempted:
				self.trips_already_attempted.append(trip.id_)
				sim2 = copy.deepcopy(sim)
				sim2.LOG = False
				sim2.set_logger(sim_copy_logger)
				sim2.advance_simulation_to_time(trip.start_time)
				station = sim2.stations[trip.start_station_id]
				sim3 = copy.deepcopy(sim2)
				sim3.advance_simulation_to_time(trip.end_time)
				dest_station = sim3.stations[trip.end_station_id]
				no_cars_places_at_end_station = dest_station.max_capacity - (len(dest_station.cars) + len([x.end_station_id == trip.end_station_id for x in sim3.in_progress_trip_list]))
				self.l.debug(f"END STATION ({dest_station}) EXPECTED OPEN SPOTS ({no_cars_places_at_end_station}) TRIP ({trip})")
				if no_cars_places_at_end_station <= 0:
					self.l.info(f"END STATION ({dest_station}) WILL BE FULL SO CANT SCHEDULE TRIP ({trip})")
					continue
				available_cars = station.cars
				if self.STUPID_VERSION:
					available_cars_at_start = copy.deepcopy(sim.stations[trip.start_station_id].cars)
					available_cars_at_start_filtered = []
					available_cars = [x.id_ for x in available_cars]
					for car in available_cars_at_start:
						if car.id_ in available_cars:
							available_cars_at_start_filtered.append(car)
					available_cars = available_cars_at_start_filtered
				available_cars = self.remove_cars_not_enough_charge(available_cars, trip.charge_cost)
				available_cars = self.remove_cars_with_future_trip(available_cars, sim.announced_trip_list, trip.start_time)
				if avoid_car_id:
					available_cars = [x for x in available_cars if x.id_ != avoid_car_id]
				if len(available_cars) == 0:
					self.l.info(f"NO SUITABLE CARS (CHARGE & NO TRIP) START STATION ({station}) TRIP ({trip})")
					continue
				trip.car_id = self.choose_car(available_cars, sim2, trip.start_station_id, trip.end_station_id).id_
				self.l.info(f"ASSIGNED CAR ({trip.car_id}) FOR TRIP ({trip})")
				count_assigned += 1
		self.tracker.no_assignments_short.append(count_assigned)
		return sim.announced_trip_list
