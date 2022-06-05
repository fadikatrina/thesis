from src.entities.simulation import Simulation
from src.helpers.logger import sim_copy_logger
from src.helpers.logger import algo_short_mode
import copy
from operator import attrgetter


class ShortMode:

	def __init__(self):
		self.l = algo_short_mode

	def set_logger(self, new_logger):
		self.l = new_logger

	def remove_cars_with_future_trip(self, cars, trip_list):
		self.l.debug(f"TRIPLIST ({[str(x) for x in trip_list]}) CARS ({[str(x) for x in cars]})")
		res = [x for x in cars if len(trip_list.get_trips_using_car(x.id_)) == 0]
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

	def assign_cars(self, sim: Simulation, avoid_car_id=None):
		for trip in sim.announced_trip_list:
			if not trip.has_a_car():
				sim2 = copy.deepcopy(sim)
				sim2.LOG = False
				sim2.set_logger(sim_copy_logger)
				sim2.advance_simulation_to_time(trip.start_time)
				station = sim2.stations[trip.start_station_id]
				available_cars = station.cars
				available_cars = self.remove_cars_not_enough_charge(available_cars, trip.charge_cost)
				available_cars = self.remove_cars_with_future_trip(available_cars, sim.announced_trip_list)
				if avoid_car_id:
					available_cars = [x for x in available_cars if x.id_ != avoid_car_id]
				if len(available_cars) == 0:
					self.l.info(f"NO SUITABLE CARS (CHARGE & NO TRIP) START STATION ({station}) TRIP ({trip})")
					continue
				trip.car_id = self.get_car_with_most_charge(available_cars).id_
				self.l.info(f"ASSIGNED CAR ({trip.car_id}) FOR TRIP ({trip})")
		return sim.announced_trip_list

