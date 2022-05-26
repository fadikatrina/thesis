from src.entities.simulation import Simulation
from src.helpers.logger import sim_copy_logger
from src.helpers.logger import algo_first_available as l
import copy


class FirstAvailable:

	def assign_cars(self, sim: Simulation):
		for trip in sim.announced_trip_list:
			if not trip.has_a_car():
				sim2 = copy.deepcopy(sim)
				sim2.LOG = False
				sim2.set_logger(sim_copy_logger)
				sim2.advance_simulation_to_time(trip.start_time)
				station = sim2.stations[trip.start_station_id]
				available_cars = station.cars
				if len(available_cars) == 0:
					l.debug(f"TRIP ({trip}) no cars available START STATION ({station})")
				try:
					trip.car_id = available_cars[0].id_
				except IndexError:
					pass
				l.debug(f"TRIP ({trip}) assigned CAR ({trip.car_id}) from start STATION ({station})")
		return sim.announced_trip_list

