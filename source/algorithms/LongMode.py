from source.entities.simulation import Simulation
from source.helpers.logger import sim_copy_logger
from source.helpers.logger import algo_long_mode as l
from source.helpers.logger import algo_short_mode, algo_short_mode_critical
from source.algorithms.ShortMode import ShortMode
import copy


class LongMode:

	short_mode = None

	def __init__(self, config, tracker):
		self.short_mode = ShortMode(config, tracker)
		self.tracker = tracker

	def keep_cars_with_1_future_trip(self, cars, trip_list, trip_start_time):
		avail_cars = []
		trips = []
		for car in cars:
			car_trips = trip_list.get_trips_using_car(car.id_, trip_start_time)
			if len(car_trips) == 1:
				avail_cars.append(car)
				trips.append(car_trips[0])
		return avail_cars, trips

	def remove_cars_not_enough_charge(self, cars, min_charge_needed):
		l.debug(f"MIN_CHARGE_NEEDED ({min_charge_needed}) CARS ({[str(x) for x in cars]})")
		res = [x for x in cars if x.current_charge_level >= min_charge_needed]
		l.debug(f"ENOUGH CHARGE CARS ({[str(x) for x in res]})")
		return res

	def assign_cars(self, sim: Simulation):
		count_assigned = 0
		# the first part is the same as the short mode algorithm, therefore instead of rewriting it, I will reuse it
		self.short_mode.set_logger(algo_short_mode)
		sim.set_new_triplist(self.short_mode.assign_cars(sim))
		for trip in sim.announced_trip_list:
			if not trip.has_a_car():
				l.info(f"SHORT NOT ENOUGH, USING LONG MODE TRIP ({trip})")
				sim2 = copy.deepcopy(sim)
				sim3 = copy.deepcopy(sim)
				sim2.set_logger(sim_copy_logger)
				sim3.set_logger(sim_copy_logger)
				sim2.advance_simulation_to_time(trip.start_time)
				station = sim2.stations[trip.start_station_id]
				available_cars = station.cars
				available_cars = self.remove_cars_not_enough_charge(available_cars, trip.charge_cost)
				# the case of no future trips is already handled by the short mode algorithm
				available_cars, available_cars_trips = self.keep_cars_with_1_future_trip(available_cars, sim.announced_trip_list, trip.start_time)
				if len(available_cars) == 0:
					l.info(f"NO SUITABLE CARS (CHARGE & 1 TRIP) START STATION ({station}) TRIP ({trip})")
					continue
				# now, for each of these cars with future routes, remove the cars trip assignment and try to find another vehicle
				l.debug(f"CARS 1 FUTURE ROUTE ({[str(x) for x in available_cars]})")
				for i in range(len(available_cars)):
					candidate_car = copy.deepcopy(available_cars[i])
					candidate_trip = copy.deepcopy(available_cars_trips[i])
					sim3.announced_trip_list.remove(candidate_trip)
					candidate_trip.car_id = -1
					sim3.announced_trip_list.append(candidate_trip)
					self.short_mode.set_logger(algo_short_mode_critical)
					new_triplist = self.short_mode.assign_cars(sim3, candidate_car.id_)
					new_trip = [x for x in new_triplist if x == candidate_trip]
					if len(new_trip) != 1:
						raise RuntimeError(f"There are two trips that are the same, this implementation does not work")
					candidate_trip_assigned_alt_car = [x for x in new_triplist if x.id_ == candidate_trip.id_][0]
					if candidate_trip_assigned_alt_car.car_id != -1:
						l.info(f"SUBSTITUTE FOUND ASSIGNED NEW CARD ID ({candidate_car.id_}) FOR TRIP ({trip})")
						l.info(f"ORIGINAL CAR ({candidate_trip_assigned_alt_car.car_id}) FROM TRIP ({candidate_trip_assigned_alt_car})")
						sim.announced_trip_list.remove(trip)
						trip.car_id = candidate_car.id_
						sim.announced_trip_list.append(trip)
						sim.announced_trip_list.remove(candidate_trip)
						candidate_trip.car_id = candidate_trip_assigned_alt_car.car_id
						sim.announced_trip_list.append(candidate_trip)
						count_assigned += 1
						break
					else:
						l.info(f"SHORTMODE NO ALTERNATIVE CAR THAN ({candidate_car.id_}) TRIP ({candidate_trip_assigned_alt_car})")
		self.tracker.no_assignments_long.append(count_assigned)
		return sim.announced_trip_list
