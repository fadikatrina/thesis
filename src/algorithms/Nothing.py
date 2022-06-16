from src.entities.simulation import Simulation


class Nothing:

	def __init__(self, config=None, tracker=None):
		pass

	def assign_cars(self, sim: Simulation):
		return sim.announced_trip_list

