from source.entities.simulation import Simulation
import copy


class Manual:

	def __init__(self, config=None, tracker=None):
		pass

	def assign_cars(self, sim: Simulation):
		for trip in sim.announced_trip_list:
			if not trip.has_a_car():
				car_id = int(input(f"Choose car id to assign TRIP ({trip}) or -1 to leave unassigned: "))
				trip.car_id = car_id
		return sim.announced_trip_list

